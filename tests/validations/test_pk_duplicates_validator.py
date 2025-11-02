import unittest
from src.validations.pk_duplicates_validator import PKDuplicateValidator

class TestPKDuplicateValidator(unittest.TestCase):
    
    def test_no_duplicates_single_pk(self):
        primary_keys = ["id"]
        row1 = {"id": 1, "name": "Alice"}
        row2 = {"id": 2, "name": "Bob"}

        validator = PKDuplicateValidator(primary_keys=primary_keys)
        errors1 = validator.validate(row1)
        errors2 = validator.validate(row2)
        
        self.assertListEqual(errors1, [])
        self.assertListEqual(errors2, [])

    def test_finds_duplicate_single_pk(self):
        primary_keys = ["id"]
        row1 = {"id": 1, "name": "Alice"}
        row2 = {"id": 1, "name": "Alice_Duplicate"}

        validator = PKDuplicateValidator(primary_keys=primary_keys)
        errors1 = validator.validate(row1) 
        errors2 = validator.validate(row2)
        
        self.assertListEqual(errors1, [])
        self.assertEqual(len(errors2), 1)
        self.assertIn("Duplicate primary key found", errors2[0])

    def test_composite_pk_duplicate(self):
        primary_keys = ["order_id", "item_id"]
        row1 = {"order_id": 100, "item_id": 1, "product": "Apple"}
        row2 = {"order_id": 100, "item_id": 2, "product": "Banana"}
        row3 = {"order_id": 100, "item_id": 1, "product": "Duplicate Apple"}

        validator = PKDuplicateValidator(primary_keys=primary_keys)      
        errors1 = validator.validate(row1)
        errors2 = validator.validate(row2)
        errors3 = validator.validate(row3)
        
        self.assertListEqual(errors1, [])
        self.assertListEqual(errors2, [])
        self.assertEqual(len(errors3), 1)
        self.assertIn("(100, 1)", errors3[0])

    def test_nulls_in_pk_are_not_duplicates(self):
        primary_keys = ["id"]
        row1 = {"id": None, "name": "Alice"}
        row2 = {"id": None, "name": "Bob"}
    
        validator = PKDuplicateValidator(primary_keys=primary_keys)
        errors1 = validator.validate(row1)
        errors2 = validator.validate(row2)
        
        self.assertListEqual(errors1, [])
        self.assertListEqual(errors2, [])

if __name__ == '__main__':
    unittest.main()