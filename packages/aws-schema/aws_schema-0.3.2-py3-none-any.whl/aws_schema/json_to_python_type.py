from ast import literal_eval

json_to_python_type_switch = {
    "array": list,
    "boolean": bool,
    "string": str,
    "object": dict,
    "number": float,
    "integer": int,
}

json_to_python_type_convert = {
    "array": literal_eval,
    "boolean": bool,
    "string": str,
    "object": literal_eval,
    "number": float,
    "integer": int,
}
