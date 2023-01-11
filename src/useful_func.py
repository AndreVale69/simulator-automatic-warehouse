import json

from src.drawer import Drawer
from src.status_warehouse.Entry.emptyEntry import EmptyEntry


def open_config() -> dict:
    """
    Read the config file
    :return: config file
    """
    # opening JSON file
    with open("../rsc/config.json", 'r') as json_file:
        # returns JSON object as a dictionary
        return json.load(json_file)


def check_minimum_space(list_obj: list, space_req: int, height_entry_col: int) -> list:
    """
    Algorithm to decide where insert a drawer.

    :param list_obj: list of columns.
    :param space_req: space requested from drawer.
    :param height_entry_col: the height of warehouse
    :return: if there is a space [space_requested, index_position_where_insert, column_where_insert].
    :exception StopIteration: if there isn't any space.
    """
    result = []
    col = None

    # calculate minimum space and search lower index
    for column in list_obj:
        [min_space, start_index] = min_search_alg(column, space_req)
        if min_space != -1 and start_index < height_entry_col:
            result = [min_space, start_index]
            col = column

    # if warehouse is full
    if col is None:
        raise StopIteration("No space found.")
    else:
        result.append(col)
        return result


def min_search_alg(self, space_req: int) -> list:
    """
    Algorithm to calculate a minimum space inside a column.

    :param self: object to calculate minimum space.
    :param space_req: space requested from drawer.
    :return: negative values if there isn't any space, otherwise [space_requested, index_position_where_insert].
    """
    min_space = self.get_height_warehouse()
    count = 0
    start_index = 0
    container = self.get_container()
    index = 0

    ############################
    # Minimum search algorithm #
    ############################
    for entry in container:
        index += 1
        # if the position is empty
        if type(entry) is EmptyEntry:
            # count number of spaces
            count += 1
        else:
            # otherwise, if it's minimum and there is enough space
            if (count < min_space) & (count >= space_req):
                # update check values
                min_space = count
                start_index = index - count
            # restart the count with reset
            count = 0

    # if warehouse is empty
    if min_space == self.get_height_warehouse():
        if count == 0:
            # double security check
            for i in range(len(container)):
                # if it isn't empty
                if type(container[i]) is Drawer:
                    # raise IndexError("There isn't any space for this drawer.")
                    print("A")
                    return [-1, -1]
            min_space = len(container)
        else:
            # update check values
            min_space = count
            start_index = index - count


    # alloc only minimum space
    if min_space >= space_req:
        min_space = space_req
    else:
        # otherwise there isn't any space
        if min_space < space_req:
            # raise IndexError("There isn't any space for this drawer.")
            return [-1, -1]

    return [min_space, start_index]
