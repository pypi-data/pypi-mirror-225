def test_response_translation_text_plain():
    open_api_path = "test_request_resource"
    open_api_method = "post"
    open_api_statusCode = 404
    open_api_response = {
        "description": "Response for statusCode '404' for method 'POST' on API 'response_test'",
        "content": {
            "text/plain": {"schema": {"type": "string", "example": "not found"}}
        },
    }

    json_schema_response = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "test_request_resource-POST-404",
        "description": "Response for statusCode '404' for method 'POST' on API 'response_test'",
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "statusCode": {"type": "number"},
            "body": {"type": "string", "examples": ["not found"]},
            "headers": {
                "type": "object",
                "additionalProperties": True,
                "patternProperties": {
                    "[cC]ontent-[tT]ype": {"type": "string", "enum": ["text/plain"]}
                },
            },
        },
        "required": ["statusCode", "headers", "body"],
    }

    from aws_schema.openAPI_converter import _convert_response

    assert (
        _convert_response(
            open_api_path,
            open_api_method,
            open_api_statusCode,
            open_api_response,
            {"info": dict()},
        )
        == json_schema_response
    )


def test_response_translation_application_json():
    open_api_path = "test_request_resource"
    open_api_method = "post"
    open_api_statusCode = 200
    open_api_response = {
        "description": "Response for statusCode '200' for method 'POST' on API 'response_test'",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "key1": {"type": "string", "example": "some string"},
                        "key2": {"type": "number", "example": 0.3},
                        "key3": {"type": "integer", "examples": [1, 2, 3]},
                        "key4": {
                            "type": "array",
                            "items": {"type": "string"},
                            "example": ["a", "b"],
                        },
                        "key5": {
                            "type": "object",
                            "properties": {"sub_key": {"type": "string"}},
                        },
                    },
                }
            }
        },
    }

    json_schema_response = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "additionalProperties": False,
        "description": "Response for statusCode '200' for method 'POST' on API "
        "'response_test'",
        "properties": {
            "body": {
                "properties": {
                    "key1": {"examples": ["some string"], "type": "string"},
                    "key2": {"examples": [0.3], "type": "number"},
                    "key3": {"examples": [1, 2, 3], "type": "integer"},
                    "key4": {
                        "examples": [["a", "b"]],
                        "items": {"type": "string"},
                        "type": "array",
                    },
                    "key5": {
                        "properties": {"sub_key": {"type": "string"}},
                        "type": "object",
                    },
                },
                "type": "object",
            },
            "headers": {
                "additionalProperties": True,
                "patternProperties": {
                    "[cC]ontent-[tT]ype": {
                        "enum": ["application/json"],
                        "type": "string",
                    }
                },
                "type": "object",
            },
            "statusCode": {"type": "number"},
        },
        "required": ["statusCode", "headers", "body"],
        "title": "test_request_resource-POST-200",
        "type": "object",
    }

    from aws_schema.openAPI_converter import _convert_response

    assert (
        _convert_response(
            open_api_path,
            open_api_method,
            open_api_statusCode,
            open_api_response,
            {"info": dict()},
        )
        == json_schema_response
    )


