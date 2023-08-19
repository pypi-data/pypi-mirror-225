from pydantic import Field

from ..base import RootSchemaBaseModel

VERSION = "0.1"


class RootSchemaBaseModelV01(RootSchemaBaseModel):
    schema_version: str = Field(default=VERSION, alias="schemaVersion")
