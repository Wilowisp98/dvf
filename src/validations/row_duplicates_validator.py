from typing import Any, Dict, List, Set, Optional
from src.validations.base_validator import BaseValidator

class RowDuplicateValidator(BaseValidator):
    def __init__(self):
        self.seen_rows: Set[Any] = set()

    def validate(self, row: Dict[str, Any]) -> List[str]:
        key = tuple(row[k] for k in row.keys())
        if key in self.seen_rows:
            return ["Duplicate row found"] 
        else:
            self.seen_rows.add(key)
        
        return []