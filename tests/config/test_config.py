import unittest
from pathlib import Path

from pydantic import ValidationError

from src.config.config_loader import ConfigLoader
from src.config.config_loader import Config

class TestConfig(unittest.TestCase):

    def test_valid_config(self):
        path = Path("tests/config/test_files/test_config_1.yaml")

        config = ConfigLoader.load(config_path=path)

        self.assertIsInstance(config, Config)

    def test_file_not_found(self):
        non_existent_path = Path("this/path/does/not/exist.csv")

        with self.assertRaises(FileNotFoundError):
            _ = ConfigLoader.load(config_path=non_existent_path)

    def test_not_yaml_file(self):
        path = Path("tests/config/test_files/test_config_2.json")

        with self.assertRaises(ValueError):
            _ = ConfigLoader.load(config_path=path)

    def test_valid_config_empty(self):
        data = {}
        
        config = Config(**data)
        
        self.assertIsNone(config.table_schema)
        self.assertIsNone(config.primary_key)
        self.assertIsNone(config.composite_keys)

    def test_extra_fields_forbidden(self):
        data = {
            "primary_keys": ["id", "id_2"],
            "an_unknown_field": "some_value"
        }
        
        with self.assertRaises(ValidationError) as context:
            Config(**data)
        
        self.assertIn("Extra inputs are not permitted", str(context.exception))

    def test_pydantic_invalid_pk_type(self):
        data = {"composite_keys": "not-a-list"}
        
        with self.assertRaises(ValidationError) as context:
            Config(**data)
            
        self.assertIn("Input should be a valid list", str(context.exception))

    def test_pydantic_invalid_schema_type(self):
        data = {"table_schema": ["not-a-dict"]}
        
        with self.assertRaises(ValidationError) as context:
            Config(**data)
            
        self.assertIn("Input should be a valid dictionary", str(context.exception))

    def test_pydantic_invalid_schema_tuple_structure(self):
        data = {"table_schema": {"id": ("int", "not-a-bool")}}
        
        with self.assertRaises(ValidationError) as context:
            Config(**data)
            
        self.assertIn("Input should be a valid boolean", str(context.exception))

    def test_custom_validator_invalid_data_type(self):
        data = {"table_schema": {"id": ("date", False)}}
        
        with self.assertRaises(ValidationError) as context:
            Config(**data)
        
        self.assertIn("Invalid data type 'date' for column 'id'", str(context.exception))

if __name__ == '__main__':
    unittest.main()