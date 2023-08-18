#!/usr/bin/env python

from __future__ import annotations

import json
import re
import subprocess
import warnings
from datetime import datetime
from decimal import Decimal
from enum import Enum
from functools import cached_property
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, Generator, Optional, Sequence, Type, Union


class MdbTools(str, Enum):
    """
    Enum the tools available via `mdbtools 1.0.0` for
    MS Access file interaction
    """

    VER = "mdb-ver"  # Prints the version (JET 3 or 4) of an mdb file.
    SCHEMA = "mdb-schema"  # Prints DDL for the specified table.
    EXPORT = "mdb-export"  # Export table to CSV or SQL formats.
    JSON = "mdb-json"  # Export table to JSON format.
    TABLES = "mdb-tables"  # A simple dump of table names to be used with shell scripts.
    COUNT = "mdb-count"  # A simple count of number of rows in a table, to be used in shell scripts and ETL pipelines.
    SQL = "mdb-sql"  # A simple SQL engine (also used by ODBC and gmdb).
    QUERIES = "mdb-queries"  # List and print queries stored in the database.
    # These tools are deprecated / developer use
    HEXDUMP = "mdb-hexdump"  # (in src/extras) Simple hex dump utility to look at mdb files.
    ARRAY = "mdb-array"  # Export data in an MDB database table to a C array.
    HEADER = "mdb-header"  # Generates a C header to be used in exporting mdb data to a C prog.
    PARSECSV = "mdb-parsecsv"  # Generates a C program given a CSV file made with mdb-export.


class AccessColumn:
    """
    >>> AccessColumn(b"example", b"Long Integer").py_type.__name__
    'int'
    >>> AccessColumn(b"example", b"Text").py_type.__name__
    'str'
    >>> AccessColumn.from_schema(b"	[Table_name]			Text (255)").py_type.__name__
    'str'
    >>> AccessColumn.from_schema(b"	[Table_name]			Long Integer").py_type.__name__
    'int'
    """

    col_regex = re.compile(rb"\s*\[(?P<field>.*?)\]\s*(?P<field_type>[^,^(.]*)")

    type_lookups = {
        b"Long Integer": int,
        b"DateTime": datetime,
        b"Text": str,
        b"Byte": int,
        b"Integer": int,
        b"Boolean": bool,
        b"Memo": str,
        b"Double": int,
        b"Currency": Decimal,
        b"Numeric": float,
        b"Single": float,
    }

    def __init__(self, column_name: bytes, column_type: bytes):
        """
        >>> c = AccessColumn(column_name=b"test", column_type=b"Boolean")
        >>> c.column_type
        b'Boolean'
        >>> c.column_name
        b'test'
        """
        assert any((column_type.startswith(t) for t in self.type_lookups))
        self.column_name = column_name
        self.column_type = column_type

    @classmethod
    def from_schema(cls, col_def: bytes) -> Optional[AccessColumn]:
        """
        Returns an "AccessColumn" instance
        from a schema dump line

        To read in an entire file:
        with open("schema.txt") as f:
            map(AccessColumn.from_schema, filter(AccessColumn.is_schema_line, (bytes(l) for l in f.readlines())))

        >>> AccessColumn.from_schema(b''' [SucoCMTID] Text (50) NOT NULL, ''').column_type
        b'Text'
        """
        match = re.match(cls.col_regex, col_def)
        if match:
            groups = match.groups()
        else:
            warnings.warn(f"Not a valid line: {str(col_def)}")
            return None
        field_name, field_type = groups
        return cls(field_name, field_type.strip())

    @classmethod
    def from_schema_lines(cls, schema_def: bytes, *args, **kwargs):
        return [cls.from_schema(line) for line in schema_def.split(b"\n") if cls.is_schema_line(line)]

    @cached_property
    def is_required(self) -> bool:
        """
        NOT NULL in Access / `null=False` in Django / not [Optional] in pydantic
        >>> AccessColumn(column_name=b"test", column_type=b"Boolean").is_required
        False
        >>> AccessColumn(column_name=b"test", column_type=b"Boolean NOT NULL").is_required
        True
        """
        return b"NOT NULL" in self.column_type.upper()

    @cached_property
    def py_type(self) -> Type[Any]:

        for column_lookup, py_type_ in self.type_lookups.items():
            if self.column_type == column_lookup:
                return py_type_
            # We use "startswith" to avoid modifiers like NOT NULL
            if self.column_type.startswith(column_lookup):
                return py_type_
        warnings.warn(f"Uncaught type: {str(self.column_type)}")
        return str

    @staticmethod
    def is_schema_line(line: bytes) -> bool:
        """
        Filter to the lines which define columns only
        >>> AccessColumn.is_schema_line(b" [BlacklistID]           Long Integer, ")
        True
        >>> AccessColumn.is_schema_line(b");")
        False
        """

        return (
            line not in {b"", b");", b" (", b"\n", b"(\n", b" (\n", b");\n"}
            and not line.startswith(b"--")
            and not line.startswith(b"CREATE TABLE")
        )

    def __str__(self):
        return f"{self.column_name.decode()} : {self.column_type.decode()} ({self.py_type.__name__})"


