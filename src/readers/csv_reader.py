import csv
from pathlib import Path
from typing import Any, Dict, Iterator

from src.readers.base_reader import BaseReader

class CSVReader(BaseReader):
    def __init__(self, file_path: Path):
        super().__init__(file_path)
        self.reader_schema = None # In case it's ever needed.

    def read(self) -> Iterator[Dict[str, Any]]:
        with open(self.file_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames:
                raise ValueError(f"No headers found in CSV file: {self.file_path}")
        
            self.reader_schema = reader.fieldnames
            
            for row in reader:
                yield row
