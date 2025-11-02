from typing import Dict, Any, List
from src.validations.base_validator import BaseValidator

class PKNullValidator(BaseValidator):
    def __init__(self, primary_keys: List[str]):
        self.primary_keys = primary_keys

    def validate(self, row: Dict[str, Any]) -> List[str]:
        errors = []
        if self.primary_keys:
            for column in self.primary_keys:
                value = row.get(column)

                if value is None or (isinstance(value, str) and not value.strip()):
                    errors.append(f"Primary key column '{column}' is null, empty or missing from the row.")
                    
        return errors
