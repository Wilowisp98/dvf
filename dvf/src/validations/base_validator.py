from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseValidator(ABC):
    @abstractmethod
    def validate(self, row: Dict[str, Any]) -> List[str]:
        pass