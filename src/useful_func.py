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


def check_minimum_space(list_obj: list, space_req: int, height_warehouse: int) -> list:
    """
    Algorithm to decide where insert a drawer.

    :param list_obj: list of columns.
    :param space_req: space requested from drawer.
    :param height_warehouse: the height of warehouse
    :return: if there is a space [space_requested, index_position_where_insert, column_where_insert].
    :exception StopIteration: if there isn't any space.
    """
    result = []
    col = None

    # calculate minimum space and search lower index
    for i in range(len(list_obj)):
        values = __min_search_alg(list_obj[i], space_req)
        if values[0] != -1 & values[1] < height_warehouse:
            result = values.copy()
            col = list_obj[i]

    # if warehouse is full
    if col is None:
        raise StopIteration("No element found")
    else:
        result.append(col)
        return result


def __min_search_alg(self, space_req: int) -> list:
    """
    Algorithm to calculate a minimum space inside a column.

    :param self: object to calculate minimum space.
    :param space_req: space requested from drawer.
    :return: negative values if there isn't any space, otherwise [space_requested, index_position_where_insert].
    """
    min_space = self.get_height()
    count = 0
    start_index = 0
    container = self.get_container()

    ############################
    # Minimum search algorithm #
    ############################
    for i in range(len(container)):
        # if the position is empty
        if isinstance(container[i], EmptyEntry):
            # count number of spaces
            count += 1
        else:
            # otherwise, if it's minimum and there is enough space
            if (count < min_space) & (count >= space_req):
                # update check values
                min_space = count
                start_index = i - count
            # restart the count with reset
            count = 0

    # if warehouse is empty
    if min_space == self.get_height():
        # double security check
        for i in range(len(container)):
            # if it isn't empty
            if isinstance(container[i], Drawer):
                # raise IndexError("There isn't any space for this drawer.")
                print("A")
                return [-1, -1]
        min_space = len(container)

    # alloc only minimum space
    if min_space > space_req:
        min_space = space_req
    else:
        # otherwise there isn't any space
        if min_space < space_req:
            # raise IndexError("There isn't any space for this drawer.")
            return [-1, -1]

    return [min_space, start_index]
