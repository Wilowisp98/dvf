import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Optional

def parse_args():
    parser = argparse.ArgumentParser(description="Data validation framework")
    parser.add_argument("--config_file", required=True, help="Path to YAML config file")
    parser.add_argument("--data_file", required=True, help="Path to the input data file (CSV)")
    parser.add_argument(
            "--save_results",
            nargs="?",
            const=True,
            default=None,
            type=Path,
            help=(
                "Save validation results to a file: "
                "If no filename is given, saves to a timestamped file based on the data_file name."
                "If a filename is given, saves to a file with that name."
            )
        )

    parser.add_argument("--profile", action="store_true", help="Enable performance profiling and report peak memory usage")

    return parser.parse_args()

def generate_filename(file_path: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = Path(file_path).stem
    new_filename = f"{base_name}_{timestamp}_results.txt"

    return Path(new_filename)

class ValidationReporter:
    def __init__(self, output_file: Optional[Path]):
        self.output_file = output_file
        self._file_handle = None
        self.total_errors = 0
        
    def __enter__(self):
        if self.output_file:
            try:
                self.output_file.parent.mkdir(parents=True, exist_ok=True)
                self._file_handle = open(self.output_file, 'w', encoding='utf-8')
            except Exception as e:
                raise OSError(f"Could not open output file: {e}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._file_handle:
            self._file_handle.close()
            
    def log_row_error(self, row_num: int, errors: List[str]):
        header = f"[ROW {row_num}] Validation errors:"
        lines = [f"  -> {err}" for err in errors]
        
        if self._file_handle:
            self._file_handle.write(f"{header}\n")
            self._file_handle.writelines([f"{line}\n" for line in lines])
        else:
            print(header)
            for line in lines:
                print(line)
                
    def log_success(self, total_rows: int):
        if self.total_errors == 0 and self._file_handle:
            self._file_handle.write(
                f"Validation successful: {total_rows} rows processed, no errors found.\n"
            )

    def log_final_summary(self, total_rows: int, total_errors: int):
        if total_errors == 0:
            print(f"Validation successful: {total_rows} rows processed, no errors found.")
            if self.output_file:
                print(f"Success report saved to: {self.output_file.resolve()}")
        else:
            print(f"Validation failed: {total_errors} total errors across {total_rows} rows.")
            if self.output_file:
                print(f"Errors saved to: {self.output_file.resolve()}")

    def log_profile(self, start_time: float, end_time: float):
        elapsed_time = end_time - start_time
        
        try:
            import resource
            usage = resource.getrusage(resource.RUSAGE_SELF)
            peak_mb = usage.ru_maxrss / 1024
        except ImportError:
            peak_mb = -1 
        
        print(f"\n--- Performance Profile ---")
        print(f"Total execution time: {elapsed_time:.4f} seconds")
        if peak_mb != -1:
            print(f"Peak memory usage:    {peak_mb:.2f} MB")