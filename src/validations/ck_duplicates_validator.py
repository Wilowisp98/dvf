from typing import Any, Dict, List, Set, Optional
from src.validations.base_validator import BaseValidator

class CKDuplicateValidator(BaseValidator):
    def __init__(self, composite_keys: Optional[List[str]]):
        self.composite_keys = composite_keys
        self.seen_keys: Set[Any] = set()

    def validate(self, row: Dict[str, Any]) -> List[str]:
        if self.composite_keys:
            key = tuple(row.get(k) for k in self.composite_keys)

            if isinstance(key, tuple) and None in key:
                return []

            if key in self.seen_keys:
                return [f"Duplicate composite key found: {key}"]
            else:
                self.seen_keys.add(key)

        return []