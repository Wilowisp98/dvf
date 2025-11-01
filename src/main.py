import sys
from pathlib import Path
from typing import List
import resource
import time 

from src.config.config_loader import ConfigLoader
from src.readers.reader_factory import ReaderFactory
from src.validations.validation_manager import ValidationManager
from src.validations.pk_null_validator import PKNullValidator
from src.validations.pk_duplicates_validator import PKDuplicateValidator
from src.validations.schema_validator import SchemaValidator
from src.utils import parse_args

def main():
    start_time = time.perf_counter()
    
    args = parse_args()
    config_path = Path(args.config_file)
    data_path = Path(args.data_file)

    try:
        config = ConfigLoader.load(config_path) 
    except Exception as e:
        print(f"[CONFIG ERROR] -> {e}") 
        sys.exit(1)

    try:
        reader = ReaderFactory.create_reader(data_path)
    except Exception as e:
        print(f"[READER ERROR] -> {e}")
        sys.exit(1)

    validators: List = [
        SchemaValidator(schema=config.table_schema),
        PKNullValidator(primary_keys=config.primary_keys),
        PKDuplicateValidator(primary_keys=config.primary_keys)

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
                print(f"  -> {err}")

    end_time = time.perf_counter()

    if total_errors == 0:
        print(f"Validation successful: {total_rows} rows processed, no errors found.")
    else:
        print(f"Validation failed: {total_errors} total errors across {total_rows} rows.")

    if args.profile:
            elapsed_time = end_time - start_time

            usage = resource.getrusage(resource.RUSAGE_SELF)
            peak_mb = usage.ru_maxrss / 1024

            print(f"\n--- Performance Profile ---")
            print(f"Total execution time: {elapsed_time:.4f} seconds")
            print(f"Peak memory usage:    {peak_mb:.2f} MB")

if __name__ == "__main__":
    main()


