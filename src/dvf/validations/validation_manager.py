from typing import List, Dict, Any
from src.dvf.validations.base_validator import BaseValidator

class ValidationManager:
    def __init__(self, validators: List[BaseValidator]):
        self.validators = validators

    def validate_row(self, row: Dict[str, Any]) -> List[str]:
        errors = []
        for validator in self.validators:
            errors.extend(validator.validate(row))
        return errors
