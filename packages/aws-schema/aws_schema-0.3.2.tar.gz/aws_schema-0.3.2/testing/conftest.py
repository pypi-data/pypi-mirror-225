from os.path import dirname, realpath

import yaml
from pytest import fixture

from testing import load_json_file


@fixture
def open_api_schema():
    with open(
        f"{dirname(realpath(__file__))}/test_data/api/openAPI_auto_creation/openapi.yaml",
        "r",
    ) as f:
        return yaml.safe_load(f)


@fixture
def event():
    return load_json_file(
        f"{dirname(realpath(__file__))}/test_data/api/request_aws_http_put_event.json"
    )
