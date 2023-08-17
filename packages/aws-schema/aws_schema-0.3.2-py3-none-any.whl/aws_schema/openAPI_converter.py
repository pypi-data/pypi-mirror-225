from copy import deepcopy
from pathlib import Path
from json import dump

__all__ = ["OpenAPIConverter"]

__JSON_SCHEMA_DRAFT = "http://json-schema.org/draft-07/schema#"


def _schema_to_property(
    api_schema: dict, full_schema: dict, query_param: bool = False
) -> dict:
    json_schema = dict()

    def get_nested_from_dict(keys: (list, iter), schema: dict) -> dict:
        keys = iter(keys)
        try:
            key = next(keys)
        except StopIteration:
            if "$ref" in schema:
                return get_nested_from_dict(schema["$ref"][2:].split("/"), full_schema)
            return schema
        return get_nested_from_dict(keys, schema[key])

    if "$ref" in api_schema:
        api_schema = get_nested_from_dict(
            api_schema["$ref"][2:].split("/"), full_schema
        )

    elif "items" in api_schema and "$ref" in api_schema["items"]:
        api_schema["items"] = get_nested_from_dict(
            api_schema["items"]["$ref"][2:].split("/"), full_schema
        )

    elif "oneOf" in api_schema:
        for oneOf_no in range(len(api_schema["oneOf"])):
            api_schema["oneOf"][oneOf_no] = _schema_to_property(
                api_schema["oneOf"][oneOf_no], full_schema
            )

    if "example" in api_schema:
        json_schema.update({"examples": [api_schema["example"]]})
        del api_schema["example"]

    if "type" in api_schema:
        if query_param:
            api_schema = {"items": api_schema, "type": "array"}

        if api_schema["type"] == "object":
            key = False
            if "patternProperties" in api_schema:
                api_schema["additionalProperties"] = False
                key = "patternProperties"
            elif "properties" in api_schema:
                key = "properties"
            if key:
                for prop in api_schema[key]:
                    api_schema[key][prop] = _schema_to_property(
                        api_schema[key][prop], full_schema
                    )

    if "items" in api_schema:
        if "properties" in api_schema["items"]:
            for prop in api_schema["items"]["properties"]:
                api_schema["items"]["properties"][prop] = _schema_to_property(
                    api_schema["items"]["properties"][prop], full_schema
                )

    if api_schema.get("nullable") is True:
        api_schema.pop("nullable")

        keys_to_keep_at_level = ["oneOf", "description"]

        if "oneOf" not in api_schema:

            api_schema["oneOf"]  = [
                {"type": "null"}, {k: v for k, v in api_schema.items() if k not in keys_to_keep_at_level}
            ]
        else:
            oneOf = api_schema.pop("oneOf")
            api_schema["oneOf"] = [
                {"type": "null"}
            ] + oneOf
        for key in api_schema.copy():
            if key not in keys_to_keep_at_level:
                api_schema.pop(key)


    json_schema.update(api_schema)

    return json_schema


