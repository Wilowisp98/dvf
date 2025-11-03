from typing import Dict, Any, List, Optional
from dvf.src.validations.base_validator import BaseValidator

class PKNullValidator(BaseValidator):
    def __init__(self, primary_key: Optional[str]):
        self.primary_key = primary_key

    def validate(self, row: Dict[str, Any]) -> List[str]:
        if self.primary_key:
            value = row.get(self.primary_key)

            if value is None or (isinstance(value, str) and not value.strip()):
                return ["Primary key column is null, empty or missing from the row."]
                    
        return []
