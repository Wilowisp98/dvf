import pyarrow.parquet as pq
from pathlib import Path
from typing import Any, Dict, Iterator

from src.dvf.readers.base_reader import BaseReader

class ParquetReader(BaseReader):
    def __init__(self, file_path: Path, batch_size: int = 5000):
        super().__init__(file_path)
        self.reader_schema = None
        self.batch_size = batch_size

    def read(self) -> Iterator[Dict[str, Any]]:
        parquet_file = pq.ParquetFile(self.file_path)
        self.reader_schema = parquet_file.schema.names
        
        for batch in parquet_file.iter_batches(batch_size=self.batch_size):
            column_names = batch.schema.names

            for i in range(len(batch)):
                row_dict = {name: batch.column(name)[i].as_py() for name in column_names}
                yield row_dict