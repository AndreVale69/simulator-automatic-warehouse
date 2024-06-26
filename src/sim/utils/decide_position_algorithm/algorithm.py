from typing import NamedTuple

from src.sim.status_warehouse.container.column import Column
from src.sim.status_warehouse.entry.empty_entry import EmptyEntry
from src.sim.utils.decide_position_algorithm.enum_algorithm import Algorithm


class DecidePositionReturns(NamedTuple):
    index: int
    column: Column


def decide_position(columns: list[Column], space_req: int, algorithm: Algorithm) -> DecidePositionReturns:
    """
    Run the algorithm to decide where to insert a drawer.
    It returns a NamedTuple where we can find the index and the best column.
    The index that you can use, for example, as a parameter in the add_column method.

    :type columns: list[Column]
    :type space_req: int
    :type algorithm: Algorithm
    :rtype: DecidePositionReturns
    :param columns: the columns checked by the algorithm to find the best position.
    :param space_req: space requested from drawer.
    :param algorithm: algorithm used.
    :return: if there is a space [index_position_where_insert, column_where_insert].
    :raises NotImplementedError: if the algorithm is not implemented.
    :raises ValueError: if the algorithm cannot find a position for the space requested.
    """
    assert len(columns) > 0, "At least one column is required."

    # select the algorithm to be used
    match algorithm:
        case algorithm.HIGH_POSITION:
            callable_algorithm = _high_position_algorithm
        case _:
            raise NotImplementedError("Algorithm not implemented")

    # calculate the index of the first column
    min_index = callable_algorithm(columns[0], space_req)
    col_min_index = columns[0]
    # finally, calculate and find the min of the other columns
    for i in range(1, len(columns)):
        col = columns[i]
        col_index = callable_algorithm(col, space_req)
        if col_index < min_index:
            min_index = col_index
            col_min_index = col

    return DecidePositionReturns(min_index, col_min_index)


def _high_position_algorithm(column: Column, space_req: int) -> int:
    """
    This algorithm prefers the top position of the column.
    So it returns the highest position (index) of the column given a space (space_req parameter).

    :type column: Column
    :type space_req: int
    :rtype: int
    :param column: the column where we want to find the best position.
    :param space_req: space required for the drawer.
    :return: the highest position (index) of the column given a space (space_req parameter).
    :raise ValueError: if the algorithm cannot find a position for the space requested.
    """
    start_index = height_last_pos = column.get_height_last_position()
    container = column.get_container()

    # verify the highest position:
    # - if the first available entry in the last position is empty (-1 because the start index is 0 and not 1)
    # - if the space required for the drawer is less than or equal to the height of the last position
    if type(container[start_index - 1]) is EmptyEntry and space_req <= height_last_pos:
        # take the highest position (from the top) as index
        return start_index - space_req

    # immediately after the highest position, iterate each entry
    count_empty_entries = 0
    for index in range(start_index, len(container)):
        # if the position is not empty, move forward
        if type(container[index]) is not EmptyEntry:
            count_empty_entries = 0
            continue
        # if the position is empty, increment the counter
        count_empty_entries += 1
        # and check if the space can be filled
        if count_empty_entries >= space_req:
            return (index - count_empty_entries) + 1

    # if no position found
    raise ValueError("No more space in the warehouse!")
