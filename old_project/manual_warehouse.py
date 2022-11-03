# TODO Library will remove
import numpy as np

# Default variables
__height_btw_drawers = 25


def create_left_column(data_column: np.ndarray):
    data_column = np.insert(data_column, 0, ("Drawer", 100))

    i = 1
    while i < 18:
        data_column = np.insert(data_column, i, ("Space", __height_btw_drawers))
        i += 1

    # i = 18    

    data_column = np.insert(data_column, i, ("Drawer", 200))
    i += 1  # = 19
    data_column = np.insert(data_column, i, ("Drawer", 200))
    i += 1  # = 20

    while i < 27:
        data_column = np.insert(data_column, i, ("Space", __height_btw_drawers))
        i += 1

    return data_column


def create_right_column(data_column: np.ndarray):
    i = 0
    data_column = np.insert(data_column, i, ("Storage", 100))

    i += 1  # = 1

    data_column = np.insert(data_column, i, ("Buffer", 100))

    i += 1  # = 2

    data_column = np.insert(data_column, i, ("Hole", 500))

    i += 1  # = 3

    data_column = np.insert(data_column, i, ("Drawer", 100))

    i += 1  # = 4

    data_column = np.insert(data_column, i, ("Drawer", 300))

    return data_column
