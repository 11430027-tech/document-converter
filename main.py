import sys
import os
from CORE import convert, ConverterError
import converter

def main():
    if len(sys.argv) < 4:
        print("Usage: python main.py <input_file> <source_fmt> <target_fmt> [output_file]")
        sys.exit(1)

    input_file = sys.argv[1]
    source_fmt = sys.argv[2]
    target_fmt = sys.argv[3]
    output_file = sys.argv[4] if len(sys.argv) > 4 else None

    if not os.path.exists(input_file):
        print(f"[ERROR] Input file not found: {input_file}")
        sys.exit(1)

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            input_data = f.read()

        output_data = convert(input_data, source_fmt, target_fmt)

        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(output_data)
            print(f"[INFO] Successfully saved output to {output_file}")
        else:
            print(output_data)

    except ConverterError as e:
        print(f"[ERROR] Conversion chain failed: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Unexpected error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()