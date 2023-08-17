def test_request_translation_get():
    open_api_path = "test_path"
    open_api_method = "get"
    open_api_request = {
        "summary": "Test API",
        "description": "some description",
        "operationId": "operationID",
        "parameters": [
            {
                "in": "query",
                "name": "string_value",
                "schema": {"type": "string"},
                "required": True,
            }
        ],
    }

    json_schema_request = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "test_path-GET",
        "description": "Test API\n---\nsome description",
        "type": "object",
        "additionalProperties": True,
        "properties": {
            "httpMethod": {
                "const": "GET",
                "description": "the ReST method(s) type allowed " "for this API",
                "type": "string",
            },
            "headers": {
                "type": "object",
                "additionalProperties": True,
                "properties": {},
                "required": list(),
            },
            "body": {
                "type": "object",
                "additionalProperties": False,
                "properties": dict(),
                "required": list(),
            },
            "pathParameters": {
                "additionalProperties": False,
                "properties": {},
                "required": [],
                "type": "object",
            },
            "queryParameters": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "string_value": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["string_value"],
            },
        },
        "required": ["headers", "httpMethod", "queryParameters"],
    }

    from aws_schema.openAPI_converter import _convert_request

    assert (
        _convert_request(
            open_api_path, open_api_method, open_api_request, {"info": dict()}
        )
        == json_schema_request
    )


def test_request_translation_post():
    open_api_path = "test_request_resource"
    open_api_method = "post"
    open_api_request = {
        "summary": "Test API",
        "description": "some description",
        "operationId": "operationID",
        "parameters": [
            {
                "in": "path",
                "name": "path_level1",
                "schema": {"type": "string"},
                "required": True,
                "description": "parameter description",
            },
            {
                "in": "path",
                "name": "path_level2",
                "required": True,
                "description": "parameter description",
                "schema": {"type": "string"},
            },
            {
                "in": "query",
                "name": "key1",
                "schema": {"type": "string"},
                "required": True,
            },
            {
                "in": "query",
                "name": "key2",
                "description": "some description",
                "schema": {"type": "integer"},
            },
            {"in": "header", "name": "isBase64Encoded", "schema": {"type": "boolean"}},
        ],
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "body_key1": {"type": "string"},
                            "body_key2": {
                                "type": "object",
                                "description": "some description",
                            },
                        },
                        "required": ["body_key1"],
                    }
                }
            },
        },
    }

    json_schema_request = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "test_request_resource-POST",
        "description": "Test API\n---\nsome description",
        "type": "object",
        "additionalProperties": True,
        "properties": {
            "httpMethod": {
                "const": "POST",
                "description": "the ReST method(s) type allowed " "for this API",
                "type": "string",
            },
            "headers": {
                "type": "object",
                "additionalProperties": True,
                "properties": {
                    "content-type": {"type": "string", "enum": ["application/json"]},
                    "isBase64Encoded": {"type": "boolean"},
                },
                "required": ["content-type"],
            },
            "body": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "body_key1": {"type": "string"},
                    "body_key2": {"type": "object", "description": "some description"},
                },
                "required": ["body_key1"],
            },
            "pathParameters": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "path_level1": {
                        "type": "string",
                        "description": "parameter description",
                    },
                    "path_level2": {
                        "type": "string",
                        "description": "parameter description",
                    },
                },
                "required": ["path_level1", "path_level2"],
            },
            "queryParameters": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "key1": {"items": {"type": "string"}, "type": "array"},
                    "key2": {
                        "items": {"type": "integer"},
                        "type": "array",
                        "description": "some description",
                    },
                },
                "required": ["key1"],
            },
        },
        "required": [
            "body",
            "headers",
            "httpMethod",
            "pathParameters",
            "queryParameters",
        ],
    }

    from aws_schema.openAPI_converter import _convert_request

    assert (
        _convert_request(
            open_api_path, open_api_method, open_api_request, {"info": dict()}
        )
        == json_schema_request
    )


