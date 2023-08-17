from .openAPI_converter import OpenAPIConverter
import argparse
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument(
    "--openAPI",
    "-o",
    action="store_true",
    help="convert openAPI file to schemas per endpoint and response",
)
parser.add_argument(
    "--file", "-f", help="the input file to read from", default="openapi.yaml"
)
parser.add_argument(
    "--output_directory",
    "-d",
    help="the output directory for the files",
    default="./api",
)

args = parser.parse_args()

if args.openAPI:
    file = Path(args.file)
    if file.suffix == "json":
        from json import load

        with open(file, "r") as f:
            data = load(f)
    else:
        from yaml import safe_load

        with open(file, "r") as f:
            data = safe_load(f)

    OpenAPIConverter(data).create_all_schemas(args.output_directory)
