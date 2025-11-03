from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, Dict, List, Set

ALLOWED_DATA_TYPES: Set[str] = {'int', 'str', 'float', 'decimal'}

class Config(BaseModel):
    model_config = ConfigDict(extra="forbid")

    table_schema: Optional[Dict[str, tuple[str, bool]]] = None
    primary_key: Optional[str] = None
    composite_keys: Optional[List[str]] = None

    @field_validator("table_schema")
    @classmethod
    def validate_schema_contents(cls, v):
        if v is None:
            return None
        
        for col, (data_type, is_optional) in v.items():
            if data_type not in ALLOWED_DATA_TYPES:
                raise ValueError(
                    f"Invalid data type '{data_type}' for column '{col}'.\n"
                    f"Must be one of: {list(ALLOWED_DATA_TYPES)}"
                )
            if not isinstance(is_optional, bool):
                raise ValueError(f"Optional flag for '{col}' must be a boolean")
        return v
    
    @field_validator("composite_keys")
    @classmethod
    def validate_composite_keys(cls, v):
        if v is None:
            return None
        
        if len(v) < 2:
            raise ValueError(
                "Can't be a composite key and only have one key. Did you mean *primary key*?"
            )
        return v