def test_request_translation_post_no_requires():
    open_api_path = "test_request_resource"
    open_api_method = "post"
    open_api_request = {
        "summary": "Test API",
        "description": "some description",
        "operationId": "operationID",
        "parameters": [
            {
                "in": "path",
                "name": "path_level1",
                "schema": {"type": "string"},
                "required": True,
                "description": "parameter description",
            },
            {
                "in": "path",
                "name": "path_level2",
                "description": "parameter description",
                "schema": {"type": "string"},
            },
            {"in": "query", "name": "key1", "schema": {"type": "string"}},
            {
                "in": "query",
                "name": "key2",
                "description": "some description",
                "schema": {"type": "integer"},
            },
            {"in": "header", "name": "isBase64Encoded", "schema": {"type": "boolean"}},
        ],
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "body_key1": {"type": "string"},
                            "body_key2": {
                                "type": "object",
                                "description": "some description",
                            },
                        },
                    }
                }
            }
        },
    }

    json_schema_request = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "test_request_resource-POST",
        "description": "Test API\n---\nsome description",
        "type": "object",
        "additionalProperties": True,
        "properties": {
            "httpMethod": {
                "const": "POST",
                "description": "the ReST method(s) type allowed " "for this API",
                "type": "string",
            },
            "headers": {
                "type": "object",
                "additionalProperties": True,
                "properties": {
                    "content-type": {"type": "string", "enum": ["application/json"]},
                    "isBase64Encoded": {"type": "boolean"},
                },
                "required": ["content-type"],
            },
            "body": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "body_key1": {"type": "string"},
                    "body_key2": {"type": "object", "description": "some description"},
                },
            },
            "pathParameters": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "path_level1": {
                        "type": "string",
                        "description": "parameter description",
                    },
                    "path_level2": {
                        "type": "string",
                        "description": "parameter description",
                    },
                },
                "required": ["path_level1"],
            },
            "queryParameters": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "key1": {"items": {"type": "string"}, "type": "array"},
                    "key2": {
                        "items": {"type": "integer"},
                        "type": "array",
                        "description": "some description",
                    },
                },
                "required": list(),
            },
        },
        "required": [
            "headers",
            "httpMethod",
            "pathParameters",
        ],
    }

    from aws_schema.openAPI_converter import _convert_request

    assert (
        _convert_request(
            open_api_path, open_api_method, open_api_request, {"info": dict()}
        )
        == json_schema_request
    )


def test_request_translation_no_body_no_query():
    open_api_path = "test_request_resource"
    open_api_method = "post"
    open_api_request = {
        "summary": "Test API",
        "description": "some description",
        "operationId": "operationID",
        "parameters": [
            {
                "in": "path",
                "name": "path_level1",
                "schema": {"type": "string"},
                "required": True,
                "description": "parameter description",
            },
            {
                "in": "path",
                "name": "path_level2",
                "description": "parameter description",
                "schema": {"type": "string"},
            },
            {"in": "header", "name": "isBase64Encoded", "schema": {"type": "boolean"}},
        ],
    }

    json_schema_request = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "test_request_resource-POST",
        "description": "Test API\n---\nsome description",
        "type": "object",
        "additionalProperties": True,
        "properties": {
            "httpMethod": {
                "const": "POST",
                "description": "the ReST method(s) type allowed " "for this API",
                "type": "string",
            },
            "headers": {
                "type": "object",
                "additionalProperties": True,
                "properties": {
                    "content-type": {"type": "string", "enum": list()},
                    "isBase64Encoded": {"type": "boolean"},
                },
                "required": [],
            },
            "body": {
                "type": "object",
                "additionalProperties": False,
                "properties": dict(),
                "required": list(),
            },
            "pathParameters": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "path_level1": {
                        "type": "string",
                        "description": "parameter description",
                    },
                    "path_level2": {
                        "type": "string",
                        "description": "parameter description",
                    },
                },
                "required": ["path_level1"],
            },
            "queryParameters": {
                "type": "object",
                "additionalProperties": False,
                "properties": dict(),
                "required": list(),
            },
        },
        "required": [
            "headers",
            "httpMethod",
            "pathParameters",
        ],
    }

    from aws_schema.openAPI_converter import _convert_request

    assert (
        _convert_request(
            open_api_path, open_api_method, open_api_request, {"info": dict()}
        )
        == json_schema_request
    )


