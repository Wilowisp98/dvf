from typing import Dict, Any, List, Optional
from src.dvf.validations.base_validator import BaseValidator

class CKNullValidator(BaseValidator):
    def __init__(self, composite_keys: Optional[List[str]]):
        self.composite_keys = composite_keys

    def validate(self, row: Dict[str, Any]) -> List[str]:
        errors = []
        if self.composite_keys:
            for column in self.composite_keys:
                value = row.get(column)

                if value is None or (isinstance(value, str) and not value.strip()):
                    errors.append(f"Composite key column '{column}' is null, empty or missing from the row.")
                    
        return errors
