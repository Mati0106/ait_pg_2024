import json

class Configuration(json.JSONEncoder):
    features_names: list
    prediction_column: str
    prediction_categories: list
    data_split_random_state: int
    smote_random_state: int

    def __init__(self, features_names: list = None, prediction_column: str = None, prediction_categories: list = None, data_split_random_state: int = 0, smote_random_state: int = 0):
        self.features_names = features_names
        self.prediction_categories = prediction_categories
        self.prediction_column = prediction_column
        self.data_split_random_state = data_split_random_state
        self.smote_random_state = smote_random_state

    def save_to_file(self, file: str):
        with open(file, 'w') as fp:
            json.dump(self, fp, cls=ConfigurationEncoder, indent=1)

class ConfigurationEncoder(json.JSONEncoder):
    def default(self, o: Configuration):
        return {
            'data_split_random_state': o.data_split_random_state,
            'smote_random_state': o.smote_random_state,
            'features_names': o.features_names,
            'prediction_column': o.prediction_column,
            'prediction_categories': o.prediction_categories,
        }


def load_config(file: str) -> Configuration:
    with open(file, 'r') as fp:
        return json.load(fp, object_hook=lambda d: Configuration(**d))
