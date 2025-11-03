from typing import Any, Dict, List, Set, Optional
from src.dvf.validations.base_validator import BaseValidator

class PKDuplicateValidator(BaseValidator):
    def __init__(self, primary_key: Optional[str]):
        self.primary_key = primary_key
        self.seen_keys: Set[Any] = set()

    def validate(self, row: Dict[str, Any]) -> List[str]:
        if self.primary_key:
            key = row[self.primary_key]

            if key is None:
                return []

            if key in self.seen_keys:
                return [f"Duplicate primary key found: {key}"]
            else:
                self.seen_keys.add(key)

        return []