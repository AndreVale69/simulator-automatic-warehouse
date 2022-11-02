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

    # list of const
    val_list = list(dict.values(data))

    # take const
    index = 0
    for i in val_list[0]:
        keys = list(dict.keys(i))
        if keys[0] == keyword:
            return val_list[0][index][keyword]
        index = index + 1

    raise ValueError("Key no found.")
