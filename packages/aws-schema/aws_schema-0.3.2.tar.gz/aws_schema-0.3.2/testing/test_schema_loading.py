from unittest import TestCase
from os.path import dirname, realpath

from testing import load_json_file


class TestSchemaLoadingFromFile(TestCase):
    def test_load_basic_schema(self):
        from aws_schema.schema_validator import (
            SchemaValidator,
        )

        schema_file = (
            f"{dirname(realpath(__file__))}/test_data/database/schema_basic.json"
        )

        expected_schema = load_json_file(schema_file)

        validator = SchemaValidator(file=schema_file)
        loaded_schema = validator.schema
        self.assertEqual(expected_schema, loaded_schema)

    def test_load_nested_schema(self):
        from aws_schema.schema_validator import (
            SchemaValidator,
        )

        base_schema_file = (
            f"{dirname(realpath(__file__))}/test_data/database/schema_nested.json"
        )

        expected_schema = load_json_file(base_schema_file)

        validator = SchemaValidator(file=base_schema_file)
        loaded_schema = validator.schema

        self.assertEqual(expected_schema, loaded_schema)


class TestSchemaLoadingFromURL(TestCase):
    pass
