#!/usr/bin/env python

import warnings
from datetime import date, datetime
from keyword import iskeyword
from typing import Any, Dict, Iterable, Optional, Protocol, Sequence, Tuple, Type


class FormatProto(Protocol):
    """
    Defines a "formatter" class as one which
    interprets an instance as something else
    """

    def __call__(self, value: Any) -> Any:
        ...


class NamerProto(Protocol):
    """
    Defines a class which takes "field names"
    and cleans them to conform to some other
    standard
    """

    def __call__(self, value: str) -> str:
        ...


class FormatGuesser(FormatProto):
    """
    Try to determine an appropriate Python format
    for a given field value in JSON

    >>> FormatGuesser()(1) == int
    True
    >>> FormatGuesser()("2011-01-01") == date
    True
    """

    date_formats: Sequence[str] = (r"%Y-%m-%d",)
    datetime_formats: Sequence[str] = (r"%Y-%m-%d %H:%M:%S",)

    def _try_date(self, value: str) -> Optional[Type[date]]:
        for fmt in self.date_formats:
            try:
                datetime.strptime(value, fmt)
                return date
            except Exception:  # noqa: F841
                continue
        return None

    def _try_strptime(self, value: str) -> Optional[Type[datetime]]:
        for fmt in self.datetime_formats:
            try:
                datetime.strptime(value, fmt)
                return datetime
            except Exception:  # noqa: F841
                continue

        return None

    def __call__(self, value: Any) -> Type[Any]:
        """
        >>> f = FormatGuesser()
        >>> f(1) == int
        True
        >>> f("foo") == str
        True
        """
        if type(value) in {float, int}:
            return type(value)

        if isinstance(value, str):
            fmt = self._try_date(value) or self._try_strptime(value)
            if fmt:
                return fmt
        return type(value)


class FieldRenamer(NamerProto):
    """ "
    Try to determine an appropriate
    Pydantic or Djangofield name
    from a JSON dict
    >>> renamer = FieldRenamer()
    >>> renamer("something")
    'something'
    >>> renamer("50%_")
    'r_50'
    """

    translate: Dict[int, str] = str.maketrans({"%": "_", " ": "_", "(": "_", ")": "_", "/": "_"})
    field_overrides: Sequence[Tuple[str, str]] = tuple()

    def _isvalid(self, value: str) -> bool:
        """
        Return whether the current value can be considered an "identifier"
        These are normal Python rules plus some Django rules
        >>> f = FieldRenamer()
        >>> f._isvalid("import")
        False
        >>> f._isvalid("pk")
        False
        >>> f._isvalid("50")
        False
        """
        return value.isidentifier() and not iskeyword(value) and value != "pk"

    def __call__(self, value: str) -> str:
        """
        parse field name to something appropriate if necessary
        """
        for i in self.field_overrides:
            if i[0] == value:
                return i[1]

        # Strip out spaces, %, etc, and ensure we don't use a
        # "keyword" by accident
        translated = value.translate(self.translate).lower()
        if not self._isvalid(translated):
            translated = f"r_{translated}"  # This prefix may be attached to fields which start with a number
        try:
            assert self._isvalid(translated)
        except AssertionError:
            raise KeyError(f"Value {translated} cannot be used as an identifier")
        # Fields also cannot contain dunder
        while "__" in translated:
            translated = translated.replace("__", "_")
        translated = translated.strip("_")
        return translated


class DjangoFormatGuesser(FormatProto):

    type_guesser = FormatGuesser()
    default_types: Dict[type, str] = {
        int: "models.IntegerField(null=True, blank=True)",
        str: "models.CharField(null=True, blank=True, max_length=1024)",
        datetime: "models.DateTimeField(null=True, blank=True)",
        date: "models.DateField(null=True, blank=True)",
        float: "models.FloatField(null=True, blank=True)",
        bool: "models.BooleanField(null=True, blank=True)",
    }

    def __init__(self, mapper: Optional[Dict[type, str]] = None):
        self.mapper = {**self.default_types, **mapper} if mapper else self.default_types

    def __call__(self, value) -> str:
        """
        Interpret a "json" type as a "django" field definition
        This takes any "python" value and returns a "Django" field as a string
        >>> fmt = DjangoFormatGuesser()
        >>> fmt(1)
        'models.IntegerField(null=True, blank=True)'
        >>> fmt(1.1)
        'models.FloatField(null=True, blank=True)'
        >>> fmt("hello World")
        'models.CharField(null=True, blank=True, max_length=1024)'
        >>> fmt("2020-01-01")
        'models.DateField(null=True, blank=True)'
        >>> fmt("2020-01-01 12:00:00")
        'models.DateTimeField(null=True, blank=True)'
        """
        py_type = self.type_guesser(value)
        if py_type in self.mapper:
            return self.mapper[py_type]
        warnings.warn(f"No field type for python type {py_type} (from {value})")
        return self.mapper[str]


class JsonToPython:
    def __init__(
        self,
        formatter: Type[FormatProto] = FormatGuesser,
        fielder: Type[NamerProto] = FieldRenamer,
    ):
        self.formatter = formatter()
        self.fielder = fielder()

    def __call__(self, js: Dict) -> Iterable[str]:
        raise NotImplementedError("Expected to be overridden in subclass")


class JsonToDjango(JsonToPython):
    def __init__(self, formatter: Type[FormatProto] = DjangoFormatGuesser):
        super().__init__(formatter=formatter)

    def __call__(self, js: Dict):
        """
        Returns a "Django Model Field" definition based on a json object
        >>> formatter = JsonToDjango()
        >>> [*formatter({"a": 1})][0]
        'a = models.IntegerField(null=True, blank=True)'
        >>> [*formatter({"50%_report": False})][0]
        'r_50_report = models.BooleanField(null=True, blank=True)'
        """
        for field_name, field_value in js.items():
            yield f"""{self.fielder(field_name)} = {self.formatter(field_value)}"""


class JsonToPydantic(JsonToPython):
    def __call__(self, js: Dict):
        """
        Returns a "Pydantic" definition based on a json object
        >>> jtop = JsonToPydantic()
        >>> [*jtop({"a": 1})][0]
        'a: Optional[int]'
        >>> [*jtop({"50%_report": False})][0]
        'r_50_report: Optional[bool]'
        """
        for field_name, field_value in js.items():
            yield f"""{self.fielder(field_name)}: Optional[{self.formatter(field_value).__name__}]"""  # noqa: E501


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
