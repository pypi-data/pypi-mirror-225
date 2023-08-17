from .json_to_python_type import json_to_python_type_switch
from json import load as json_load
from jsonschema.validators import Draft7Validator, RefResolver
from jsonschema.exceptions import ValidationError
from os.path import dirname, abspath
from .nested_dict_helper import delete_keys_in_nested_dict, find_path_values_in_dict
from copy import deepcopy
from pathlib import Path

_current_validator = Draft7Validator

__all__ = [
    "SchemaValidator",
    "verify_data",
    "check_if_data_type_is_allowed",
]


class SchemaValidator:
    def __init__(
        self,
        file: str = None,
        url: str = None,
        raw: dict = None,
        custom_validator: _current_validator = _current_validator,
    ):
        if not any(i for i in [file, url, raw]):
            raise ValueError("one input must be specified")
        self.__file = file
        self.__url = url
        self.__raw = raw
        self.__base_validator = custom_validator

        self.__resolver = None

        self.__validator = None
        self.__validator_without_required_check = None

        if file:
            self.__open_file(file)

        elif url:
            raise NotImplementedError

        else:
            self.__raw_schema = raw

    def __open_file(self, origin):
        origin = Path(origin)
        if origin.suffix != ".json":
            origin = origin.with_suffix(".json")
        with open(origin, "r") as f:
            self.__raw_schema = json_load(f)

    @property
    def schema(self):
        return self.validator.schema

    @property
    def validator(self):
        if not self.__validator:
            self.__create_validator()
        return self.__validator

    @property
    def validator_without_required_check(self):
        if not self.__validator_without_required_check:
            self.__create_validator(no_required_key=True)
        return self.__validator_without_required_check

    def validate(self, data, no_required_check=False):
        if not no_required_check:
            self.validator.validate(data)
        else:
            self.validator_without_required_check.validate(data)

    def get_sub_schema(
        self, path_to_sub_schema: list, current_sub_schema: dict = None, depth: int = 0
    ) -> (dict, int):
        if not current_sub_schema:
            current_sub_schema = self.schema
        next_element = path_to_sub_schema.__iter__()
        try:
            if "properties" in current_sub_schema:
                n = next(next_element)
                depth += 1
                return self.get_sub_schema(
                    path_to_sub_schema[1:], current_sub_schema["properties"][n], depth
                )
            elif "patternProperties" in current_sub_schema:
                from re import compile

                n = next(next_element)
                depth += 1
                for key in current_sub_schema["patternProperties"]:
                    if compile(key).match(n):
                        return self.get_sub_schema(
                            path_to_sub_schema[1:],
                            current_sub_schema["patternProperties"][key],
                            depth,
                        )
                raise ValidationError(
                    f"none of the patternProperties matched: {list(current_sub_schema['patternProperties'].keys())}",
                )
            elif "items" in current_sub_schema and next(next_element):
                depth += 1
                return self.get_sub_schema(
                    path_to_sub_schema, current_sub_schema["items"], depth
                )
            elif "$ref" in current_sub_schema:
                current_sub_schema = self.validator.resolver.resolve(
                    current_sub_schema["$ref"]
                )
                return self.get_sub_schema(
                    path_to_sub_schema, current_sub_schema[1], depth
                )

            elif "oneOf" in current_sub_schema:
                one_of_types = list()
                for item in current_sub_schema["oneOf"]:
                    schema_part, depth = self.get_sub_schema(
                        path_to_sub_schema, item, depth
                    )
                    one_of_types.append(schema_part)
                current_sub_schema = {"oneOf": one_of_types}

            elif next(next_element) in current_sub_schema:
                n = path_to_sub_schema[0]
                return self.get_sub_schema(
                    path_to_sub_schema[1:], current_sub_schema[n], depth
                )

            return current_sub_schema, depth
        except StopIteration:
            return current_sub_schema, depth

    def validate_sub_part(self, new_data):
        paths_in_new_data, new_values = find_path_values_in_dict(new_data)

        for path_no in range(len(paths_in_new_data)):
            path_to_new_attribute = paths_in_new_data[path_no]

            relevant_sub_schema, depth = self.get_sub_schema(path_to_new_attribute)
            if depth != len(paths_in_new_data[path_no]):
                paths_in_new_data[path_no] = paths_in_new_data[path_no][:depth]
                relevant_path = paths_in_new_data[path_no].copy()
                new_values[path_no] = new_data.copy()
                while relevant_path:
                    new_values[path_no] = new_values[path_no][relevant_path.pop(0)]
            try:
                self.__base_validator(
                    relevant_sub_schema,
                    resolver=self.validator.resolver,
                ).validate(new_values[path_no])
            except ValidationError as VE:
                for path in path_to_new_attribute[::-1]:
                    VE.__dict__["path"].appendleft(path)
                raise VE

    def __file_resolver(self):
        absolute_directory = dirname(abspath(self.__file))
        relative_directory = f"file://{absolute_directory}/"
        self.__resolver = RefResolver(relative_directory, None)

    def __url_resolver(self):
        raise NotImplementedError

    def __create_validator(self, no_required_key=False):
        if self.__file:
            self.__file_resolver()
        elif self.__url:
            self.__url_resolver()

        if no_required_key:
            schema = deepcopy(self.__raw_schema)
            delete_keys_in_nested_dict(schema, ["required"])
            self.__validator_without_required_check = self.__base_validator(
                schema, resolver=self.__resolver
            )
        else:
            self.__validator = self.__base_validator(
                self.__raw_schema, resolver=self.__resolver
            )


def verify_data(
    data_to_verify: dict, file: str = None, url: str = None, raw: dict = None
):
    """
    Verify data to JSON schema

    Parameters
    ----------
    data_to_verify : dict
        any data to check if fitting the schema
    file : str
        if schema is originated at file
    url : str
        if schema is originated at url
    raw : dict
        the schema directly provided

    """
    validator_class = SchemaValidator(file, url, raw)
    validator_class.validator.validate(data_to_verify)


def check_if_data_type_is_allowed(data, json_type, enum=False):
    if enum:
        if data not in enum:
            raise TypeError
    else:
        if not isinstance(json_type, (list, tuple)):
            json_type = [json_type]

        for type_entry in json_type:
            if isinstance(data, json_to_python_type_switch[type_entry]):
                return
        raise TypeError
