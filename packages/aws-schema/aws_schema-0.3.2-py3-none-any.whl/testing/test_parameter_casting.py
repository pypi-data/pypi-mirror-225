from pytest import mark


@mark.parametrize(
    ("schema_body", "parsed_body"),
    (
        (
            {
                "body": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "key1": {"type": "array", "items": {"type": "string"}},
                        "key2": {"type": "array", "items": {"type": "integer"}},
                        "key3": {"type": "array", "items": {"type": "string"}},
                        "key4": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {"subKey": {"type": "integer"}},
                            },
                        },
                    },
                }
            },
            {"key1": ["value1"], "key2": [2], "key3": ["02"], "key4": [{"subKey": 3}]},
        ),
        (
            {
                "body": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "key1": {"type": "array", "items": {"type": "string"}},
                        "key2": {"type": "array", "items": {"type": "integer"}},
                        "key3": {"type": "array", "items": {"type": "string"}},
                        "key4": {"type": "array", "items": {"type": "object"}},
                    },
                }
            },
            {
                "key1": ["value1"],
                "key2": [2],
                "key3": ["02"],
                "key4": [{"subKey": "3"}],
            },
        ),
        (
            {
                "body": {
                    "type": "object",
                    "additionalProperties": True,
                }
            },
            {
                "key1": ["value1"],
                "key2": ["2"],
                "key3": ["02"],
                "key4": ['{"subKey": "3"}'],
            },
        ),
        (
            dict(),
            {
                "key1": ["value1"],
                "key2": ["2"],
                "key3": ["02"],
                "key4": ['{"subKey": "3"}'],
            },
        ),
    ),
)
def test_x_www_url_encoded(schema_body, parsed_body):
    data = {
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "body": {
            "key1": ["value1"],
            "key2": ["2"],
            "key3": ["02"],
            "key4": ['{"subKey": "3"}'],
        },
    }
    schema = {
        "type": "object",
        "additionalProperties": True,
        "properties": {
            "httpMethod": {
                "const": "POST",
                "description": "the ReST method(s) type allowed for this API",
                "type": "string",
            },
        },
    }

    schema["properties"].update(schema_body)
    from aws_schema._parameter_casting import cast_parameter

    cast_parameter(data, schema)
    assert data["body"] == parsed_body
