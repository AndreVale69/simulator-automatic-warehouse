import json


def read_value_of_const_json(keyword):
    """
    Read a specific data inside JSON file.
    :param keyword: constant search inside JSON file.
    :return: constant.
    """
    # opening JSON file
    f = open("../resource/info.json")

    # returns JSON object as a dictionary
    data = json.load(f)

    # closing JSON file
    f.close()

    # take const
    return data[keyword]
