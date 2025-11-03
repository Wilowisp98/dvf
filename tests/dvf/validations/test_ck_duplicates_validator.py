import unittest
from src.dvf.validations.ck_duplicates_validator import CKDuplicateValidator

class TestCKDuplicateValidator(unittest.TestCase):
    
    def test_no_duplicates_single_ck(self):
        composite_keys = ["id", "id_2"]
        row1 = {"id": 1, "id_2": 1, "name": "Alice"}
        row2 = {"id": 2, "id_2": 2, "name": "Bob"}

        validator = CKDuplicateValidator(composite_keys=composite_keys)
        errors1 = validator.validate(row1)
        errors2 = validator.validate(row2)
        
        self.assertListEqual(errors1, [])
        self.assertListEqual(errors2, [])

    def test_composite_ck_duplicate(self):
        composite_keys = ["order_id", "item_id"]
        row1 = {"order_id": 100, "item_id": 1, "product": "Apple"}
        row2 = {"order_id": 100, "item_id": 2, "product": "Banana"}
        row3 = {"order_id": 100, "item_id": 1, "product": "Duplicate Apple"}

        validator = CKDuplicateValidator(composite_keys=composite_keys)      
        errors1 = validator.validate(row1)
        errors2 = validator.validate(row2)
        errors3 = validator.validate(row3)
        
        self.assertListEqual(errors1, [])
        self.assertListEqual(errors2, [])
        self.assertEqual(len(errors3), 1)
        self.assertIn("(100, 1)", errors3[0])

    def test_nulls_in_ck_are_not_duplicates(self):
        composite_keys = ["id", "id_2"]
        row1 = {"id": None, "id_2": 1, "name": "Alice"}
        row2 = {"id": None, "id_2": 2, "name": "Bob"}
    
        validator = CKDuplicateValidator(composite_keys=composite_keys)
        errors1 = validator.validate(row1)
        errors2 = validator.validate(row2)
        
        self.assertListEqual(errors1, [])
        self.assertListEqual(errors2, [])

if __name__ == '__main__':
    unittest.main()