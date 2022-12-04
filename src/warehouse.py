import copy

from src.useful_func import obt_value_json
from src.status_warehouse.Container.column import Column
from src.status_warehouse.Container.carousel import Carousel


class Warehouse:
    def __init__(self):
        self.height = obt_value_json("height_warehouse")
        self.container = []
        self.carousel = Carousel(0)

    # def __deepcopy__(self):
    #     copy_instance = Warehouse()
    #     copy_instance.__carousel = copy.deepcopy(self.get_carousel())
    #     copy_instance.__container = copy.deepcopy(self.get_container())
    #     return copy_instance

    def __deepcopy__(self, memo):
        newone = type(self)()
        newone.__dict__.update(self.__dict__)
        self.carousel = copy.deepcopy(self.carousel, memo)
        self.container = copy.deepcopy(self.container, memo)
        return newone

    def get_height(self) -> int:
        return self.height

    def get_container(self) -> list[Column]:
        return self.container

    def get_carousel(self) -> Carousel:
        return self.carousel

    def add_container(self, container: Column):
        self.get_container().append(container)
