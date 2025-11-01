from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Any, Iterator

class BaseReader(ABC):
    def __init__(self, file_path: Path, schema: List[str]):
        self.file_path = file_path
        self.schema = schema

        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")
        
    def _validate_schema(self, file_fields: List[str]) -> None:
        if not self.schema:
            return 
        
        missing_fields = [f for f in self.schema if f not in file_fields]

        if missing_fields:
            raise ValueError(
                f"The following required fields are missing: {', '.join(missing_fields)}"
            )
        
    @abstractmethod
    def read(self) -> Iterator[Dict[str, Any]]:
        pass
