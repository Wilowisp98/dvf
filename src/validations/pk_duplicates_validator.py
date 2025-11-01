from typing import Any, Dict, List, Set, Optional
from src.validations.base_validator import BaseValidator

class PKDuplicateValidator(BaseValidator):
    def __init__(self, primary_keys: Optional[List[str]]):
        self.primary_keys = primary_keys
        self.seen_keys: Set[Any] = set()

    def validate(self, row: Dict[str, Any]) -> List[str]:
        errors = []
        if self.primary_keys:
            if len(self.primary_keys) == 1:
                key = row.get(self.primary_keys[0])
            else:
                key = tuple(row.get(k) for k in self.primary_keys)

            if key is None or (isinstance(key, tuple) and None in key):
                return errors

            if key in self.seen_keys:
                errors.append(f"Duplicate primary key found: {key}")
            else:
                self.seen_keys.add(key)

        return errors