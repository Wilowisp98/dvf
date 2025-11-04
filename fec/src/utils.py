import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="File Extension Converter")
    parser.add_argument("--file", required=True, help="Path to file being converted")
    parser.add_argument("--format", required=True, help="Extension of the file to be converted to")

    return parser.parse_args()