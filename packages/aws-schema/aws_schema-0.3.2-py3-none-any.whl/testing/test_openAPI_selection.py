from os.path import dirname, realpath

from testing import load_json_file


def test_converter(open_api_schema):
    from aws_schema.openAPI_converter import OpenAPIConverter

    converter = OpenAPIConverter(open_api_schema)

    assert isinstance(converter, OpenAPIConverter)
    assert converter.origin_schema == open_api_schema
    assert converter.validation_schema == dict()


def test_converter_path(open_api_schema):
    from aws_schema.openAPI_converter import OpenAPIConverter, _OpenAPIPath

    converter = OpenAPIConverter(open_api_schema)

    test_path = "/test_request_resource/{path_level1}/{path_level2}"

    path = converter[test_path]

    assert isinstance(path, _OpenAPIPath)
    assert isinstance(path.origin, OpenAPIConverter)
    assert path.path_name == "/test_request_resource/{path_level1}/{path_level2}"
    assert path.origin_schema == open_api_schema["paths"][test_path]
    assert path.methods == dict()


def test_converter_path_method(open_api_schema):
    from aws_schema.openAPI_converter import (
        OpenAPIConverter,
        _OpenAPIPath,
        _OpenAPIMethod,
    )

    converter = OpenAPIConverter(open_api_schema)

    test_path = "/test_request_resource/{path_level1}/{path_level2}"
    test_method = "PUT"

    path = converter[test_path]
    method = converter[test_path][test_method]

    assert isinstance(method, _OpenAPIMethod)
    assert isinstance(method.path, _OpenAPIPath)
    assert isinstance(method.path.origin, OpenAPIConverter)

    assert method.path.path_name == "/test_request_resource/{path_level1}/{path_level2}"
    assert method.path.origin_schema == open_api_schema["paths"][test_path]
    assert (
        len(path.methods) == 1 and list(path.methods.keys())[0] == test_method.lower()
    )

    assert method.method_name == test_method.lower()

    assert (
        method.origin_schema == open_api_schema["paths"][test_path][test_method.lower()]
    )


def test_converter_path_method_response(open_api_schema):
    from aws_schema.openAPI_converter import OpenAPIConverter, _OpenAPIResponses

    converter = OpenAPIConverter(open_api_schema)

    test_path = "/test_request_resource/{path_level1}/{path_level2}"
    test_method = "PUT"

    response_object = converter[test_path][test_method].response

    assert isinstance(response_object, _OpenAPIResponses)
    assert (
        response_object.method.path.path_name
        == "/test_request_resource/{path_level1}/{path_level2}"
    )
    assert (
        response_object.method.path.origin_schema == open_api_schema["paths"][test_path]
    )

    assert (
        response_object.origin_schema
        == open_api_schema["paths"][test_path][test_method.lower()]["responses"]
    )
    assert len(response_object.origin_schema) == 2
    assert set(response_object.origin_schema) == {201, 404}


def test_select_request(open_api_schema, event):
    expected_request_schema = load_json_file(
        f"{dirname(realpath(__file__))}"
        + "/test_data/api/test_request_resource||{path_level1}||{path_level2}-PUT.json"
    )

    from aws_schema.openAPI_converter import OpenAPIConverter

    converter = OpenAPIConverter(open_api_schema)

    assert converter[event["resource"]]["put"].request == expected_request_schema


def test_response201(open_api_schema):
    expected_response_schema = load_json_file(
        f"{dirname(realpath(__file__))}/test_data/response/test_response_resource-PUT-201.json"
    )

    from aws_schema.openAPI_converter import OpenAPIConverter

    response_schema = OpenAPIConverter(open_api_schema)[
        "/test_request_resource/{path_level1}/{path_level2}"
    ]["put"].response[201]

    assert response_schema == expected_response_schema


def test_response404(open_api_schema):
    expected_response_schema = load_json_file(
        f"{dirname(realpath(__file__))}/test_data/response/test_response_resource-PUT-404.json"
    )

    from aws_schema.openAPI_converter import OpenAPIConverter

    response_schema = OpenAPIConverter(open_api_schema)[
        "/test_request_resource/{path_level1}/{path_level2}"
    ]["put"].response[404]

    assert response_schema == expected_response_schema


def test_response_from_string_statusCode(open_api_schema):
    expected_response_schema = load_json_file(
        f"{dirname(realpath(__file__))}/test_data/response/test_response_resource-PUT-404.json"
    )

    from aws_schema.openAPI_converter import OpenAPIConverter

    response_schema = OpenAPIConverter(open_api_schema)[
        "/test_request_resource/{path_level1}/{path_level2}"
    ]["put"].response["404"]

    assert response_schema == expected_response_schema


def test_request_with_reference(open_api_schema):
    expected_request_schema = load_json_file(
        f"{dirname(realpath(__file__))}" + "/test_data/api/test_path_with_ref-POST.json"
    )

    from aws_schema.openAPI_converter import OpenAPIConverter

    request_schema = OpenAPIConverter(open_api_schema)["/test_path_with_ref"][
        "post"
    ].request

    assert request_schema == expected_request_schema


def test_response_with_reference(open_api_schema):
    expected_request_schema = load_json_file(
        f"{dirname(realpath(__file__))}"
        + "/test_data/api/openAPI_auto_creation/test_path_with_ref-POST-200.json"
    )

    from aws_schema.openAPI_converter import OpenAPIConverter

    request_schema = OpenAPIConverter(open_api_schema)["/test_path_with_ref"][
        "post"
    ].response["200"]

    assert request_schema == expected_request_schema