class AccessTable:
    """
    Represents a single table in an Access database and
    wraps certain `mdb_tools` items
    """

    def __init__(self, access_database: AccessDatabase, table: str):
        self.acess_database = access_database
        self.table = table

    def __repr__(self):
        return f"{self.table} in {self.acess_database.access_file}"

    @cached_property
    def count(self) -> int:
        completed_process = subprocess.run(
            [MdbTools.COUNT, self.acess_database.access_file, self.table],
            capture_output=True,
            check=True,
        )
        return_value = completed_process.stdout.strip()
        return int(return_value)

    def export(self, *args) -> bytes:
        """
        export data from MDB file

        -H, --no-header           Suppress header row.
        -d, --delimiter=char      Specify an alternative column delimiter. Default is comma.
        -R, --row-delimiter=char  Specify a row delimiter
        -Q, --no-quote            Don't wrap text-like fields in quotes.
        -q, --quote=char          Use <char> to wrap text-like fields. Default is double quote.
        -X, --escape=format       Use <char> to escape quoted characters within a field. Default is doubling.
        -e, --escape-invisible    Use C-style escaping for return
                                  (\r), tab (\t), line-feed (\n), and back-slash (\\) characters.
                                  Default is to leave as they are.
        -I, --insert=backend      INSERT statements (instead of CSV)
        -N, --namespace=namespace Prefix identifiers with namespace
        -S, --batch-size=int      Size of insert batches on supported platforms.
        -D, --date-format=format  Set the date format (see strftime(3) for details)
        -T, --datetime-format=formatSet the date/time format (see strftime(3) for details)
        -0, --null=char           Use <char> to represent a NULL value
        -b, --bin=strip|raw|octal|hexBinary export mode
        -B, --boolean-words       Use TRUE/FALSE in Boolean fields (default is 0/1)
        """
        return subprocess.run(
            [MdbTools.EXPORT, self.acess_database.access_file, self.table, *args],
            capture_output=True,
            check=True,
        ).stdout

    @cached_property
    def schema(self, *args) -> bytes:
        """
        Fetch the "schema" file
        """
        return subprocess.run(
            [
                MdbTools.SCHEMA,
                f"{self.acess_database.access_file.absolute()}",
                "-T",
                self.table,
                *args,
            ],
            capture_output=True,
            check=True,
        ).stdout

    @cached_property
    def columns(self) -> Sequence[AccessColumn]:
        return AccessColumn.from_schema_lines(self.schema)

    def json(self, date_format="%Y-%m-%d", date_time_format="%Y-%m-%d %H:%M:%S", *args):
        """
        export data from Access file to JSON

        -D, --date-format=format  Set the date format (see strftime(3) for details)
        -T, --datetime-format=formatSet the date/time format (see strftime(3) for details)
        -U, --no-unprintable      Change unprintable characters to spaces (otherwise escaped as 00XX)
        """
        process = subprocess.run(
            [
                MdbTools.JSON,
                "-D",
                date_format,
                "-T",
                date_time_format,
                self.acess_database.access_file,
                self.table,
                *args,
            ],
            capture_output=True,
            check=True,
        )
        return BytesIO(process.stdout)

    def dict(self, *args) -> Union[Generator[Dict, None, None], None]:
        for line in self.json():
            yield json.loads(line)


class AccessDatabase:
    """
    Wraps certain subprocess calls for an Access database
    """

    def __init__(self, access_file: Path):
        self.access_file = access_file
        table_names = subprocess.run([MdbTools.TABLES, self.access_file], text=True, capture_output=True).stdout.split(
            " "
        )
        self.tables = {t: AccessTable(self, t) for t in table_names if len(t.strip())}


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
