import csv
from typing import Any, Dict, List

from fec.src.writers.base_writer import BaseWriter

class CSVWriter(BaseWriter):
    def __init__(self, file_name: str):
        super().__init__(file_name)
        self.file = None
        self.writer = None
        self.fieldnames = None

    def write(self, batch: List[Dict[str, Any]]) -> None:
        if self.writer is None:
            self.fieldnames = list(batch[0].keys())
            
            try:
                self.file = open(self.file_name, mode="w", newline="", encoding="utf-8")
                self.writer = csv.DictWriter(self.file, fieldnames=self.fieldnames)
                self.writer.writeheader()
            except Exception as e:
                print(f"Error opening or writing header to file {self.file_name}: {e}")
                if self.file:
                    self.file.close()
                self.file = None
                return

        self.writer.writerows(batch)

    def close(self) -> None:
        if self.file:
            self.file.close()
            self.file = None
            self.writer = None