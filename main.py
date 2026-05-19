import sys
import os
import logging
from CORE import convert, ConverterError, UnsupportedFormatError

def configure_logging():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.INFO)
    stderr_handler.setFormatter(formatter)

    file_handler = logging.FileHandler("converter.log", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    root_logger.addHandler(stderr_handler)
    root_logger.addHandler(file_handler)

def main():
    configure_logging()
    
    if len(sys.argv) < 3:
        print("Usage: python main.py <input_file_path> <target_format>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    target_fmt = sys.argv[2].lower()

    if not os.path.exists(input_file):
        logging.getLogger("CLI").error(f"Target filesystem node does not exist: {input_file}")
        sys.exit(1)

    _, ext = os.path.splitext(input_file)
    source_fmt = ext.lstrip('.').lower()

    supported_extensions = {'json', 'toml', 'yaml', 'html'}
    if source_fmt not in supported_extensions or target_fmt not in supported_extensions:
        err = UnsupportedFormatError(f"Provided extension format context '{source_fmt}' or '{target_fmt}' outside ecosystem range.")
        logging.getLogger("CLI").error(str(err))
        sys.exit(1)

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            raw_data = f.read()

        output_data = convert(raw_data, source_fmt, target_fmt)
        print(output_data)

    except ConverterError as e:
        logging.getLogger("CLI").error(f"Framework runtime error context: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logging.getLogger("CLI").error(f"Unexpected native subsystem failure: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()