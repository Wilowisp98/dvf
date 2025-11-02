import unittest
from pathlib import Path

from src.readers.csv_reader import CSVReader

class TestCSVReader(unittest.TestCase):

    def test_read_valid_csv(self):
        path = Path("tests/readers/test_files/test_file_1.csv")

        reader = CSVReader(path)
        rows = list(reader.read()) 
        
        self.assertEqual(len(rows), 1)
        expected_rows = [
            {"id": "1", "name": "John Doe", "age": "32", "country": "USA"}
        ]

        self.assertListEqual(rows, expected_rows)

    def test_read_headers_only_csv(self):
        path = Path("tests/readers/test_files/test_file_4.csv")

        reader = CSVReader(path)
        rows = list(reader.read())
        
        self.assertListEqual(rows, [])

    def test_read_empty_file_raises_value_error(self):
        path = Path("tests/readers/test_files/test_file_5.csv")
        
        with self.assertRaises(ValueError) as context:
            reader = CSVReader(path)
            list(reader.read())
        
        self.assertIn("No headers found in CSV file", str(context.exception))

    def test_read_nonexistent_file_raises_file_not_found(self):
        non_existent_path = Path("this/path/does/not/exist.csv")
        
        with self.assertRaises(FileNotFoundError):
            _ = CSVReader(non_existent_path)

if __name__ == '__main__':
    unittest.main()