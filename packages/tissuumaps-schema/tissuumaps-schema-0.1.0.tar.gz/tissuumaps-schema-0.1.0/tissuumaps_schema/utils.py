from typing import Any

from . import v01

SCHEMA_MODULES = [v01]

current_schema_module = v01


def guess_schema_version(model_data: dict[str, Any]) -> str:
    return model_data.get("schemaVersion", v01.VERSION)