def _convert_response(path, method, statusCode, api_schema, full_schema) -> dict:
    schema = {
        "$schema": __JSON_SCHEMA_DRAFT,
        "title": f"{path}-{method.upper()}-{statusCode}",
        "description": api_schema["description"] if "description" in api_schema else "",
    }

    if "version" in full_schema["info"]:
        schema.update({"version": full_schema["info"]["version"]})

    spec = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "statusCode": {"type": "number"},
            "headers": {"type": "object", "additionalProperties": True},
        },
        "required": ["statusCode"],
    }

    if "content" in api_schema:
        spec["properties"].update({"body": dict()})
        spec["properties"]["headers"].update(
            {
                "patternProperties": {
                    "[cC]ontent-[tT]ype": {
                        "type": "string",
                        "enum": [
                            i for i in api_schema["content"].keys() if i != "example"
                        ],
                    }
                }
            }
        )
        spec["required"].append("headers")
        spec["required"].append("body")
    else:
        api_schema["content"] = list()

    if "headers" in api_schema:
        if "properties" not in spec["properties"]["headers"]:
            spec["properties"]["headers"]["properties"] = dict()
        for header in api_schema["headers"]:
            spec["properties"]["headers"]["properties"].update(
                {
                    header: _schema_to_property(
                        api_schema["headers"][header]["schema"], full_schema
                    )
                }
            )
        if "headers" not in spec["required"]:
            spec["required"].append("headers")

    specs = list()

    for content_type in api_schema["content"]:
        if content_type == "example":
            continue
        spec_var = spec.copy()

        try:
            spec_var["properties"]["body"] = _schema_to_property(
                api_schema["content"][content_type]["schema"], full_schema
            )
        except KeyError as e:
            if content_type == "text/plain":
                spec_var["properties"]["body"]["type"] = "string"
                if "example" in api_schema["content"]:
                    spec_var["properties"]["body"]["example"] = api_schema["content"][
                        "example"
                    ]
            else:
                raise e
        if "headers" in api_schema:
            for header in api_schema["headers"]:
                spec_var["properties"]["headers"]["properties"][
                    header
                ] = _schema_to_property(
                    api_schema["headers"][header]["schema"], full_schema
                )
                if "description" in api_schema["headers"][header]:
                    spec_var["properties"]["headers"]["properties"][header].update(
                        {"description": api_schema["headers"][header]["description"]}
                    )

        specs.append(deepcopy(spec_var))

    if len(specs) == 1:
        schema.update(specs[0])
    elif len(specs) > 1:
        schema.update({"oneOf": specs})
    else:
        schema.update(spec)
    return schema


def _convert_request(path, method, api_schema, full_schema) -> dict:
    schema = {
        "$schema": __JSON_SCHEMA_DRAFT,
        "title": f"{path}-{method.upper()}",
        "type": "object",
        "additionalProperties": True,
        "properties": {
            "httpMethod": {
                "const": method.upper(),
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
                "type": "object",
                "additionalProperties": False,
                "properties": dict(),
                "required": list(),
            },
            "queryParameters": {
                "type": "object",
                "additionalProperties": False,
                "properties": dict(),
                "required": list(),
            },
        },
        "required": ["httpMethod"],
    }

    if "version" in full_schema["info"]:
        schema.update({"version": full_schema["info"]["version"]})

    if method != "get":
        schema["properties"]["headers"]["properties"].update(
            {"content-type": {"type": "string", "enum": list()}}
        )

    def add_description():
        if "summary" in api_schema and "description" in api_schema:
            schema[
                "description"
            ] = f"{api_schema['summary']}\n---\n{api_schema['description']}"
        elif "summary" in api_schema:
            schema["description"] = api_schema["summary"]
        elif "description" in api_schema:
            schema["description"] = api_schema["description"]

    add_description()

    required_parameter_types = {"headers"}
    parameter_type_map = {
        "header": "headers",
        "path": "pathParameters",
        "query": "queryParameters",
    }
    if "parameters" in api_schema:
        for parameter in api_schema["parameters"]:
            parameter_type = parameter_type_map[parameter["in"]]
            parameter_name = parameter["name"]

            schema["properties"][parameter_type]["properties"][
                parameter_name
            ] = _schema_to_property(
                parameter["schema"],
                full_schema,
                True if parameter_type == "queryParameters" else False,
            )

            if "description" in parameter:
                schema["properties"][parameter_type]["properties"][parameter_name][
                    "description"
                ] = parameter["description"]

            if "required" not in schema["properties"][parameter_type]:
                schema["properties"][parameter_type]["required"] = list()
            if "required" in parameter and parameter["required"]:
                required_parameter_types.add(parameter_type)
                schema["properties"][parameter_type]["required"].append(parameter_name)

    if "requestBody" in api_schema:
        schema["properties"]["headers"]["required"].append("content-type")
        bodies = list()
        if (
            "required" in api_schema["requestBody"]
            and api_schema["requestBody"]["required"]
        ):
            required_parameter_types.add("body")
        for content_type in api_schema["requestBody"]["content"]:
            schema["properties"]["headers"]["properties"]["content-type"][
                "enum"
            ].append(content_type)

            body = _schema_to_property(
                api_schema["requestBody"]["content"][content_type]["schema"],
                full_schema,
            )
            if "additionalProperties" not in body:
                body.update({"additionalProperties": False})
            if "required" in body and body["required"]:
                required_parameter_types.add("body")
            bodies.append(body)

        if len(bodies) == 1:
            schema["properties"]["body"] = bodies[0]
        else:
            schema["properties"]["body"] = {"oneOf": bodies}

    schema["required"] += required_parameter_types
    schema["required"].sort()

    return schema


