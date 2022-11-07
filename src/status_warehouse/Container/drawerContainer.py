from abc import abstractmethod, ABC
from src.useful_func import read_value_of_const_json
from src.status_warehouse.Entry.emptyEntry import EmptyEntry
from src.drawer import Drawer


class DrawerContainer:
    def __init__(self, height: int):
        # initialize main vars
        self.__container = []
        self.__height = height
        self.__num_entries = self.__height // read_value_of_const_json("default_height_space")

        # create container
        for i in range(self.__num_entries):
            self.__container.append(EmptyEntry())

    def get_height(self) -> int:
        return self.__height

    def get_num_entries(self) -> int:
        return self.__num_entries

    def get_container(self) -> list:
        return self.__container

    @abstractmethod
    def add_drawer(self, index: int, drawer: Drawer):
        pass

    @abstractmethod
    def remove_drawer(self, drawer: Drawer):
        pass
