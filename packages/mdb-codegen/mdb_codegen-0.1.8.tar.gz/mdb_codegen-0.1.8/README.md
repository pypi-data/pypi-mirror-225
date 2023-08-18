# mdb-codegen

A static file generator to create Django model definitions and Pydantic BaseModels from an MS Access database.

This reads data from an Access file using [mdbtools](https://github.com/mdbtools/mdbtools), see the [installation](https://github.com/mdbtools/mdbtools#installation) instructions on how to install for your os.


## Howto

 This parser is based on different classes to determine the Django model name, Pydantic "BaseModel" name, and the fields for Django and/or Pydantic.

There is a command line tool to generate files, `mdb-codegen.py`

 - Run `poetry install`
 - Then run `cd mdb_codegen`
 - Then run `./mdb-codegen.py path_to_your_db`
