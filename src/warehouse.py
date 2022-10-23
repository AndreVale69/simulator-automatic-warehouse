import numpy as np
from src.drawer import Drawer


class Warehouse(object):
    __type = np.dtype([("name", "U30"), ("height", "uint32"), ("drawer", Drawer)])
    __warehouse = np.array([], dtype=__type)
    __height = 0

    def set_height(self, height: int):
        self.__height = height

    def get_height(self):
        return self.__height

    def get_warehouse(self):
        return self.__warehouse

    def add_drawer(self, drawer: Drawer, pos: int):
        self.__warehouse = np.insert(self.__warehouse, pos, ("drawer", drawer.get_max_height(), drawer))

    # TODO: debug
    def print_warehouse(self):
        print(self.__warehouse)