def test_response_translation_multiple_content_types():
    open_api_path = "test_request_resource"
    open_api_method = "post"
    open_api_statusCode = 200
    open_api_response = {
        "description": "Response for statusCode '200' for method 'POST' on API 'response_test'",
        "content": {
            "text/plain": {"schema": {"type": "string", "example": "not found"}},
            "application/json": {
                "schema": {"type": "object", "properties": {"key1": {"type": "string"}}}
            },
        },
    }

    json_schema_response = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "description": "Response for statusCode '200' for method 'POST' on API "
        "'response_test'",
        "oneOf": [
            {
                "additionalProperties": False,
                "properties": {
                    "body": {"examples": ["not found"], "type": "string"},
                    "headers": {
                        "additionalProperties": True,
                        "patternProperties": {
                            "[cC]ontent-[tT]ype": {
                                "enum": ["text/plain", "application/json"],
                                "type": "string",
                            }
                        },
                        "type": "object",
                    },
                    "statusCode": {"type": "number"},
                },
                "required": ["statusCode", "headers", "body"],
                "type": "object",
            },
            {
                "additionalProperties": False,
                "properties": {
                    "body": {
                        "properties": {"key1": {"type": "string"}},
                        "type": "object",
                    },
                    "headers": {
                        "additionalProperties": True,
                        "patternProperties": {
                            "[cC]ontent-[tT]ype": {
                                "enum": ["text/plain", "application/json"],
                                "type": "string",
                            }
                        },
                        "type": "object",
                    },
                    "statusCode": {"type": "number"},
                },
                "required": ["statusCode", "headers", "body"],
                "type": "object",
            },
        ],
        "title": "test_request_resource-POST-200",
    }

    from aws_schema.openAPI_converter import _convert_response

    assert (
        _convert_response(
            open_api_path,
            open_api_method,
            open_api_statusCode,
            open_api_response,
            {"info": dict()},
        )
        == json_schema_response
    )


def test_response_translation_additional_headers():
    open_api_path = "test_request_resource"
    open_api_method = "post"
    open_api_statusCode = 404
    open_api_response = {
        "description": "Response for statusCode '404' for method 'POST' on API 'response_test'",
        "content": {
            "text/plain": {"schema": {"type": "string", "example": "not found"}}
        },
        "headers": {
            "header1": {
                "schema": {"type": "integer"},
                "description": "some description",
            },
            "header2": {"schema": {"type": "string", "pattern": "regex"}},
        },
    }

    json_schema_response = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "test_request_resource-POST-404",
        "description": "Response for statusCode '404' for method 'POST' on API 'response_test'",
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "statusCode": {"type": "number"},
            "body": {"type": "string", "examples": ["not found"]},
            "headers": {
                "type": "object",
                "additionalProperties": True,
                "patternProperties": {
                    "[cC]ontent-[tT]ype": {"type": "string", "enum": ["text/plain"]}
                },
                "properties": {
                    "header1": {"type": "integer", "description": "some description"},
                    "header2": {"type": "string", "pattern": "regex"},
                },
            },
        },
        "required": [
            "statusCode",
            "headers",
            "body",
        ],
    }

    from aws_schema.openAPI_converter import _convert_response

    assert (
        _convert_response(
            open_api_path,
            open_api_method,
            open_api_statusCode,
            open_api_response,
            {"info": dict()},
        )
        == json_schema_response
    )


def test_response_translation_array():
    open_api_path = "test_request_resource"
    open_api_method = "post"
    open_api_statusCode = 404
    open_api_response = {
        "description": "Response for statusCode '404' for method 'POST' on API 'response_test'",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "example_key": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {"key1": {"type": "string"}},
                                "required": ["key1"],
                            },
                        }
                    },
                }
            }
        },
    }

    json_schema_response = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "test_request_resource-POST-404",
        "description": "Response for statusCode '404' for method 'POST' on API 'response_test'",
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "statusCode": {"type": "number"},
            "body": {
                "type": "object",
                "properties": {
                    "example_key": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {"key1": {"type": "string"}},
                            "required": ["key1"],
                        },
                    }
                },
            },
            "headers": {
                "type": "object",
                "additionalProperties": True,
                "patternProperties": {
                    "[cC]ontent-[tT]ype": {
                        "type": "string",
                        "enum": ["application/json"],
                    }
                },
            },
        },
        "required": ["statusCode", "headers", "body"],
    }

    from aws_schema.openAPI_converter import _convert_response

    assert (
        _convert_response(
            open_api_path,
            open_api_method,
            open_api_statusCode,
            open_api_response,
            {"info": dict()},
        )
        == json_schema_response
    )


