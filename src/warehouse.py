import copy

from src.useful_func import obt_value_json
from src.status_warehouse.Container.column import Column
from src.status_warehouse.Container.carousel import Carousel


class Warehouse:
    def __init__(self):
        self.__height = obt_value_json("height_warehouse")
        self.__container = []
        self.__carousel = Carousel(self.__height, 0)

    def __deepcopy__(self):
        copy_instance = Warehouse()
        copy_instance.__carousel = copy.deepcopy(self.get_carousel())
        copy_instance.__container = copy.deepcopy(self.get_container())
        return copy_instance

    def get_height(self) -> int:
        return self.__height

    def get_container(self) -> list[Column]:
        return self.__container

    def get_carousel(self) -> Carousel:
        return self.__carousel

    def add_container(self, container: Column):
        self.get_container().append(container)
