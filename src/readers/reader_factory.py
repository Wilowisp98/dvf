from pathlib import Path
from typing import List, Optional

from src.readers.csv_reader import CSVReader
from src.readers.base_reader import BaseReader

class ReaderFactory:
    _readers = {
        ".csv": CSVReader
    }

    @classmethod
    def create_reader(cls, file_path: Path, schema: Optional[List[str]] = None) -> BaseReader:
        extension = file_path.suffix.lower()

        if extension not in cls._readers:
            raise ValueError(
                f"Unsupported file extension: {extension}.\n"
                f"Supported file extensions: {', '.join(cls.readers.keys())}"
            )
        
        reader_class = cls._readers[extension]
        return reader_class(file_path, schema)