import sys
from pathlib import Path
from typing import List

from src.config.config_loader import load_config
from src.readers.reader_factory import ReaderFactory
from src.validations.validation_manager import ValidationManager
from src.validations.pk_null_validator import PKNullValidator
from src.utils import parse_args

def main():
    args = parse_args()

    config_path = Path(args.config_file)
    data_path = Path(args.data_file)

    try:
        config = load_config(config_path)
    except Exception as e:
        print(f"[CONFIG ERROR] | {e}")
        sys.exit(1)

    try:
        reader = ReaderFactory.create_reader(data_path, schema=list(config.schema.keys()))
    except Exception as e:
        print(f"[READER ERROR] | {e}")
        sys.exit(1)

    validators: List = [
        PKNullValidator(primary_keys=config.primary_keys),
    ]
    manager = ValidationManager(validators)

    total_errors = 0
    total_rows = 0

    for i, row in enumerate(reader.read(), start=1):
        total_rows += 1
        errors = manager.validate_row(row)
        if errors:
            total_errors += len(errors)
            print(f"[ROW {i}] Validation errors:")
            for err in errors:
                print(f"  - {err}")

    if total_errors == 0:
        print(f"Validation successful: {total_rows} rows processed, no errors found.")
    else:
        print(f"Validation failed: {total_errors} total errors across {total_rows} rows.")

if __name__ == "__main__":
    main()


