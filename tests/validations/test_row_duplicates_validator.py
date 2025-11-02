import unittest
from src.validations.row_duplicates_validator import RowDuplicateValidator

class TestRowDuplicateValidator(unittest.TestCase):
    
    def test_no_duplicates(self):
        row1 = {"id": 1, "name": "Alice"}
        row2 = {"id": 2, "name": "Bob"}

        validator = RowDuplicateValidator()   
        errors1 = validator.validate(row1)
        errors2 = validator.validate(row2)
        
        self.assertListEqual(errors1, [])
        self.assertListEqual(errors2, [])

    def test_simple_duplicate_identical_order(self):
        row1 = {"id": 1, "name": "Alice"}
        row2 = {"id": 1, "name": "Alice"}
        
        validator = RowDuplicateValidator()
        errors1 = validator.validate(row1)
        errors2 = validator.validate(row2)
        
        self.assertListEqual(errors1, [])
        self.assertEqual(len(errors2), 1)
        self.assertIn("Duplicate row found", errors2[0])

if __name__ == '__main__':
    unittest.main()