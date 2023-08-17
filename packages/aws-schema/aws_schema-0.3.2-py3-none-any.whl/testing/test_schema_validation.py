from unittest import TestCase
from os.path import dirname, realpath
from jsonschema.exceptions import ValidationError

from testing import load_json_file


class TestSchemaValidation(TestCase):
    pass


class TestFullSchemaValidation(TestSchemaValidation):
    def test_basic_schema(self):
        from aws_schema import SchemaValidator

        test_item = load_json_file(
            f"{dirname(realpath(__file__))}/test_data/database/item_basic.json"
        )

        schema_file = (
            f"{dirname(realpath(__file__))}//test_data/database/schema_basic.json"
        )
        validator = SchemaValidator(file=schema_file)

        validator.validate(test_item)

    def test_basic_schema_wrong_data(self):
        from aws_schema import SchemaValidator

        test_item = load_json_file(
            f"{dirname(realpath(__file__))}/test_data/database/item_basic_wrong.json"
        )

        schema_file = (
            f"{dirname(realpath(__file__))}/test_data/database/schema_basic.json"
        )
        validator = SchemaValidator(file=schema_file)

        try:
            validator.validate(test_item)
            self.fail()
        except ValidationError:
            pass

    def test_nested_schema(self):
        from os import chdir, getcwd

        actual_cwd = getcwd()
        chdir(dirname(realpath(__file__)))

        try:
            from aws_schema import SchemaValidator

            test_item = load_json_file(
                f"{dirname(realpath(__file__))}/test_data/database/item_nested.json"
            )

            schema_file = (
                f"{dirname(realpath(__file__))}/test_data/database/schema_nested.json"
            )
            validator = SchemaValidator(file=schema_file)

            validator.validate(test_item)
        except BaseException as b:
            exc = b
        finally:
            chdir(actual_cwd)
        if "exc" in globals():
            raise exc

    def test_basic_schema_without_required(self):
        from aws_schema import SchemaValidator

        test_item = load_json_file(
            f"{dirname(realpath(__file__))}/test_data/database/item_basic.json"
        )

        test_item.pop("some_float")

        schema_file = (
            f"{dirname(realpath(__file__))}/test_data/database/schema_basic.json"
        )
        validator = SchemaValidator(file=schema_file)

        validator.validate(test_item, no_required_check=True)

    def test_basic_schema_without_required_nested(self):
        from aws_schema import SchemaValidator

        test_item = load_json_file(
            f"{dirname(realpath(__file__))}/test_data/database/item_basic.json"
        )

        test_item["some_nested_dict"]["KEY1"].pop("subKEY2")

        schema_file = (
            f"{dirname(realpath(__file__))}/test_data/database/schema_basic.json"
        )
        validator = SchemaValidator(file=schema_file)

        validator.validate(test_item, no_required_check=True)


class TestGetSubSchema(TestSchemaValidation):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw_schema_file = (
            f"{dirname(realpath(__file__))}/test_data/database/schema_nested.json"
        )
        cls.raw_schema = load_json_file(cls.raw_schema_file)

        from aws_schema import SchemaValidator

        cls.validator = SchemaValidator(file=cls.raw_schema_file)

    def test_get_first_level(self):
        sub_schema, depth = self.validator.get_sub_schema(["some_dict"])

        self.assertEqual(self.raw_schema["properties"]["some_dict"], sub_schema)
        self.assertEqual(1, depth)

    def test_get_nested_dict(self):
        sub_schema, depth = self.validator.get_sub_schema(
            ["some_nested_dict", "KEY1", "subKEY2"]
        )

        self.assertEqual(
            self.raw_schema["properties"]["some_nested_dict"]["properties"]["KEY1"][
                "properties"
            ]["subKEY2"],
            sub_schema,
        )
        self.assertEqual(3, depth)

    def test_get_array(self):
        sub_schema, depth = self.validator.get_sub_schema(["some_array"])

        self.assertEqual(self.raw_schema["properties"]["some_array"], sub_schema)
        self.assertEqual(1, depth)

    def test_get_referenced_sub_schema_from_dict(self):
        sub_schema, depth = self.validator.get_sub_schema(
            ["some_nested_dict", "KEY1", "subKEY3"]
        )

        nested_schema = load_json_file(
            f"{dirname(realpath(__file__))}/test_data/database/schema_nested_definitions.json"
        )
        self.assertEqual(
            nested_schema["definitions"]["third_nested_dict_key"], sub_schema
        )
        self.assertEqual(3, depth)

    def test_get_referenced_sub_schema_from_array(self):
        sub_schema, depth = self.validator.get_sub_schema(["nested_array", "KEY1"])

        nested_schema = load_json_file(
            f"{dirname(realpath(__file__))}/test_data/database/schema_nested_array_child.json"
        )
        self.assertEqual(nested_schema["properties"]["KEY1"], sub_schema)
        self.assertEqual(2, depth)

    def test_get_one_of_sub_schema(self):
        sub_schema, depth = self.validator.get_sub_schema(["oneOfKey", "oneOfKey1"])

        self.assertEqual(
            {"oneOf": [{"type": "integer"}, {"type": "string"}]}, sub_schema
        )
        self.assertEqual(3, depth)

    def test_get_subschema_with_more_depth_than_available(self):
        sub_schema, depth = self.validator.get_sub_schema(
            ["some_nested_dict", "KEY2", "anySubKey", "nextSubLevel"]
        )

        self.assertEqual(
            self.raw_schema["properties"]["some_nested_dict"]["properties"]["KEY2"],
            sub_schema,
        )
        self.assertEqual(2, depth)


