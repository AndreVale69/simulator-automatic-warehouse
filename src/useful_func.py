import json


def obt_value_json(keyword) -> int:
    """
    Read a specific data inside JSON file.

    :param keyword: constant search inside JSON file
    :return: value found
    """

    # opening JSON file
    f = open("../rsc/info.json")

    # returns JSON object as a dictionary
    data = json.load(f)

    # closing JSON file
    f.close()

    # take const
    return data[keyword]
