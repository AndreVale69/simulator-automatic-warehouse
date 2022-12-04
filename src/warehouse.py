import copy

from src.useful_func import obt_value_json
from src.status_warehouse.Container.column import Column
from src.status_warehouse.Container.carousel import Carousel


class Warehouse:
    def __init__(self):
        self.__height = obt_value_json("height_warehouse")
        self.__container = []
        self.__carousel = Carousel(0)

    # def __deepcopy__(self):
    #     copy_instance = Warehouse()
    #     copy_instance.__carousel = copy.deepcopy(self.get_carousel())
    #     copy_instance.__container = copy.deepcopy(self.get_container())
    #     return copy_instance

    def __deepcopy__(self, memo):
        newone = type(self)()
        newone.__dict__.update(self.__dict__)
        self.__carousel = copy.deepcopy(self.__carousel, memo)
        self.__container = copy.deepcopy(self.__container, memo)
        return newone

    def get_height(self) -> int:
        return self.__height

    def get_container(self) -> list[Column]:
        return self.__container

    def get_carousel(self) -> Carousel:
        return self.__carousel

    def add_container(self, container: Column):
        self.get_container().append(container)
