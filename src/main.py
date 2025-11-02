import sys
from pathlib import Path
from typing import List
import time 

from src.config.config_loader import ConfigLoader
from src.readers.reader_factory import ReaderFactory
from src.validations.validation_manager import ValidationManager
from src.validations.pk_null_validator import PKNullValidator
from src.validations.pk_duplicates_validator import PKDuplicateValidator
from src.validations.schema_validator import SchemaValidator
from src.utils import parse_args, generate_filename, ValidationReporter

def load_app_config(config_path: Path):
    try:
        return ConfigLoader.load(config_path) 
    except Exception as e:
        print(f"[CONFIG ERROR] -> {e}") 
        sys.exit(1)

def create_data_reader(data_path: Path):
    try:
        return ReaderFactory.create_reader(data_path)
    except Exception as e:
        print(f"[READER ERROR] -> {e}")
        sys.exit(1)

def main():
    start_time = time.perf_counter()
    
    args = parse_args()
    
    if args.save_results is True:
        args.save_results = generate_filename(args.data_file)

    config = load_app_config(Path(args.config_file))
    reader = create_data_reader(Path(args.data_file))

    validators: List = [
        SchemaValidator(schema=config.table_schema),
        PKNullValidator(primary_keys=config.primary_keys),
        PKDuplicateValidator(primary_keys=config.primary_keys)
    ]
    manager = ValidationManager(validators)
    
    total_errors = 0
    total_rows = 0

    try:
        with ValidationReporter(args.save_results) as reporter:
            for i, row in enumerate(reader.read(), start=1):
                total_rows += 1
                errors = manager.validate_row(row)
                
                if errors:
                    total_errors += len(errors)
                    reporter.log_row_error(i, errors)

            reporter.total_errors = total_errors
            reporter.log_success(total_rows)

    except Exception as e:
        print(f"[FILE_SYSTEM_ERROR] | {e}")
        sys.exit(1)

    end_time = time.perf_counter()

    reporter.log_final_summary(total_rows, total_errors)
    
    if args.profile:
        reporter.log_profile(start_time, end_time)

if __name__ == "__main__":
    main()