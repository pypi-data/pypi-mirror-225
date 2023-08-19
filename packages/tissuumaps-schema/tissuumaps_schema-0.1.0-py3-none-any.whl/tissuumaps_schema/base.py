from typing import Any, Optional, Type, TypeVar

from pydantic import BaseModel, ConfigDict, Field


class SchemaBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


TRoot = TypeVar("TRoot", bound="RootSchemaBaseModel")


class RootSchemaBaseModel(BaseModel):
    _previous_model_type: Optional[Type["RootSchemaBaseModel"]] = None
    schema_version: str = Field(alias="schemaVersion")

    @classmethod
    def parse(
        cls: Type[TRoot], model_data: dict[str, Any], strict: Optional[bool] = None
    ) -> TRoot:
        return cls.model_validate(model_data, strict=strict)

    @classmethod
    def upgrade(cls: Type[TRoot], model: "RootSchemaBaseModel") -> TRoot:
        if isinstance(model, cls):
            return model
        if cls._previous_model_type is not None:
            if not isinstance(model, cls._previous_model_type):
                model = cls._previous_model_type.upgrade(model)
                assert isinstance(model, cls._previous_model_type)
            return cls._upgrade_from_previous_model(model)
        raise NotImplementedError(f"No upgrade path for version {model.schema_version}")

    @classmethod
    def _upgrade_from_previous_model(
        cls: Type[TRoot], previous_model: "RootSchemaBaseModel"
    ) -> TRoot:
        raise NotImplementedError()
