#!/usr/bin/env python

from __future__ import annotations

import json
import os
import warnings
from datetime import date, datetime
from decimal import Decimal

# from pnds_db.pnds_data.importer import read_data_json, get_tables
from io import StringIO, TextIOBase
from textwrap import dedent, indent
from typing import Dict, List, Optional, Sequence, Tuple, Type

from rich.progress import Progress

from mdb_codegen.jsontools import FieldRenamer, NamerProto
from mdb_codegen.mdbtools import AccessColumn, AccessDatabase, AccessTable


class AccessTableNames:
    """
    Wrap some useful functions to fetch consistent names for
    an Access table
    """

    overrides: Optional[Tuple[Tuple[str, str]]] = None

    def clean_table_name(self, table: AccessTable, replace_underscore: bool = True, lower: bool = False) -> str:
        """
        Generate a unique, python-classname-valid table name
        from the provided Access table instance and its siblings
        """

        def tname(t: AccessTable):
            """
            Replace underscores and strip whitespace
            """
            _t = t.table
            if replace_underscore:
                _t = _t.replace("_", "")
            if lower:
                _t = _t.lower()
            return _t

        # Specify individual table names manually in `overrides`
        if self.overrides:
            for access_name, clean_name in self.overrides:
                if table.table == access_name:
                    return clean_name

        # Prepare an integer to differentiate between table names
        # in cases where different access tables resolve to the same name
        # in this class
        uniqifier = 0
        for other_table in table.acess_database.tables.values():
            if other_table == table:
                break
            if tname(other_table) == tname(table):
                uniqifier += 1
        return f"{tname(table)}{uniqifier}" if uniqifier else tname(table)

    def postgres_table_name(self, table: AccessTable) -> str:
        """
        The name to use for the postgres Table
        Override this method to give lower-case names
        """
        return table.table

    def base_model(self, table: AccessTable) -> str:
        return f"{self.clean_table_name(table)}In"

    def model(self, table: AccessTable) -> str:
        """
        This is the model name for models.py
        """
        return self.clean_table_name(table)

    def api(self, table: AccessTable) -> str:
        return self.clean_table_name(table)

    def model_schema(self, table: AccessTable) -> str:
        """
        The model name to use for the Pydantic class
        """
        return f"{self.clean_table_name(table)}Out"


class IOWriter:
    """
    Encapsulate writes to a file-like object
    """

    def __init__(self, builder: TextIOBase = StringIO()):
        self.builder = builder

    def _importstrings(self, *args, **kwargs) -> Sequence[str]:
        """
        generate the "imports" required by
        this file
        """
        return []

    def _write(self, s: str) -> None:
        """
        Called with no args, write a newline else
        write the string
        """
        self.builder.write(s)

    def _imports(self):
        """
        Write "imports" to the IO class
        """
        self._write(f"{os.linesep.join(self._importstrings())}")
        self._write(os.linesep * 2)


class AccessTableToPydantic(IOWriter):
    def __init__(
        self,
        builder: TextIOBase,
        table_namer: Type[AccessTableNames] = AccessTableNames,
        field_namer: Type[NamerProto] = FieldRenamer,
    ):
        self.builder = builder
        self.field_writer = AccessColumnToPydantic(builder, field_namer=field_namer)
        self.table_namer = table_namer()

    def _importstrings(self, *args, **kwargs) -> Sequence[str]:
        return (
            "from datetime import date, datetime",
            "from decimal import Decimal",
            "\n",  # This should be isort compatible
            "from pydantic import BaseModel, Field",
        )

    def __call__(self, table: AccessTable) -> None:

        bname = self.table_namer.base_model(table)
        self._write(
            dedent(
                f'''\n
                class {bname}(BaseModel):
                    """
                    Originally sourced from {table} ({table.count} records)
                    """\n
                '''
            )
        )
        for column in table.columns:
            self.field_writer(column)


class AccessColumnToDjango(IOWriter):
    """
    Convert an "Access Column" to a Django column string repr
    """

    def __init__(self, builder: TextIOBase, field_renamer: NamerProto = FieldRenamer(), pg_namer: Optional[NamerProto] = None):
        super().__init__(builder)
        self.field_namer = field_renamer
        self.pg_field_namer = pg_namer or self.field_namer

    def __call__(self, col: AccessColumn, pre: str = " " * 4, primary: bool = False):

        column_lookup: Dict[type, Tuple[str, List[str]]] = {
            str: ("CharField", ["max_length=1024"]),
            date: ("DateField", []),
            datetime: ("DateTimeField", []),
            int: ("IntegerField", []),
            float: ("FloatField", []),
            bool: ("BooleanField", []),
            Decimal: ("DecimalField", ["decimal_places=2", "max_digits=12"]),
        }

        col_type_params = column_lookup[col.py_type]
        if primary:
            col_type_params[1].extend(
                [
                    "primary_key=True",
                ]
            )
        elif not col.is_required:
            col_type_params[1].extend(["null=True", "blank=True"])
        col_s = self.pg_field_namer(col.column_name.decode())
        col_name = self.field_namer(col_s)

        # If the col_name is different from the "django name", use
        # db_column
        if "%" in col_s:
            # There is special handling here for columns with '%' signs
            # which cause problems with Django / psycopg2 escaping
            col_s = col_s.replace("%", "")

        if col_name != col_s:
            if '"' in col_s:
                col_type_params[1].extend([f'db_column="""{col_s}"""'])
            else:
                col_type_params[1].extend([f'db_column="{col_s}"'])

        self._write(f"""{pre}{col_name} = models.{col_type_params[0]}({', '.join(col_type_params[1])})\n""")


