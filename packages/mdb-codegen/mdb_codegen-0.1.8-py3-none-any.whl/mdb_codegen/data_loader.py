# When loading data from a table we
# - determine the Pydantic instance to use
# - determine the model to use
# - do an "update_or_create" on the model

import importlib
from datetime import datetime
from pathlib import Path
from types import ModuleType
from typing import Iterator, Type, Union

from django.db import models
from django.db import transaction
from pydantic import BaseModel
import itertools

from rich.console import Console

console = Console()

from mdb_codegen.djaccess import AccessTableNames, PNDSAccessTableNames
from mdb_codegen.jsontools import FieldRenamer, NamerProto
from mdb_codegen.mdbtools import AccessDatabase, AccessTable


def _get_pk(model: Type[models.Model]) -> models.Field:
    for field in model._meta.fields:
        if getattr(field, "primary_key", False) is True:
            return field
    raise KeyError("No primary key?")


class ModelUpdater:
    def __init__(
        self,
        app_label: str,
        table_renamer: Type[AccessTableNames] = AccessTableNames,
        field_namer: Type[NamerProto] = FieldRenamer,
    ):
        self.table_renamer: AccessTableNames = table_renamer()
        self.field_namer: FieldRenamer = field_namer()
        self.models_: ModuleType = importlib.import_module(f"{app_label}.models")
        self.base_models_: ModuleType = importlib.import_module(f"{app_label}.base_models")

    def update_from_table(self, table: AccessTable, sample_only:bool = False):
        django_model: models.Model = getattr(self.models_, self.table_renamer.model(table))
        pydantic_base_model: BaseModel = getattr(self.base_models_, self.table_renamer.base_model(table))

        # List the current primary keys. Anything NOT in the list needs
        # to be created.

        # Fields to be updated are everything except for PK


        update_fields = [f for f in django_model._meta.fields if not f.primary_key]

        qs: models.QuerySet = django_model.objects

        lines = (json.replace(b"1900-01-00", b"1900-01-01") for json in table.json())
        if sample_only:
            lines = itertools.islice(lines, 5)

        pydantic_instances = [
            pydantic_base_model.parse_raw(line)
            for line in lines
        ]
        django_pk = _get_pk(django_model).name
        database_primary_keys = set(qs.values_list("pk", flat=True))

        # Instances already in the database
        # We need these fields from Django to match the "aliases"
        fieldmap = {k: getattr(v, 'alias', k) for k, v in pydantic_base_model.__fields__.items()}
        pydantic_instances_from_django = [pydantic_base_model.parse_obj(
            {alias: getattr(i, fieldname) for fieldname, alias in fieldmap.items()}
        ) for i in django_model.objects.all()]

        django_hashes = {hash(i) for i in pydantic_instances_from_django}
        pydantic_hashes = {hash(i) for i in pydantic_instances}

        unchanged = django_hashes.intersection(pydantic_hashes)
        to_create_or_update = pydantic_hashes.difference(django_hashes)

        create: Iterator[django_model] = (
            django_model(**{i: j for i, j in instance})
            for instance in pydantic_instances
            if hash(instance) in to_create_or_update and
            getattr(instance, django_pk) not in database_primary_keys
        )
        update: Iterator[django_model] = (
            django_model(**{i: j for i, j in instance})
            for instance in pydantic_instances
            if hash(instance) in to_create_or_update and
            getattr(instance, django_pk) in database_primary_keys
        )

        console.log(f"[yellow] Updating {table}")
        try:
            created = qs.bulk_create(create, batch_size=100)
        except Exception as E:
            console.log(f"[red]Failed to create records in {table}")
            console.log(f'{E}')
            return
        
        console.log(f"[green]created: {len(created)}")
        try:
            updated = qs.bulk_update(update, batch_size=1000, fields=[f.name for f in update_fields])
        except Exception as E:
            console.log(f"[red]Failed to update records in {table}")
            console.log(f'{E}')
            return
        console.log(f"[green]updated: {updated}")
        console.log(f"[green]skipped: {len(unchanged)}")

    def __call__(self, target: Union[AccessDatabase, AccessTable]):
        # Disable constraints until all tables are updated
        from django.db import connection
        with connection.constraint_checks_disabled():
            with transaction.atomic():
                if isinstance(target, AccessTable):
                    return self.update_from_table(target)
                elif isinstance(target, AccessDatabase):
                    for table in target.tables.values():
                        self.__call__(table)
                    return
                elif isinstance(target, Path):
                    return self.__call__(AccessDatabase(target))
    
        raise TypeError("Expected either a Table or a Database instance")


class PndsModelUpdater(ModelUpdater):
    def __init__(self):
        super().__init__(app_label="pnds_data", table_renamer=PNDSAccessTableNames)

    def __call__(self, target=AccessDatabase(Path.home() / "PNDS_Interim_MIS-Data.accdb")):
        super().__call__(target=target)
