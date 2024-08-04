from dataclasses import dataclass

from automatic_warehouse.status_warehouse.container.column import Column
from automatic_warehouse.status_warehouse.entry.empty_entry import EmptyEntry
from automatic_warehouse.utils.decide_position_algorithm.enum_algorithm import Algorithm


@dataclass
class DecidePositionReturns:
    """ `Python Dataclass <https://docs.python.org/3/library/dataclasses.html>`_ - 
    It is the return value of the :attr:`decide_position <automatic_warehouse.utils.decide_position_algorithm.algorithm.decide_position>` function. """

    index: int
    """ Index position where the tray is to be placed. """

    column: Column
    """ Column on which the tray is to be placed. """



def decide_position(columns: list[Column], space_req: int, algorithm: Algorithm) -> DecidePositionReturns:
    """
    Run the algorithm to decide where to insert a tray.
    It returns :class:`DecidePositionReturns` dataclass where you can find the index and the best column.

    :type columns: list[Column]
    :type space_req: int
    :type algorithm: Algorithm
    :rtype: DecidePositionReturns
    :param columns: the columns checked by the algorithm to find the best position.
    :param space_req: space requested from tray.
    :param algorithm: algorithm used.
    :return: if there is a space, dataclass with the fields ``index_position_where_insert``, ``column_where_insert``.
    :raises NotImplementedError: if the algorithm is not implemented.
    :raises ValueError: if the algorithm cannot find a position for the space requested.
    """
    assert len(columns) > 0, "At least one column is required."
    assert space_req > 0, "The space requested from the tray must be greater than zero."

    # select the algorithm to be used
    if algorithm == algorithm.HIGH_POSITION:
        callable_algorithm = _high_position_algorithm
    else:
        raise NotImplementedError("Algorithm not implemented")

    # calculate the index of the first column
    first_column = columns[0]
    min_index = callable_algorithm(first_column, space_req)
    col_min_index = first_column
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
    :param space_req: space required for the tray.
    :return: the highest position (index) of the column given a space (space_req parameter).
    :raise ValueError: if the algorithm cannot find a position for the space requested.
    """
    start_index = height_last_pos = column.get_height_last_position()
    container = column.get_container()

    # verify the highest position:
    # - if the first available entry in the last position is empty (-1 because the start index is 0 and not 1)
    # - if the space required for the tray is less than or equal to the height of the last position
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