class AccessColumnToPydantic(IOWriter):
    """
    Convert an "Access Column" to a Django column string repr
    """

    def __init__(self, builder: TextIOBase, field_namer: NamerProto = FieldRenamer(), pg_namer: Optional[NamerProto] = None):
        super().__init__(builder=builder)
        self.field_namer = field_namer
        self.pg_field_namer = pg_namer or self.field_namer

    def __call__(self, col: AccessColumn, pre: str = " " * 4):
        column_lookup: Dict[type, Tuple[str, List[str]]] = {
            str: ("str", []),
            date: ("date", []),
            datetime: ("datetime", []),
            int: ("int", []),
            float: ("float", []),
            bool: ("bool", []),
            Decimal: ("Decimal", []),
        }

        col_type_params = column_lookup[col.py_type]
        col_s = self.pg_field_namer(col.column_name.decode())
        col_name = self.field_namer(col_s)
        # If the col_name is different from the "django name", use
        # db_column

        if not col.is_required:
            col_type_params[1].extend(["None"])

        if col_name != col_s:
            if '"' in col_s:
                col_type_params[1].extend([f'alias="""{col_s}"""'])
            else:
                col_type_params[1].extend([f'alias="{col_s}"'])
        self._write(f"""{pre}{col_name}: {col_type_params[0]} = Field({', '.join(col_type_params[1])})\n""")


