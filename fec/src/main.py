import sys
from pathlib import Path
import time 

from fec.src.utils import parse_args
from utils.readers.reader_factory import ReaderFactory
from fec.src.writers.writer_factory import WriterFactory

def create_data_reader(data_path: Path):
    try:
        return ReaderFactory.create_reader(data_path)
    except Exception as e:
        print(f"[READER ERROR] -> {e}")
        sys.exit(1)

def create_data_writer(file_name: str, file_format: str):
    try:
        return WriterFactory.create_writer(file_name=file_name, file_format=file_format)
    except Exception as e:
        print(f"[WRITER ERROR] -> {e}")
        sys.exit(1)

def main():
    start_time = time.perf_counter()
    
    args = parse_args()
    input_path = Path(args.data_file)

    output_name = f"{input_path.stem}_converted{args.format}"
    output_path = input_path.with_name(output_name)

    reader = create_data_reader(input_path)
    writer = create_data_writer(file_name=str(output_path), file_format=args.format)

    try:
        print(f"Processing {input_path} -> {output_path}")
        for i, batch in enumerate(reader.read_batches(), start=1): 
            writer.write(batch)

        print(f"\nSuccessfully processed {i} batches.")

    except Exception as e:
        print(f"\n[FILE_SYSTEM_ERROR] | {e}")
        sys.exit(1)
    finally:
        if writer:
            writer.close()
            print(f"File closed: {output_path}")

    end_time = time.perf_counter()
    
    if args.profile:
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