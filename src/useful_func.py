import json
from src.drawer import Drawer
from src.status_warehouse.Entry.drawerEntry import DrawerEntry
from src.status_warehouse.Entry.emptyEntry import EmptyEntry


def obt_value_json(keyword: str) -> int:
    """
    Read a specific data inside JSON file.

    :param keyword: constant search inside JSON file.
    :return: value found.
    :exception KeyError: value not found.
    """

    # opening JSON file
    with open("../rsc/config.json", 'r') as json_file:
        # returns JSON object as a dictionary
        json_data = json.load(json_file)

    # jsonpath_expression = parse()

    # closing JSON file
    json_file.close()

    try:
        # if the value isn't inside a list
        if keyword in json_data:
            return json_data[keyword]
        else:
            # for each element inside the dictionary
            for i in json_data:
                # manipulate list element
                if isinstance(json_data[i], list):
                    for j in range(len(json_data[i])):
                        # each element of the list is a dictionary type, so try to find the element
                        if keyword in json_data[i][j]:
                            return json_data[i][j][keyword]
                else:
                    # manipulate dictionary element
                    if isinstance(json_data[i], dict):
                        # try to find the element
                        if keyword in json_data[i]:
                            return json_data[i][keyword]
    except KeyError as e:
        print(str(e) + "\nValue not found")


def search_drawer(list_obj: list, drawer: Drawer) -> DrawerEntry:
    """
    Search first drawer in relationship with drawer parameter.

    :param list_obj: list of columns.
    :param drawer: drawer in relationship with DrawerEntry to search.
    :return: object in relationship with drawer
    """
    from src.status_warehouse.Container.column import Column

    for j in range(len(list_obj)):
        for i in range(len(Column.get_container(list_obj[j]))):
            if isinstance(Column.get_container(list_obj[j])[i], DrawerEntry):
                if DrawerEntry.get_drawer(Column.get_container(list_obj[j])[i]) == drawer:
                    return Column.get_container(list_obj[j])[i]

    raise StopIteration("No element found")


def check_minimum_space(list_obj: list, space_req: int) -> list:
    """
    Algorithm to decide where insert a drawer.

    :param list_obj: list of columns.
    :param space_req: space requested from drawer.
    :return: if there is a space [space_requested, index_position_where_insert, column_where_insert].
    :exception StopIteration: if there isn't any space.
    """
    result = []
    col = None
    min_index = obt_value_json("height_warehouse") // obt_value_json("default_height_space")

    # calculate minimum space and search lower index
    for i in range(len(list_obj)):
        values = __min_search_alg(list_obj[i], space_req)
        if values[0] != -1 & values[1] < min_index:
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
    for i in range(len(container) + 1):
        if i != len(container):
            # count number of space
            if isinstance(container[i], EmptyEntry):
                count = count + 1
            else:
                # otherwise, if its minimum and there is enough space
                if (count < min_space) & (count >= space_req):
                    min_space = count
                    start_index = i - count
                # restart the count with reset
                count = 0
        else:
            if (count < min_space) & (count >= space_req):
                min_space = count
                start_index = i - count
            # restart the count with reset
            count = 0  # TODO: check eventually rmv

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
