from dataclasses import fields
from src.config.config_model import Config
from typing import Dict, Any

def get_allowed_fields() -> set[str]:
    return {f.name for f in fields(Config)}

def validate(data: Dict[str, Any]) -> None:
    allowed_fields = get_allowed_fields()

    unknown_fields = set(data.keys()) - allowed_fields
    if unknown_fields:
        raise ValueError(f"Unknown fields in config: {', '.join(unknown_fields)}")

    if "schema" in data:
        _validate_schema(data["schema"])
    if "primary_keys" in data:
        _validate_keys(data["primary_keys"], field="primary_keys")
    if "foreign_keys" in data:
        _validate_keys(data["foreign_keys"], field="foreign_keys")

def _validate_schema(schema: Any) -> None:
    if not isinstance(schema, dict):
        raise ValueError("`schema` must be a dictionary of columns.")

    for col, props in schema.items():
        if not isinstance(props, list) or len(props) != 2:
            raise ValueError(f"Schema for '{col}' must be a list of [data_type, is_optional].")

        data_type, is_optional = props
        if not isinstance(data_type, str):
            raise ValueError(f"Data type for '{col}' must be a string.")
        if not isinstance(is_optional, bool):
            raise ValueError(f"The second item for '{col}' must be a boolean.")

def _validate_keys(keys: Any, field: str) -> None:
    if not isinstance(keys, list) or not all(isinstance(k, str) for k in keys):
        raise ValueError(f"`{field}` must be a list of strings.")
