from unittest import TestCase
from os.path import dirname, realpath
from os import getcwd, chdir

from testing import load_json_file


class TestAPIValidation(TestCase):
    def test_basic_with_schema_file(self):
        from aws_schema.api_validation import (
            APIDataValidator,
        )

        api_schema_file = (
            f"{dirname(realpath(__file__))}/test_data/api/test_request_resource.json"
        )
        api_data = load_json_file(
            f"{dirname(realpath(__file__))}/test_data/api/request_basic.json"
        )
        APIDataValidator(
            file=api_schema_file, api_data=api_data, api_name="test_request_resource"
        )

    def test_basic_with_schema_file_including_http_method(self):
        from aws_schema.api_validation import (
            APIDataValidator,
        )

        api_schema_file = f"{dirname(realpath(__file__))}/test_data/api/test_request_resource-POST.json"
        api_data = load_json_file(
            f"{dirname(realpath(__file__))}/test_data/api/request_basic.json"
        )
        APIDataValidator(
            file=api_schema_file, api_data=api_data, api_name="test_request_resource"
        )

    def test_basic_with_schema_directory(self):
        from aws_schema.api_validation import (
            APIDataValidator,
        )

        api_schema_directory = f"{dirname(realpath(__file__))}/test_data/api/"
        api_data = load_json_file(
            f"{dirname(realpath(__file__))}/test_data/api/request_basic.json"
        )

        def api_basic():
            APIDataValidator(
                file=api_schema_directory,
                api_data=api_data,
                api_name="test_request_resource",
            )

        api_basic()

    def test_basic_with_relative_schema_file(self):
        from aws_schema.api_validation import (
            APIDataValidator,
        )

        actual_cwd = getcwd()
        try:
            chdir(dirname(realpath(__file__)))

            api_schema_file = "./test_data/api/test_request_resource.json"
            api_data = load_json_file("./test_data/api/request_basic.json")

            APIDataValidator(
                file=api_schema_file,
                api_data=api_data,
                api_name="test_request_resource",
            )
        finally:
            chdir(actual_cwd)

    def test_basic_with_relative_schema_directory(self):
        from aws_schema.api_validation import (
            APIDataValidator,
        )

        actual_cwd = getcwd()
        try:
            chdir(dirname(realpath(__file__)))
            api_schema_directory = "./test_data/api/"
            api_data = load_json_file("./test_data/api/request_basic.json")

            def api_basic():
                APIDataValidator(
                    file=api_schema_directory,
                    api_data=api_data,
                    api_name="test_request_resource",
                )

            api_basic()
        finally:
            chdir(actual_cwd)

    def test_basic_with_wrong_httpMethod(self):
        from aws_schema.api_validation import (
            APIDataValidator,
        )

        api_schema_file = (
            f"{dirname(realpath(__file__))}/test_data/api/test_request_resource.json"
        )
        api_data = load_json_file(
            f"{dirname(realpath(__file__))}/test_data/api/request_basic.json"
        )
        api_data["httpMethod"] = "WRONG"

        with self.assertRaises(NotImplementedError) as TE:
            APIDataValidator(
                file=api_schema_file,
                api_data=api_data,
                api_name="test_request_resource",
            )

        self.assertEqual(
            {
                "statusCode": 501,
                "body": "API is not defined",
                "headers": {"Content-Type": "text/plain"},
            },
            TE.exception.args[0],
        )

    def test_basic_with_missing_body(self):
        from aws_schema.api_validation import (
            APIDataValidator,
        )

        api_schema_file = (
            f"{dirname(realpath(__file__))}/test_data/api/test_request_resource.json"
        )
        api_data = load_json_file(
            f"{dirname(realpath(__file__))}/test_data/api/request_basic.json"
        )
        api_data["body"] = None

        with self.assertRaises(TypeError) as TE:
            APIDataValidator(
                file=api_schema_file,
                api_data=api_data,
                api_name="test_request_resource",
            )

        self.assertEqual(
            {
                "statusCode": 400,
                "body": "'body' is a required property",
                "headers": {"Content-Type": "text/plain"},
            },
            TE.exception.args[0],
        )

    def test_basic_with_wrong_body(self):
        from aws_schema.api_validation import (
            APIDataValidator,
        )

        api_schema_file = (
            f"{dirname(realpath(__file__))}/test_data/api/test_request_resource.json"
        )
        api_data = load_json_file(
            f"{dirname(realpath(__file__))}/test_data/api/request_basic.json"
        )

        api_data["body"]["body_key1"] = 123

        with self.assertRaises(TypeError) as TE:
            APIDataValidator(
                file=api_schema_file,
                api_data=api_data,
                api_name="test_request_resource",
            )

        self.assertEqual(
            {
                "statusCode": 400,
                "body": "123 is not of type 'string'\n\n"
                        "Failed validating 'type' in "
                        "schema['properties']['body']['properties']['body_key1']:\n"
                        "    {'description': 'containing only a string', 'type': 'string'}\n\n"
                        "On instance['body']['body_key1']:\n"
                        "    123",
                "headers": {"Content-Type": "text/plain"},
            },
            TE.exception.args[0],
        )

    def test_basic_with_missing_path_parameter(self):
        from aws_schema.api_validation import (
            APIDataValidator,
        )

        api_schema_file = (
            f"{dirname(realpath(__file__))}/test_data/api/test_request_resource.json"
        )
        api_data = load_json_file(
            f"{dirname(realpath(__file__))}/test_data/api/request_basic.json"
        )
        api_data.pop("pathParameters")

        with self.assertRaises(TypeError) as TE:
            APIDataValidator(
                file=api_schema_file,
                api_data=api_data,
                api_name="test_request_resource",
            )

        self.assertEqual(
            {
                "statusCode": 400,
                "body": "'pathParameters' is a required property",
                "headers": {"Content-Type": "text/plain"},
            },
            TE.exception.args[0],
        )

    def test_complete_aws_rest_event_data(self):
        from aws_schema.api_validation import (
            APIDataValidator,
        )

        api_schema_file = (
            f"{dirname(realpath(__file__))}/test_data/api/test_request_resource.json"
        )
        api_data = load_json_file(
            f"{dirname(realpath(__file__))}/test_data/api/request_aws_http_event.json"
        )
        APIDataValidator(
            file=api_schema_file, api_data=api_data, api_name="test_request_resource"
        )

    def test_non_rest_event(self):
        from aws_schema.api_validation import (
            APIDataValidator,
        )

        api_schema_file = f"{dirname(realpath(__file__))}/test_data/api/api_basic.json"
        api_data = {"body_key1": "some_string", "body_key2": {"key2.1": 2}}
        APIDataValidator(file=api_schema_file, api_data=api_data, api_name="api_basic")

        api_data = {"body_key1": "some_string", "body_key2": 2}
        with self.assertRaises(TypeError):
            APIDataValidator(
                file=api_schema_file, api_data=api_data, api_name="api_basic"
            )

    def test_url_nested_path(self):
        from aws_schema.api_validation import (
            APIDataValidator,
        )

        api_schema_directory = f"{dirname(realpath(__file__))}/test_data/api/"
        api_data = {"httpMethod": "POST", "body": {"key_1": "some_string"}}

        APIDataValidator(
            file=api_schema_directory,
            api_data=api_data,
            api_name="/test_request_resource/specific_resource",
        )

    def test_url_nested_path_variables(self):
        from aws_schema.api_validation import (
            APIDataValidator,
        )

        api_schema_directory = f"{dirname(realpath(__file__))}/test_data/api/"
        api_data = {
            "httpMethod": "PUT",
            "body": {"body_key1": "some_string"},
            "headers": {"content-type": "application/json"},
            "pathParameters": {
                "path_level1": "path_value1",
                "path_level2": "path_value",
            },
            "multiValueQueryStringParameters": {
                "key1": ["some string"],
                "key2": ["another string"],
            },
        }

        APIDataValidator(
            file=api_schema_directory,
            api_data=api_data,
            api_name="/test_request_resource/{path_level1}/{path_level2}",
        )

    def test_basic_with_parameter_casting(self):
        from aws_schema.api_validation import (
            APIDataValidator,
        )

        api_schema_file = f"{dirname(realpath(__file__))}/test_data/api/test_request_resource_parsing_params.json"
        api_data = load_json_file(
            f"{dirname(realpath(__file__))}/test_data/api/request_basic_for_parsing_params.json"
        )
        APIDataValidator(
            file=api_schema_file, api_data=api_data, api_name="test_request_resource"
        )

    def test_basic_with_parameter_casting_wrong_value(self):
        from aws_schema.api_validation import (
            APIDataValidator,
        )

        api_schema_file = f"{dirname(realpath(__file__))}/test_data/api/test_request_resource_parsing_params.json"
        api_data = load_json_file(
            f"{dirname(realpath(__file__))}/test_data/api/request_basic_for_parsing_params.json"
        )

        api_data["pathParameters"]["path_level1"] = "1,25"

        with self.assertRaises(TypeError) as TE:
            APIDataValidator(
                file=api_schema_file,
                api_data=api_data,
                api_name="test_request_resource",
            )

        self.assertEqual(
            {
                "statusCode": 400,
                "body": "'1,25' is not of type 'number'\n\nFailed validating 'type' in "
                        "schema['properties']['pathParameters']['properties']['path_level1']:\n"
                        "    {'description': 'key name as specified in endpoint config, first level',\n"
                        "     'type': 'number'}\n\n"
                        "On instance['pathParameters']['path_level1']:\n"
                        "    '1,25'",
                "headers": {"Content-Type": "text/plain"},
            },
            TE.exception.args[0],
        )

    def test_basic_with_parameter_casting_wrong_keys(self):
        from aws_schema.api_validation import (
            APIDataValidator,
        )

        api_schema_file = f"{dirname(realpath(__file__))}/test_data/api/test_request_resource_parsing_params.json"
        api_data = load_json_file(
            f"{dirname(realpath(__file__))}/test_data/api/request_basic_for_parsing_params.json"
        )

        api_data["multiValueQueryStringParameters"]["unknown_key"] = ["125"]

        with self.assertRaises(TypeError) as TE:
            APIDataValidator(
                file=api_schema_file,
                api_data=api_data,
                api_name="test_request_resource",
            )

        self.assertEqual(
            {
                "statusCode": 400,
                "body": "Additional properties are not allowed ('unknown_key' was unexpected) in queryParameters",
                "headers": {"Content-Type": "text/plain"},
            },
            TE.exception.args[0],
        )

    def test_x_www_form_url_parameter_casting(self):
        from aws_schema.api_validation import (
            APIDataValidator,
        )

        api_schema_file = (
                str(dirname(realpath(__file__))) +
                "/test_data/api/test_request_resource_parsing_x_www_form_urlencoded_params-POST.json"
        )
        api_data = load_json_file(
            str(dirname(realpath(__file__))) +
            "/test_data/api/request_resource_for_parsing_x_www_form_urlencoded_params.json"
        )
        parsed_data = APIDataValidator(
            file=api_schema_file, api_data=api_data, api_name="test_request_resource"
        ).data

        assert parsed_data["body"] == {
            "type_string_key": ["some_string"],
            "type_list_of_strings_key": [["abc", "0123"]],
            "type_object_key": [{"sub_key3.1": "02", "sub_key3.2": 2}],
            "type_list_of_numbers_key": [[2.34, 45.6]],
            "double_query_key": [2, 4],
        }