class AccessTableToDjango(IOWriter):
    """
    Writes an MS Access table as a Django `models.py` file
    """

    def __init__(
        self,
        builder: TextIOBase,
        field_writer: Type[AccessColumnToDjango] = AccessColumnToDjango,
        table_namer: Type[AccessTableNames] = AccessTableNames,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.builder = builder
        self.field_writer = field_writer(builder)
        self.table_namer = table_namer()

    def _importstrings(self):
        return ("from django.db import models",)

    def __call__(self, table: AccessTable) -> None:
        # Use the first row in the table to generate a Django
        # class definition
        pre = " " * 4
        class_name = f"class {self.table_namer.model(table)}(models.Model):\n"
        doc_string = indent(
            f'"""\nOriginally sourced from {table} ({table.count} records)\n"""\n',
            pre,
        )

        self._write(class_name)
        self._write(doc_string)
        # Write the "db_table" parameter
        self._write(indent("\nclass Meta:\n", pre))
        self._write(indent(f'db_table = "{self.table_namer.postgres_table_name(table)}"\n\n', pre * 2))

        for colidx, column in enumerate(table.columns):
            # Assume the first column is the primary key
            self.field_writer(column, primary=colidx == 0)
        # Add 2 newlines
        self._write("\n")
        self._write("\n")


class AccessTableToAdmin(IOWriter):
    """
    Write an access table as an "admin.py" class
    """

    def __init__(
        self,
        builder: TextIOBase,
        table_namer: Type[AccessTableNames] = AccessTableNames,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.builder = builder
        self.table_namer = table_namer()

    def _importstrings(self):
        return (
            "from django.contrib import admin",
            "from . import models",
        )

    def __call__(self, table: AccessTable) -> None:
        # Use the first row in the table to generate a Django
        # class definition
        decorator = f"admin.register(models.{self.table_namer.model(table)})"
        class_name = f"{self.table_namer.model(table)}Admin(admin.ModelAdmin)"
        list_display_text = f"[n.name for n in models.{self.table_namer.model(table)}._meta.fields]"

        self._write(
            dedent(
                f"""
        @{decorator}
        class {class_name}:
            list_display = {list_display_text}

        """
            )
        )


class AccessTableToModelSchema(AccessTableToDjango, IOWriter):
    """
    Returns a Django-Ninja "ModelSchema" template
    """

    def _importstrings(self):
        """
        Specifies imports from django-ninja and a
        sinple "Error" schema
        """
        return (
            "from ninja import Schema, ModelSchema",
            "",
            "from . import models",
            "",
            "",
            "class Error(Schema):",
            "    message: str",
        )

    def __call__(self, table: AccessTable, *args, **kwargs) -> None:

        class_name = f"{self.table_namer.model_schema(table)}(ModelSchema)"

        self._write(
            dedent(
                f'''\n
            class {class_name}:
                """
                Originally sourced from {table} ({table.count} records)
                """
                class Config:
                    model = models.{self.table_namer.model(table)}
                    model_fields = "__all__"
                \n'''
            )
        )


class AccessTableToApiPostEntry(IOWriter):
    """
    Note: This is far less "polished" than others
    and likely requires a lot more manual intervention
    """

    def __init__(
        self,
        builder: TextIOBase,
        field_namer: Type[NamerProto] = FieldRenamer,
        django_field_namer: Type[NamerProto] = FieldRenamer,
        table_namer: Type[AccessTableNames] = AccessTableNames,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.builder = builder
        self.django_field_namer = django_field_namer()
        self.field_namer = field_namer()
        self.table_namer = table_namer()

    def _write(self, s: str) -> None:
        self.builder.write(s)

    def _importstrings(self):
        """
        Add required imports
        """
        return (
            "from typing import List, Optional, Type",
            "from http import HTTPStatus",
            "from ninja import ModelSchema, NinjaAPI",
            "",
            "from . import models",
            "from . import base_models",
            "from . import schema",
            "",
            "",
            "api = NinjaAPI()",
            "",
            "def _get_pk(model: Type[models.Model]) -> models.Field:",
            "    for field in model._meta.fields:",
            '        if getattr(field, "primary_key", False) is True:',
            "            return field",
            '    raise KeyError("No primary key?")',
            "",
        )

    def __call__(self, table: AccessTable) -> None:
        # Use the first row in the table to generate a Pydantic
        # class definition

        decorator = f'api.post("/{self.table_namer.api(table)}", response={{HTTPStatus.CREATED: schema.{self.table_namer.model_schema(table)}, HTTPStatus.OK: schema.{self.table_namer.model_schema(table)}, HTTPStatus.BAD_REQUEST: schema.Error}})'  # noqa: E501
        def_name = (
            f"add_{self.table_namer.api(table)}(request, data: base_models.{self.table_namer.base_model(table)})"
        )
        self._write(
            dedent(
                f"""
            @{decorator}
            async def {def_name}:
                model = models.{self.table_namer.model(table)}
                objects = model.objects
                pk_field =  _get_pk(model).name # This is the name of the "primary key" field
                data_for_update = data.dict()
                data_for_update.pop(pk_field)

                instance, created = await objects.aupdate_or_create(
                    pk = pk_field,
                    defaults=data_for_update
                )

                return instance
        \n\n"""
            )
        )


class AccessTableToApiGetEntry(IOWriter):
    def __init__(self, builder: TextIOBase, table_namer: AccessTableNames = AccessTableNames(), *args, **kwargs):
        self.builder = builder
        self.django_fielder = FieldRenamer()
        self.table_namer = table_namer

    def _importstrings(self):
        """
        Add required imports
        """
        return (
            "from typing import List, Optional",
            "from ninja import ModelSchema, NinjaAPI",
            "api = NinjaAPI()",
            "\n",
        )

    def __call__(self, table: AccessTable) -> None:
        """
        Write a ModelSchema definition to
        this class instance' builder
        """
        api = self.table_namer.api(table)
        schema = self.table_namer.model_schema(table)
        model = self.table_namer.model(table)
        self._write(
            dedent(
                f'''
                @api.get("/{api}-list", response=List[{schema}])
                def get_{api}_list(request):
                    """
                    Originally sourced from {table} ({table.count} records)
                    """
                    return models.{model}.objects.all()\n\n
                '''
            )
        )


class AccessDatabaseToDjangoModels:
    """
    Intended to be able to generate a complete "models.py" file from an accdb / mdb
    """

    def __init__(self, builder: TextIOBase, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field_namer = FieldRenamer()
        self.table_write = AccessTableToDjango(builder)

    def __call__(self, db: AccessDatabase):
        self.table_write._imports()
        for table in db.tables.values():
            self.table_write(table)


def push_table(
    table: AccessTable, endpoint: str = "http://localhost:8000/api/financemonitoring", raise_exceptions=True
):
    import requests  # noqa  Requires "pip install requests"

    with Progress() as progress:
        task_1 = progress.add_task(f"Update {table}", total=table.count)
        for x in table.json():
            response = requests.post(endpoint, json=json.loads(x))

            if not response.ok:
                warnings.warn(response.reason)
                warnings.warn(x.decode())
                if raise_exceptions:
                    response.raise_for_status()
            progress.update(task_1, advance=1)


class PNDSAccessTableNames(AccessTableNames):
    """
    Corrects some misspelt table names
    """
    def postgres_table_name(self, table: AccessTable) -> str:
        """
        The name to use for the postgres Table
        """
        return self.clean_table_name(table , replace_underscore=False, lower=True)

    overrides = (("SubpojectOutputs", "SubprojectOutputs"),)
