from typing import Dict, Any, List, Optional
from decimal import Decimal
from dvf.src.validations.base_validator import BaseValidator

class SchemaValidator(BaseValidator):
    def __init__(self, schema: Optional[Dict[str, tuple[str, bool]]]):
        self.schema = schema

    def validate(self, row: Dict[str, Any]) -> List[str]:
        errors = []
        if self.schema:
            for col_name, (data_type, is_optional) in self.schema.items():
                value = row.get(col_name)
                is_missing = value in (None, "")

                if is_missing:
                    if not is_optional:
                        errors.append(f"Column '{col_name}' (type: {data_type}) is required but is missing.")
                    continue

                type_error = self._check_type(value, data_type, col_name)
                if type_error:
                    errors.append(type_error)

        return errors

    def _check_type(self, value: Any, data_type: str, col_name: str) -> Optional[str]:
        try:
            if data_type == "int":
                int(value)
            elif data_type == "float":
                float(value)
            elif data_type == "decimal":
                Decimal(value)
            elif data_type == "str":
                pass
            
            return None
        except:
            return f"Column '{col_name}' value '{value}' cannot be converted to {data_type}."