class TestCheckSubItemType(TestSchemaValidation):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw_schema_file = (
            f"{dirname(realpath(__file__))}/test_data/database/schema_nested.json"
        )
        cls.raw_schema = load_json_file(cls.raw_schema_file)

        from aws_schema import SchemaValidator

        cls.validator = SchemaValidator(file=cls.raw_schema_file)

    def test_first_level_string(self):
        self.validator.validate_sub_part({"some_string": "abcdef"})

    def test_first_level_int(self):
        self.validator.validate_sub_part({"some_int": 3})

    def test_nested_dict_end_value(self):
        self.validator.validate_sub_part({"some_nested_dict": {"KEY1": {"subKEY2": 4}}})

    def test_nested_dict_unspecified_sub_type(self):
        self.validator.validate_sub_part(
            {"some_nested_dict": {"KEY2": {"anyKey": "any string at lowest level"}}}
        )

    def test_nested_dict_end_value_wrong_value_with_schema_error_path(self):
        from jsonschema import ValidationError

        with self.assertRaises(ValidationError) as VE:
            self.validator.validate_sub_part(
                {"some_nested_dict": {"KEY1": {"subKEY3": ["string_value", 4]}}}
            )

        self.assertEqual("4 is not of type 'string'", VE.exception.args[0])
        self.assertEqual(
            ["some_nested_dict", "KEY1", "subKEY3", 1], list(VE.exception.path)
        )

    def test_nested_dict_pattern_properties(self):
        new_sub_dict = {
            "some_nested_dict": {
                "KEY1": {"subKEY4": {"abc": [{"sub_sub_key": "some_string_value"}]}}
            }
        }
        self.validator.validate_sub_part(new_sub_dict)

    def test_nested_dict_pattern_properties_wrong_pattern(self):
        from jsonschema import ValidationError

        new_sub_dict = {
            "some_nested_dict": {
                "KEY1": {"subKEY4": {"Abc": [{"sub_sub_key": "some_string_value"}]}}
            }
        }
        with self.assertRaises(ValidationError) as VE:
            self.validator.validate_sub_part(new_sub_dict)

        self.assertEqual(
            "none of the patternProperties matched: ['^[a-z]+$', '^[a-z0-9]+$']",
            VE.exception.args[0],
        )

        # ToDo path isn't added when checking patternProperties
        # self.assertEqual(
        #     ["some_nested_dict", "KEY1", "subKEY4"], list(VE.exception.path)
        # )

    def test_nested_dict_dict_value(self):
        self.validator.validate_sub_part(
            {"some_nested_dict": {"KEY1": {"subKEY1": "some_string", "subKEY2": 5}}}
        )

    def test_array_item1(self):
        self.validator.validate_sub_part({"some_array": ["some_string"]})

    def test_array_item2(self):
        self.validator.validate_sub_part({"some_array": [34]})

    def test_array_item3(self):
        self.validator.validate_sub_part(
            {"some_array": [{"KEY1": {"subKEY1": "string", "subKEY2": 45}}]}
        )

    def test_array_item_not_given_in_list(self):
        from jsonschema import ValidationError

        with self.assertRaises(ValidationError):
            self.validator.validate_sub_part(
                {"some_array": "some_string_not_in_an_array"}
            )

    def test_array_item_wrong_type(self):
        from jsonschema import ValidationError

        with self.assertRaises(ValidationError):
            self.validator.validate_sub_part({"some_array": [[[1]]]})


class TestCustomValidator(TestSchemaValidation):
    @staticmethod
    def is_set(checker, instance):
        return isinstance(instance, set)

    schema = {
        "properties": {"some_string": {"type": "string"}, "some_set": {"type": "set"}}
    }
    item = {"some_string": "abc", "some_set": {"a", "b", "c"}}

    def test_with_standard_validator(self):
        from aws_schema import SchemaValidator
        from jsonschema.exceptions import UnknownType

        validator = SchemaValidator(raw=self.schema)
        with self.assertRaises(UnknownType):
            validator.validate(self.item)

    def test_with_custom_validator(self):
        from jsonschema.validators import Draft7Validator, extend
        from aws_schema import SchemaValidator

        custom_validator = extend(
            Draft7Validator,
            type_checker=Draft7Validator.TYPE_CHECKER.redefine_many(
                {"set": self.is_set}
            ),
        )

        validator = SchemaValidator(raw=self.schema, custom_validator=custom_validator)
        validator.validate(self.item)

    def test_part_with_custom_validator(self):
        from jsonschema.validators import Draft7Validator, extend
        from aws_schema import SchemaValidator

        custom_validator = extend(
            Draft7Validator,
            type_checker=Draft7Validator.TYPE_CHECKER.redefine_many(
                {"set": self.is_set}
            ),
        )

        validator = SchemaValidator(raw=self.schema, custom_validator=custom_validator)
        validator.validate_sub_part({"some_set": self.item["some_set"]})
