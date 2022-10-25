import numpy as np
from src.drawer import Drawer


class Warehouse(object):
    # __type = np.dtype([("name", "U30"), ("drawer", Drawer)])
    # __warehouse = np.array([], dtype=__type)
    __warehouse = []
    __height = 0
    __minimum_height = 500

    def __init__(self, height: int):
        self.__height = height

        # error
        if height < self.__minimum_height:
            raise ValueError("The height is too low, please digit a value grater/equal than " +
                             str(self.__minimum_height))

        # creation of space
        num_space = height // 25
        for i in range(num_space):
            self.__warehouse.append(25)

    def set_height(self, height: int):
        self.__height = height

    def get_height(self):
        return self.__height

    def get_warehouse(self):
        return self.__warehouse

    def add_drawer(self, drawer: Drawer):
        self.__count_minimum_space(drawer.get_max_height())
        self.__warehouse.append(drawer)

    # TODO: to finish
    def __count_minimum_space(self, request):
        if (request % 25) == 0:
            effective_req = request // 25
        else:
            effective_req = (request // 25) + 1

        min = len(self.__warehouse)
        count = 0

        for i in range(len(self.__warehouse) - 1):
            if (self.__warehouse[i] == 25) & (self.__warehouse[i + 1] == 25):
                count = count + 1
            else:
                if count < min:
                    min = count
                    index = i - count

                count = 0


    # TODO: debug
    def print_warehouse(self):
        print(self.__warehouse)
