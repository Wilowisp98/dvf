import csv
from pathlib import Path
from typing import Any, Dict, Iterator, List
import itertools

from utils.readers.base_reader import BaseReader

class CSVReader(BaseReader):
    def __init__(self, file_path: Path, batch_size: int = 500):
        super().__init__(file_path)
        self.reader_schema = None
        self.batch_size = batch_size

    def get_schema(self, file: Any):
        if self.reader_schema is None:
            self.reader_schema = file.fieldnames

    def read(self) -> Iterator[Dict[str, Any]]:
        with open(self.file_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            self.get_schema(reader)

            if not self.reader_schema:
                raise ValueError(f"No headers found in CSV file: {self.file_path}")
            
            for row in reader:
                yield row

    def read_batches(self) -> Iterator[List[Dict[str, Any]]]:
        with open(self.file_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            self.get_schema(reader)

            if not self.reader_schema:
                raise ValueError(f"No headers found in CSV file: {self.file_path}")
            
            while True:
                batch = list(itertools.islice(reader, self.batch_size))
                if not batch:
                    break
                yield batch