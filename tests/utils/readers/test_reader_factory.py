import unittest
from pathlib import Path

from utils.readers.reader_factory import ReaderFactory
from utils.readers.csv_reader import CSVReader

class TestReaderFactory(unittest.TestCase):

    def test_valid_extension_returns_csv_reader(self):
        path = Path("tests/utils/readers/test_files/test_file_1.csv")
        
        reader = ReaderFactory.create_reader(file_path=path)
        
        self.assertIsInstance(reader, CSVReader)

    def test_invalid_extension_raises_value_error(self):
        path = Path("tests/utils/readers/test_files/test_file_2.json")
        
        with self.assertRaises(ValueError):
            ReaderFactory.create_reader(file_path=path)

    def test_uppercase_extension_is_handled(self):
        path = Path("tests/utils/readers/test_files/test_file_3.CSV")
        
        reader = ReaderFactory.create_reader(file_path=path)
        
        self.assertIsInstance(reader, CSVReader)

if __name__ == '__main__':
    unittest.main()