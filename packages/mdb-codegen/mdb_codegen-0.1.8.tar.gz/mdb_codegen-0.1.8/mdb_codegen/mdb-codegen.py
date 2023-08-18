#!/usr/bin/env python

import argparse
import os
from pathlib import Path

from rich.progress import Progress

from mdb_codegen.djaccess import (
    AccessTableToAdmin,
    AccessTableToApiPostEntry,
    AccessTableToDjango,
    AccessTableToModelSchema,
    AccessTableToPydantic,
    PNDSAccessTableNames,
)
from mdb_codegen.mdbtools import AccessDatabase

parser = argparse.ArgumentParser(
    prog="mdb-codegen",
    description="Generate Django and Pydantic code definitions from an Access database",
    argument_default=None,
)

parser.add_argument("db", action="store", nargs=1, help="Input access database")

args = parser.parse_args()


db: AccessDatabase = AccessDatabase(Path(args.db[0]))
output = "./output"
os.makedirs(output, exist_ok=True)
table_namer = PNDSAccessTableNames
with Progress() as p:
    tablecount = len([*db.tables.keys()])
    model_progress = p.add_task("export models", total=tablecount)
    schema_progress = p.add_task("export schemas", total=tablecount)
    api_progress = p.add_task("export api", total=tablecount)
    mc_progress = p.add_task("export ModelSchemas", total=tablecount)
    admin_progress = p.add_task("export Admin", total=tablecount)

    with open(Path(output) / "models.py", "w") as builder:
        parser = AccessTableToDjango(builder, table_namer=table_namer)
        parser._imports()
        for table in db.tables.values():
            parser(table)
            p.update(model_progress, advance=1)

    with open(Path(output) / "schema.py", "w") as builder:
        parser = AccessTableToModelSchema(builder, table_namer=table_namer)
        parser._imports()
        for table in db.tables.values():
            parser(table)
            p.update(schema_progress, advance=1)

    with open(Path(output) / "api_post.py", "w") as builder:
        parser_post = AccessTableToApiPostEntry(builder, table_namer=table_namer)
        parser_post._imports()
        for table in db.tables.values():
            parser_post(table)
            p.update(api_progress, advance=1)

    with open(Path(output) / "base_models.py", "w") as builder:
        parser_pydantic = AccessTableToPydantic(builder, table_namer=table_namer)
        parser_pydantic._imports()
        for table in db.tables.values():
            parser_pydantic(table)
            p.update(mc_progress, advance=1)

    with open(Path(output) / "admin.py", "w") as builder:
        parser_pydantic = AccessTableToAdmin(builder, table_namer=table_namer)
        parser_pydantic._imports()
        for table in db.tables.values():
            parser_pydantic(table)
            p.update(admin_progress, advance=1)
