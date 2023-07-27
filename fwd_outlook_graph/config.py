import json

def load_config(config_file_path):
    with open(config_file_path) as config_file:
        return json.load(config_file)