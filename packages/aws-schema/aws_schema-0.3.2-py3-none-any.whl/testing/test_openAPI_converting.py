from pathlib import Path
from os.path import dirname, realpath

from testing import load_all


def test_conversion(open_api_schema, tmp_path):
    from aws_schema.openAPI_converter import OpenAPIConverter

    converter = OpenAPIConverter(open_api_schema)

    converter.create_all_schemas(tmp_path)

    expected = load_all(
        f"{dirname(realpath(__file__))}/test_data/api/openAPI_auto_creation"
    )
    actual = load_all(tmp_path)

    expected = {Path(k).name: v for k, v in expected.items()}
    actual = {Path(k).name: v for k, v in actual.items()}

    for file in expected:
        assert actual[file] == expected[file]
