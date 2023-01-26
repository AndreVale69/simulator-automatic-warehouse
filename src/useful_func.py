import json


def open_config() -> dict:
    """
    Read the configuration file
    :return: config file
    """
    # opening JSON file
    with open("../rsc/config.json", 'r') as json_file:
        # returns JSON object as a dictionary
        return json.load(json_file)
