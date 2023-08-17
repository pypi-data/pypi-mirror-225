from unittest import TestCase
from os import environ as os_environ
from os.path import dirname, realpath
from os import chdir, getcwd
from copy import deepcopy

reference_dict = {
    "some_string": "abcdef",
    "some_int": 42,
    "some_float": 13.42,
    "some_dict": {"key1": "value1", "key2": 2},
    "some_nested_dict": {"KEY1": {"subKEY1": "subVALUE1", "subKEY2": 42.24}},
    "some_array": [
        "array_string",
        13,
        {"KEY1": {"arraySubKEY1": "subVALUE1", "arraySubKEY2": 42.24}},
    ],
}


class TestNestedDict(TestCase):
    actual_cwd = str()

    @classmethod
    def setUpClass(cls) -> None:
        os_environ["STAGE"] = "TEST"
        os_environ["WRAPPER_CONFIG_FILE"] = "_helper_wrapper_config_empty.json"

        cls.actual_cwd = getcwd()
        chdir(dirname(realpath(__file__)))

    @classmethod
    def tearDownClass(cls) -> None:
        chdir(cls.actual_cwd)

    def setUp(self) -> None:
        self._reference_dict = deepcopy(reference_dict)

    def tearDown(self) -> None:
        global reference_dict
        reference_dict = self._reference_dict


class TestDeleteKeysInNestedDict(TestNestedDict):
    def test_delete_nothing(self):
        from aws_schema.nested_dict_helper import (
            delete_keys_in_nested_dict,
        )

        self.assertEqual(reference_dict, delete_keys_in_nested_dict(reference_dict, []))

    def test_no_supported_delete_type(self):
        from aws_schema.nested_dict_helper import (
            delete_keys_in_nested_dict,
        )

        with self.assertRaises(TypeError) as TE:
            self.assertEqual(
                reference_dict,
                delete_keys_in_nested_dict(reference_dict, "some string"),
            )
        self.assertEqual(
            ("dict_keys_to_delete must be a list, given some string",),
            TE.exception.args,
        )

    def test_delete_top_level(self):
        from aws_schema.nested_dict_helper import (
            delete_keys_in_nested_dict,
        )

        to_deleted_dict = deepcopy(reference_dict)
        delete_keys_in_nested_dict(to_deleted_dict, ["some_float"])

        reference_dict.pop("some_float")

        self.assertEqual(reference_dict, to_deleted_dict)

    def test_delete_in_sub_dict(self):
        from aws_schema.nested_dict_helper import (
            delete_keys_in_nested_dict,
        )

        to_deleted_dict = deepcopy(reference_dict)
        delete_keys_in_nested_dict(to_deleted_dict, ["subKEY1"])

        reference_dict["some_nested_dict"]["KEY1"].pop("subKEY1")

        self.assertEqual(reference_dict, to_deleted_dict)

    def test_delete_in_array_contained_dict(self):
        from aws_schema.nested_dict_helper import (
            delete_keys_in_nested_dict,
        )

        to_deleted_dict = deepcopy(reference_dict)
        delete_keys_in_nested_dict(to_deleted_dict, ["arraySubKEY1"])

        reference_dict["some_array"][2]["KEY1"].pop("arraySubKEY1")

        self.assertEqual(reference_dict, to_deleted_dict)


class TestFindAllPathsInDict(TestNestedDict):
    def test_find_paths(self):
        from aws_schema.nested_dict_helper import find_path_values_in_dict

        expected_paths = [
            ["some_string"],
            ["some_int"],
            ["some_float"],
            ["some_dict", "key1"],
            ["some_dict", "key2"],
            ["some_nested_dict", "KEY1", "subKEY1"],
            ["some_nested_dict", "KEY1", "subKEY2"],
            ["some_array"],
        ]
        expected_values = [
            "abcdef",
            42,
            13.42,
            "value1",
            2,
            "subVALUE1",
            42.24,
            [
                "array_string",
                13,
                {"KEY1": {"arraySubKEY1": "subVALUE1", "arraySubKEY2": 42.24}},
            ],
        ]
        found_paths, found_values = find_path_values_in_dict(reference_dict)

        self.assertEqual(expected_paths, found_paths)
        self.assertEqual(expected_values, found_values)


class TestNewPathsInDict(TestNestedDict):
    def test_find_no_new_attribute(self):
        origin = {"1": {"2": {"3": 4}}}
        new_data = {"1": {"2": {"3": 4}}}

        from aws_schema.nested_dict_helper import find_new_paths_in_dict

        paths, values = find_new_paths_in_dict(origin, new_data)
        assert paths == []
        assert values == []

    def test_find_no_new_path_only_new_attribute(self):
        origin = {"1": {"2": {"3": 4}}}
        new_data = {"1": {"2": {"3": 5}}}

        from aws_schema.nested_dict_helper import find_new_paths_in_dict

        paths, values = find_new_paths_in_dict(origin, new_data)
        assert paths == [["1", "2", "3"]]
        assert values == [5]

    def test_find_single_new_path(self):
        origin = {"1": {"2": {"3": 4}}}
        new_data = {"1": {"2a": {"3a": 55}}}

        from aws_schema.nested_dict_helper import find_new_paths_in_dict

        paths, values = find_new_paths_in_dict(origin, new_data)
        assert paths == [["1", "2a"]]
        assert values == [{"3a": 55}]

    def test_find_multiple_new_paths(self):
        origin = {"1": {"2": {"3": 4}}}
        new_data = {"1": {"2a": {"3a": 55}, "2b": {"3b": 678}}}

        from aws_schema.nested_dict_helper import find_new_paths_in_dict

        paths, values = find_new_paths_in_dict(origin, new_data)
        assert paths == [["1", "2a"], ["1", "2b"]]
        assert values == [{"3a": 55}, {"3b": 678}]

    def test_find_new_and_existing_paths(self):
        origin = {"1": {"2": {"3": 4}}}
        new_data = {"1": {"2": {"3": 45}, "2a": {"3a": 55}, "2b": {"3b": 678}}}
        from aws_schema.nested_dict_helper import find_new_paths_in_dict

        paths, values = find_new_paths_in_dict(origin, new_data)
        assert paths == [["1", "2", "3"], ["1", "2a"], ["1", "2b"]]
        assert values == [45, {"3a": 55}, {"3b": 678}]

    def test_find_new_and_existing_paths_additional_one_no_new_attribute(self):
        origin = {"1": {"2": {"3": 4, "z": 0}}}
        new_data = {"1": {"2": {"3": 45, "z": 0}, "2a": {"3a": 55}, "2b": {"3b": 678}}}
        from aws_schema.nested_dict_helper import find_new_paths_in_dict

        paths, values = find_new_paths_in_dict(origin, new_data)
        assert paths == [["1", "2", "3"], ["1", "2a"], ["1", "2b"]]
        assert values == [45, {"3a": 55}, {"3b": 678}]
