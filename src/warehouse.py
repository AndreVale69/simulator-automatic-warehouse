import numpy as np
from src.drawer import Drawer


class Warehouse(object):
    # __type = np.dtype([("name", "U30"), ("drawer", Drawer)])
    # __warehouse = np.array([], dtype=__type)
    __warehouse = []
    __height = 0

    def __init__(self, height: int = 0):
        self.__height = height

    def set_height(self, height: int):
        self.__height = height

    def get_height(self):
        return self.__height

    def get_warehouse(self):
        return self.__warehouse

    def add_drawer(self, drawer: Drawer):
        self.__warehouse.append(drawer)

    # TODO: debug
    def print_warehouse(self):
        print(self.__warehouse)

