from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseWriter(ABC):
    def __init__(self, file_name: str):
        self.file_name = file_name

    @abstractmethod
    def write(self, batch: List[Dict[str, Any]]) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass