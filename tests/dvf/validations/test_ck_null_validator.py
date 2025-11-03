import unittest
from src.dvf.validations.ck_null_validator import CKNullValidator

class TestCKNullValidator(unittest.TestCase):

    def test_valid_row_multiple_keys(self):
        composite_keys = ["id", "id_2"]
        row = {
            "id": "10",
            "id_2": "10"
        }

        validator = CKNullValidator(composite_keys=composite_keys)
        errors = validator.validate(row)

        self.assertListEqual(errors, [])

    def test_empty_key_multiple_keys(self):
        composite_keys = ["id", "id_2"]
        row = {
            "id": "",
            "id_2": "10"
        }

        validator = CKNullValidator(composite_keys=composite_keys)
        errors = validator.validate(row)

        self.assertEqual(len(errors), 1)
        self.assertIn("is null, empty or missing from the row", errors[0])

    def test_missing_key(self):
        composite_keys = ["id", "id_2"]
        row = {
            "id_2": "10"
        }

        validator = CKNullValidator(composite_keys=composite_keys)
        errors = validator.validate(row)

        self.assertEqual(len(errors), 1)
        self.assertIn("is null, empty or missing from the row", errors[0])

if __name__ == '__main__':
    unittest.main()