def test_response_translation_with_reference():
    open_api_path = "test_path_with_ref"
    open_api_method = "post"
    open_api_statusCode = 200
    open_api_response = {
        "description": "success",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "ref_key": {"$ref": "#/components/schemas/example_ref"}
                    },
                }
            }
        },
    }

    components = {
        "info": dict(),
        "components": {
            "schemas": {
                "example_ref": {
                    "type": "object",
                    "properties": {
                        "example_key1": {
                            "description": "explaining example_key1",
                            "type": "string",
                        },
                        "example_key2": {"type": "integer"},
                    },
                }
            }
        },
    }

    json_schema_response = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "test_path_with_ref-POST-200",
        "description": "success",
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "statusCode": {"type": "number"},
            "body": {
                "type": "object",
                "properties": {
                    "ref_key": {
                        "type": "object",
                        "properties": {
                            "example_key1": {
                                "description": "explaining example_key1",
                                "type": "string",
                            },
                            "example_key2": {"type": "integer"},
                        },
                    }
                },
            },
            "headers": {
                "type": "object",
                "additionalProperties": True,
                "patternProperties": {
                    "[cC]ontent-[tT]ype": {
                        "enum": ["application/json"],
                        "type": "string",
                    }
                },
            },
        },
        "required": [
            "statusCode",
            "headers",
            "body",
        ],
    }

    from aws_schema.openAPI_converter import _convert_response

    assert (
        _convert_response(
            open_api_path,
            open_api_method,
            open_api_statusCode,
            open_api_response,
            components,
        )
        == json_schema_response
    )


def test_response_translation_with_reference_in_items():
    open_api_path = "test_path_with_ref"
    open_api_method = "post"
    open_api_statusCode = 200
    open_api_response = {
        "description": "success",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "example_key": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/example_ref"},
                        }
                    },
                }
            }
        },
    }

    components = {
        "info": dict(),
        "components": {
            "schemas": {
                "example_ref": {
                    "type": "object",
                    "properties": {
                        "example_key1": {
                            "description": "explaining example_key1",
                            "type": "string",
                        },
                        "example_key2": {"type": "integer"},
                    },
                }
            }
        },
    }

    json_schema_response = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "test_path_with_ref-POST-200",
        "description": "success",
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "statusCode": {"type": "number"},
            "body": {
                "type": "object",
                "properties": {
                    "example_key": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "example_key1": {
                                    "description": "explaining example_key1",
                                    "type": "string",
                                },
                                "example_key2": {"type": "integer"},
                            },
                        },
                    }
                },
            },
            "headers": {
                "type": "object",
                "additionalProperties": True,
                "patternProperties": {
                    "[cC]ontent-[tT]ype": {
                        "enum": ["application/json"],
                        "type": "string",
                    }
                },
            },
        },
        "required": [
            "statusCode",
            "headers",
            "body",
        ],
    }

    from aws_schema.openAPI_converter import _convert_response

    assert (
        _convert_response(
            open_api_path,
            open_api_method,
            open_api_statusCode,
            open_api_response,
            components,
        )
        == json_schema_response
    )


def test_response_translation_no_body():
    open_api_path = "test_path_with_ref"
    open_api_method = "post"
    open_api_statusCode = 404
    open_api_response = {"description": "not found"}

    json_schema_response = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "test_path_with_ref-POST-404",
        "description": "not found",
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "statusCode": {"type": "number"},
            "headers": {
                "additionalProperties": True,
                "type": "object",
            },
        },
        "required": ["statusCode"],
    }

    from aws_schema.openAPI_converter import _convert_response

    assert (
        _convert_response(
            open_api_path,
            open_api_method,
            open_api_statusCode,
            open_api_response,
            {"info": dict()},
        )
        == json_schema_response
    )


def test_response_translation_no_body_with_header():
    open_api_path = "/test_path_with_ref"
    open_api_method = "post"
    open_api_statusCode = 400
    open_api_response = {
        "description": "error",
        "headers": {"header_key": {"schema": {"type": "string"}}},
    }

    json_schema_response = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "/test_path_with_ref-POST-400",
        "description": "error",
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "statusCode": {"type": "number"},
            "headers": {
                "type": "object",
                "additionalProperties": True,
                "properties": {"header_key": {"type": "string"}},
            },
        },
        "required": ["statusCode", "headers"],
    }

    from aws_schema.openAPI_converter import _convert_response

    assert (
        _convert_response(
            open_api_path,
            open_api_method,
            open_api_statusCode,
            open_api_response,
            {"info": dict()},
        )
        == json_schema_response
    )


