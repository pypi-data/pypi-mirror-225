import json


def load_json_file(file_name):
    with open(file_name, "r") as f:
        return json.load(f)


def load_all(directory_name):
    import glob

    file_names = glob.glob(f"{directory_name}/*.json")
    files = {}
    for file in file_names:
        files[file] = load_json_file(file)
    return files
