import unittest
from src.validations.pk_null_validator import PKNullValidator

class TestPKNullValidator(unittest.TestCase):

    def test_valid_row(self):
        primary_keys = ["id"]
        row = {
            "id": "10"
        }

        validator = PKNullValidator(primary_keys=primary_keys)
        errors = validator.validate(row)

        self.assertListEqual(errors, [])

    def test_valid_row_multiple_keys(self):
        primary_keys = ["id", "id_2"]
        row = {
            "id": "10",
            "id_2": "10"
        }

        validator = PKNullValidator(primary_keys=primary_keys)
        errors = validator.validate(row)

        self.assertListEqual(errors, [])

    def test_empty_key(self):
        primary_keys = ["id"]
        row = {
            "id": "",
        }

        validator = PKNullValidator(primary_keys=primary_keys)
        errors = validator.validate(row)

        self.assertEqual(len(errors), 1)
        self.assertIn("is null, empty or missing from the row", errors[0])

    def test_empty_key_multiple_keys(self):
        primary_keys = ["id", "id_2"]
        row = {
            "id": "",
            "id_2": "10"
        }

        validator = PKNullValidator(primary_keys=primary_keys)
        errors = validator.validate(row)

        self.assertEqual(len(errors), 1)
        self.assertIn("is null, empty or missing from the row", errors[0])

    def test_missing_key(self):
        primary_keys = ["id"]
        row = {
        }

        validator = PKNullValidator(primary_keys=primary_keys)
        errors = validator.validate(row)

        self.assertEqual(len(errors), 1)
        self.assertIn("is null, empty or missing from the row", errors[0])

if __name__ == '__main__':
    unittest.main()