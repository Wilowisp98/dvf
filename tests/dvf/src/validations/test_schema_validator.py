import unittest
from dvf.src.validations.schema_validator import SchemaValidator

class TestSchemaValidator(unittest.TestCase):
    
    def test_valid_row(self):
        schema = {
            "id": ("int", False),
            "name": ("str", False)
        }
        row = {"id": "123", "name": "Alice"}

        validator = SchemaValidator(schema=schema)
        errors = validator.validate(row)

        self.assertListEqual(errors, [])

    def test_invalid_data_type(self):
        schema = {
            "id": ("int", False)
        }
        row = {"id": "not-a-number"}

        validator = SchemaValidator(schema=schema)
        errors = validator.validate(row)

        self.assertEqual(len(errors), 1)
        self.assertIn("cannot be converted to int", errors[0])

    def test_missing_required_field(self):
        schema = {
            "id": ("int", False)
        }
        row = {"name": "Bob"}

        validator = SchemaValidator(schema=schema)
        errors = validator.validate(row)
        
        self.assertEqual(len(errors), 1)
        self.assertIn("is required but is missing", errors[0])

    def test_missing_optional_field(self):
        schema = {
            "id": ("int", False),
            "notes": ("str", True)
        }
        row = {"id": "123"}

        validator = SchemaValidator(schema=schema)
        errors = validator.validate(row)
        
        self.assertListEqual(errors, [])

if __name__ == '__main__':
    unittest.main()