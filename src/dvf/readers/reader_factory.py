from pathlib import Path

from src.dvf.readers.parquet_reader import ParquetReader
from src.dvf.readers.csv_reader import CSVReader
from src.dvf.readers.base_reader import BaseReader

class ReaderFactory:
    _readers = {
        ".csv": CSVReader,
        ".parquet": ParquetReader
    }

    @classmethod
    def create_reader(cls, file_path: Path) -> BaseReader:
        extension = file_path.suffix.lower()

        if extension not in cls._readers:
            raise ValueError(
                f"Unsupported file extension: {extension}.\n"
                f"Supported file extensions: {', '.join(cls._readers.keys())}"
            )
        
        reader_class = cls._readers[extension]
        return reader_class(file_path)