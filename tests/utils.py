import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="File Extension Converter")
    parser.add_argument("--data_file", required=True, help="Path to file being converted")
    parser.add_argument("--format", required=True, help="Extension of the file to be converted to")
    parser.add_argument("--profile", action="store_true", help="Enable performance profiling and report peak memory usage")
    
    return parser.parse_args()