class _OpenAPIResponses:
    def __init__(self, method):
        self.__method = method

        self.__responses = dict()

    @property
    def method(self):
        return self.__method

    @property
    def origin_schema(self):
        return self.method.origin_schema["responses"]

    def __iter__(self):
        return iter(self.method.origin_schema["responses"])

    def __getitem__(self, statusCode: int) -> dict:
        statusCode = int(statusCode)
        if statusCode not in self.__responses:
            self.__resolve_response(statusCode)
        return self.__responses[statusCode]

    def __resolve_response(self, statusCode):
        try:
            api_schema = self.origin_schema[int(statusCode)]
        except KeyError:
            api_schema = self.origin_schema[str(statusCode)]

        self.__responses[statusCode] = _convert_response(
            path=self.method.path.path_name,
            method=self.method.method_name,
            statusCode=statusCode,
            api_schema=api_schema,
            full_schema=self.method.path.origin.origin_schema,
        )


class _OpenAPIMethod:
    def __init__(self, path, method):
        self.__path = path
        self.__method = method
        self.__request = None
        self.__responses = _OpenAPIResponses(self)

        self.path.methods[self.method_name] = self
        property(self.path.__setattr__(self.method_name, self))

    @property
    def path(self):
        return self.__path

    @property
    def method_name(self):
        return self.__method

    @property
    def origin_schema(self):
        return self.path.origin_schema[self.method_name]

    @property
    def response(self) -> _OpenAPIResponses:
        return self.__responses

    @property
    def request(self):
        if not self.__request:
            self.__request = _convert_request(
                path=self.path.path_name,
                method=self.method_name,
                api_schema=self.origin_schema,
                full_schema=self.path.origin.origin_schema,
            )
        return self.__request


class _OpenAPIPath:
    def __init__(self, origin, path: str):
        self.__origin = origin
        self.__path = path
        self.__methods = dict()

        self.origin.validation_schema[self.path_name] = self

    @property
    def origin(self):
        return self.__origin

    @property
    def path_name(self) -> str:
        return self.__path

    @property
    def origin_schema(self):
        return self.origin.origin_schema["paths"][self.path_name]

    @property
    def methods(self):
        return self.__methods

    def __iter__(self):
        return iter(self.origin_schema)

    def __getitem__(self, method):
        method = method.lower()

        if method not in self.methods:
            _OpenAPIMethod(self, method)
        return self.methods[method]


class OpenAPIConverter:
    def __init__(self, open_api_schema: dict):
        self.__origin_schema = open_api_schema
        self.__validation_schema = dict()
        self.__save_directory = str()

    @property
    def origin_schema(self):
        return self.__origin_schema

    @property
    def validation_schema(self):
        return self.__validation_schema

    def __getitem__(self, path: str) -> _OpenAPIPath:
        if path not in self.validation_schema:
            _OpenAPIPath(self, path)
        return self.validation_schema[path]

    def __iter__(self):
        return iter(self.origin_schema["paths"])

    def __write_schema(self, schema, path, method, response=None):
        file_name = (
            f"{path}-{method.upper()}-{response}.json"[1:]
            if response
            else f"{path}-{method.upper()}.json"[1:]
        )

        file_name = file_name.replace("/", "||")
        p = Path(self.__save_directory, file_name)
        with open(p, "w") as f:
            dump(schema, f, indent=4)

    def create_all_schemas(self, directory: (str, Path) = "api"):
        self.__save_directory = directory
        for path in self:
            for method in self[path]:
                self.__write_schema(self[path][method].request, path, method)
                for response in self[path][method].response:
                    self.__write_schema(
                        self[path][method].response[response], path, method, response
                    )
