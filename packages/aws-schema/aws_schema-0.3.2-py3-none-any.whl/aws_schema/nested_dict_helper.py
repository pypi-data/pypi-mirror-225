def delete_keys_in_nested_dict(nested: (dict, list), dict_keys_to_delete: list):
    """
    Delete keys in a nested dict. If nested is neither a dict or a dict in a list, skipped.
    Tuples and sets are not covered

    Parameters
    ----------
    nested : dict, list
    dict_keys_to_delete : list

    Returns
    -------

    """

    if not isinstance(dict_keys_to_delete, list):
        raise TypeError(
            f"dict_keys_to_delete must be a list, given {dict_keys_to_delete}"
        )

    if isinstance(nested, list):
        for i in range(len(nested)):
            nested[i] = delete_keys_in_nested_dict(nested[i], dict_keys_to_delete)
    elif isinstance(nested, dict):
        for key in nested.copy():
            if key in dict_keys_to_delete:
                del nested[key]
            else:
                nested[key] = delete_keys_in_nested_dict(
                    nested[key], dict_keys_to_delete
                )
    return nested


def find_path_values_in_dict(
    data: dict, current_path=None, all_paths=None, all_values=None
):
    if all_values is None:
        all_values = list()
    if all_paths is None:
        all_paths = list()
    if current_path is None:
        current_path = list()
    if isinstance(data, dict):
        for key, value in data.items():
            current_path.append(key)
            if isinstance(value, dict):
                find_path_values_in_dict(value, current_path, all_paths, all_values)
            else:
                all_paths.append(current_path.copy())
                all_values.append(value)
                current_path.pop(-1)
    try:
        current_path.pop(-1)
    except IndexError:
        pass
    return all_paths, all_values


def find_new_paths_in_dict(
    origin: dict, new_data: dict, current_path=None, all_paths=None, all_values=None
):

    if not current_path:
        current_path = list()
    if all_paths is None:
        all_paths = list()
    if not all_values:
        all_values = list()

    if isinstance(new_data, dict):
        for key in new_data:
            current_path.append(key)
            if key in origin:
                all_paths, all_values = find_new_paths_in_dict(
                    origin[key], new_data[key], current_path, all_paths, all_values
                )
            else:
                all_paths.append(current_path.copy())
                all_values.append(new_data[key])
            current_path.pop(-1)
    elif new_data != origin:
        all_paths.append(current_path.copy())
        all_values.append(new_data)

    return all_paths, all_values
