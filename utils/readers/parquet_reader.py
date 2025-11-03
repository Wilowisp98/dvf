import pyarrow.parquet as pq
from pathlib import Path
from typing import Any, Dict, Iterator, List

from utils.readers.base_reader import BaseReader

class ParquetReader(BaseReader):
    def __init__(self, file_path: Path, batch_size: int = 5000):
        super().__init__(file_path)
        self.reader_schema = None
        self.batch_size = batch_size

    def get_schema(self, file: Any) -> None:
        if self.reader_schema is None:
            self.reader_schema = file.schema.names

    def read(self) -> Iterator[Dict[str, Any]]:
        parquet_file = pq.ParquetFile(self.file_path)
        self.get_schema(parquet_file)
        
        for batch in parquet_file.iter_batches(batch_size=self.batch_size):
            for i in range(len(batch)):
                row_dict = {name: batch.column(name)[i].as_py() for name in self.reader_schema}
                yield row_dict

    def read_batches(self) -> Iterator[List[Dict[str, Any]]]:
        parquet_file = pq.ParquetFile(self.file_path)
        self.get_schema(parquet_file)
        
        for batch in parquet_file.iter_batches(batch_size=self.batch_size):
            yield batch.to_pylist()