def test_request_translation_with_reference():
    open_api_path = "test_path_with_ref"
    open_api_method = "put"
    open_api_request = {
        "summary": "Test API",
        "description": "some description",
        "operationId": "operationID",
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "body_key1": {
                                "type": "string",
                                "description": "containing only a string",
                            },
                            "body_key2": {
                                "$ref": "#/components/schemas/example_object"
                            },
                        },
                        "required": ["body_key2"],
                    }
                }
            }
        },
    }

    open_api_full_schema_component = {
        "info": dict(),
        "components": {
            "schemas": {
                "example_object": {
                    "type": "object",
                    "properties": {
                        "example_key1": {
                            "type": "string",
                            "description": "explaining example_key1",
                        },
                        "example_key2": {"type": "integer"},
                    },
                }
            }
        },
    }

    json_schema_request = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "additionalProperties": True,
        "description": "Test API\n---\nsome description",
        "properties": {
            "body": {
                "additionalProperties": False,
                "properties": {
                    "body_key1": {
                        "description": "containing " "only a " "string",
                        "type": "string",
                    },
                    "body_key2": {
                        "properties": {
                            "example_key1": {
                                "description": "explaining " "example_key1",
                                "type": "string",
                            },
                            "example_key2": {"type": "integer"},
                        },
                        "type": "object",
                    },
                },
                "required": ["body_key2"],
                "type": "object",
            },
            "headers": {
                "additionalProperties": True,
                "properties": {
                    "content-type": {"enum": ["application/json"], "type": "string"}
                },
                "required": ["content-type"],
                "type": "object",
            },
            "httpMethod": {
                "const": "PUT",
                "description": "the ReST method(s) type allowed " "for this API",
                "type": "string",
            },
            "pathParameters": {
                "additionalProperties": False,
                "properties": dict(),
                "required": list(),
                "type": "object",
            },
            "queryParameters": {
                "additionalProperties": False,
                "properties": dict(),
                "required": list(),
                "type": "object",
            },
        },
        "required": ["body", "headers", "httpMethod"],
        "title": "test_path_with_ref-PUT",
        "type": "object",
    }

    from aws_schema.openAPI_converter import _convert_request

    assert (
        _convert_request(
            open_api_path,
            open_api_method,
            open_api_request,
            open_api_full_schema_component,
        )
        == json_schema_request
    )


def test_request_translation_with_unspecified_body():
    open_api_path = "test_path_with_unspecified_body"
    open_api_method = "post"
    open_api_request = {
        "summary": "Test API",
        "description": "some description",
        "operationId": "operationID",
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": {"type": "object", "additionalProperties": True}
                }
            }
        },
    }

    open_api_full_schema_component = {"info": dict()}

    json_schema_request = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "additionalProperties": True,
        "description": "Test API\n---\nsome description",
        "properties": {
            "body": {"additionalProperties": True, "type": "object"},
            "headers": {
                "additionalProperties": True,
                "properties": {
                    "content-type": {"enum": ["application/json"], "type": "string"}
                },
                "required": ["content-type"],
                "type": "object",
            },
            "httpMethod": {
                "const": "POST",
                "description": "the ReST method(s) type allowed " "for this API",
                "type": "string",
            },
            "pathParameters": {
                "additionalProperties": False,
                "properties": dict(),
                "required": list(),
                "type": "object",
            },
            "queryParameters": {
                "additionalProperties": False,
                "properties": dict(),
                "required": list(),
                "type": "object",
            },
        },
        "required": ["headers", "httpMethod"],
        "title": "test_path_with_unspecified_body-POST",
        "type": "object",
    }

    from aws_schema.openAPI_converter import _convert_request

    assert (
        _convert_request(
            open_api_path,
            open_api_method,
            open_api_request,
            open_api_full_schema_component,
        )
        == json_schema_request
    )
