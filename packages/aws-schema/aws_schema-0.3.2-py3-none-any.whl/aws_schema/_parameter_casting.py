from .json_to_python_type import json_to_python_type_convert


def _get_content_type(data):
    if "headers" in data and "content-type" in data["headers"]:
        content_type = data["headers"]["content-type"]
    elif "headers" in data and "Content-Type" in data["headers"]:
        content_type = data["headers"]["Content-Type"]
    else:
        content_type = None
    return content_type


def _cast_path_parameter(data, schema):
    for param_name in data["pathParameters"]:
        try:
            data["pathParameters"][param_name] = json_to_python_type_convert[
                schema["properties"]["pathParameters"]["properties"][param_name]["type"]
            ](data["pathParameters"][param_name])
        except (ValueError, SyntaxError):
            pass


def _cast_query_parameter(data, schema):
    for param_name in data["queryParameters"]:
        for param_no in range(len(data["queryParameters"][param_name])):
            try:
                data["queryParameters"][param_name][
                    param_no
                ] = json_to_python_type_convert[
                    schema["properties"]["queryParameters"]["properties"][param_name][
                        "items"
                    ]["type"]
                ](
                    data["queryParameters"][param_name][param_no]
                )
            except (ValueError, SyntaxError, KeyError):
                pass


def _cast_x_www_form_urlencoded(data, schema):
    converted = False
    if isinstance(data, str):
        data = json_to_python_type_convert[schema["type"]](data)
        converted = True

    if isinstance(data, list):
        for item_no, item in enumerate(data):
            data[item_no] = _cast_x_www_form_urlencoded(
                item, schema if not converted else schema["items"]
            )
    if isinstance(data, dict):
        for key in data:
            if "properties" in schema and key in schema["properties"]:
                data[key] = _cast_x_www_form_urlencoded(
                    data[key], schema["properties"][key]
                )
            elif "items" in schema.get(key, dict()):
                data[key] = _cast_x_www_form_urlencoded(data[key], schema[key]["items"])

    return data


def cast_parameter(data, schema):
    if "pathParameters" in data:
        _cast_path_parameter(data, schema)
    if "queryParameters" in data and data["queryParameters"]:
        _cast_query_parameter(data, schema)
    if _get_content_type(data) == "application/x-www-form-urlencoded":
        _cast_x_www_form_urlencoded(
            data["body"],
            schema["properties"].get("body", dict()).get("properties", dict()),
        )