def test_response_translation_text_plain_without_schema():
    open_api_path = "/test_path_with_ref"
    open_api_method = "post"
    open_api_statusCode = 400
    open_api_response = {
        "description": "error",
        "content": {"text/plain": {}, "example": "not found"},
    }

    json_schema_response = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "/test_path_with_ref-POST-400",
        "description": "error",
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "statusCode": {"type": "number"},
            "body": {"type": "string", "example": "not found"},
            "headers": {
                "type": "object",
                "additionalProperties": True,
                "patternProperties": {
                    "[cC]ontent-[tT]ype": {"enum": ["text/plain"], "type": "string"}
                },
            },
        },
        "required": ["statusCode", "headers", "body"],
    }

    from aws_schema.openAPI_converter import _convert_response

    assert (
        _convert_response(
            open_api_path,
            open_api_method,
            open_api_statusCode,
            open_api_response,
            {"info": dict()},
        )
        == json_schema_response
    )


def test_response_translation_propertyPattern():
    open_api_path = "test_request_resource"
    open_api_method = "post"
    open_api_statusCode = 404
    open_api_response = {
        "description": "Response for statusCode '404' for method 'POST' on API 'response_test'",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "patternProperties": {"^\\d+$": {"type": "string"}},
                }
            }
        },
    }

    json_schema_response = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "test_request_resource-POST-404",
        "description": "Response for statusCode '404' for method 'POST' on API 'response_test'",
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "statusCode": {"type": "number"},
            "body": {
                "type": "object",
                "patternProperties": {"^\\d+$": {"type": "string"}},
                "additionalProperties": False,
            },
            "headers": {
                "type": "object",
                "additionalProperties": True,
                "patternProperties": {
                    "[cC]ontent-[tT]ype": {
                        "type": "string",
                        "enum": ["application/json"],
                    }
                },
            },
        },
        "required": ["statusCode", "headers", "body"],
    }

    from aws_schema.openAPI_converter import _convert_response

    assert (
        _convert_response(
            open_api_path,
            open_api_method,
            open_api_statusCode,
            open_api_response,
            {"info": dict()},
        )
        == json_schema_response
    )


def test_response_translation_propertyPattern_with_ref():
    open_api_path = "test_request_resource"
    open_api_method = "post"
    open_api_statusCode = 404
    open_api_response = {
        "description": "Response for statusCode '404' for method 'POST' on API 'response_test'",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "patternProperties": {
                        "^\\d+$": {"$ref": "#/components/schemas/example_ref"}
                    },
                }
            }
        },
    }

    components = {
        "info": dict(),
        "components": {
            "schemas": {
                "example_ref": {
                    "type": "object",
                    "properties": {
                        "example_key1": {
                            "description": "explaining example_key1",
                            "type": "string",
                        },
                        "example_key2": {"type": "integer"},
                    },
                }
            }
        },
    }

    json_schema_response = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "test_request_resource-POST-404",
        "description": "Response for statusCode '404' for method 'POST' on API 'response_test'",
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "statusCode": {"type": "number"},
            "body": {
                "type": "object",
                "patternProperties": {
                    "^\\d+$": {
                        "type": "object",
                        "properties": {
                            "example_key1": {
                                "description": "explaining example_key1",
                                "type": "string",
                            },
                            "example_key2": {"type": "integer"},
                        },
                    }
                },
                "additionalProperties": False,
            },
            "headers": {
                "type": "object",
                "additionalProperties": True,
                "patternProperties": {
                    "[cC]ontent-[tT]ype": {
                        "type": "string",
                        "enum": ["application/json"],
                    }
                },
            },
        },
        "required": ["statusCode", "headers", "body"],
    }

    from aws_schema.openAPI_converter import _convert_response

    assert (
        _convert_response(
            open_api_path,
            open_api_method,
            open_api_statusCode,
            open_api_response,
            components,
        )
        == json_schema_response
    )
