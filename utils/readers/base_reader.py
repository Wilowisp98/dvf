from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, Iterator, List

class BaseReader(ABC):
    def __init__(self, file_path: Path):
        self.file_path = file_path

        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")
        
    @abstractmethod
    def read(self) -> Iterator[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def read_batches(self) -> Iterator[List[Dict[str, Any]]]:
        pass

    @abstractmethod
    def get_schema(self, file: Any) -> None:
        pass