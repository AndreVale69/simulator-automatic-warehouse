# TODO Library will remove
import numpy as np

# Default variables
__height_btw_drawers = 25

def create_left_column(data_column: np.ndarray):
    data_column = np.insert(data_column, 0, ("Drawer", 100))

    i = 1
    for i in range(18):
        data_column = np.insert(data_column, i, ("Space", __height_btw_drawers))
        print("prova")

    data_column = np.insert(data_column, 18, ("Drawer", 200))
    data_column = np.insert(data_column, 19, ("Drawer", 50))

    index = 20
    for index in range(index + 27):
        data_column = np.insert(data_column, index, ("Space", __height_btw_drawers))

    return data_column


def create_right_column(data_column: np.ndarray):
    data_column = np.array([("Drawer", 100)])
    return data_column