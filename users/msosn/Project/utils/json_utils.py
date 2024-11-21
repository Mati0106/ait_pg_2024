import json

def save_to_json_file(file: str, dictionary: dict):
    """
    Save dictionary to given json file
    :param file: file path
    :param dictionary:
    """
    with open(file, "w") as fp:
        json.dump(dictionary, fp, indent=1)

def load_from_json_file(file: str) -> dict:
    """
    Load dictionary from given json file
    :param file: path to file
    :return:
    """
    with open(file, "r") as fp:
        return json.load(fp)

