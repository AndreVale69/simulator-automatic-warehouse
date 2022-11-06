from abc import ABC, abstractmethod
from src.useful_func import read_value_of_const_json


class DrawerContainer(ABC):
    def __init__(self, height: int):
        def_space = read_value_of_const_json("default_height_space")
        self.__height = height
        self.__num_entries = self.__height // def_space

    def get_height(self) -> int:
        return self.__height

    def get_num_entries(self) -> int:
        return self.__num_entries

    @abstractmethod
    def add_drawer(self):
        pass

    @abstractmethod
    def remove_drawer(self):
        pass
