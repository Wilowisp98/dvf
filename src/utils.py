import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Data validation framework")
    parser.add_argument("--config_file", required=True, help="Path to YAML config file")
    parser.add_argument("--data_file", required=True, help="Path to the input data file (CSV)")
    parser.add_argument("--profile", action="store_true", help="Enable performance profiling and report peak memory usage")
    return parser.parse_args()