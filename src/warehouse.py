from src.drawer import Drawer
from src.material import Material
from src.useful_func import obt_value_json
from src.status_warehouse.Container.column import Column
from src.status_warehouse.Container.carousel import Carousel
from src.status_warehouse.Entry.drawerEntry import DrawerEntry


class Warehouse:
    def __init__(self):
        self.__height = obt_value_json("height_warehouse")

        # TODO: to rmv DEBUG
        material = Material(123, "name", 256, 789, 12345)
        material2 = Material(234, "abc", 126, 987, 00000)
        drawer = Drawer([material, material2])
        material3 = Material(567, "def", 128, 564, 0)
        drawer2 = Drawer([material3])
        container_left = Column(self.__height, 1)
        container_left.add_drawer(0, drawer)
        print("------------------------------------------------------")
        print(container_left.get_container())
        print("------------------------------------------------------")
        print(container_left.check_minimum_space(drawer2.get_max_num_space()))
        container_left.remove_drawer(drawer)
        print("------------------------------------------------------")
        print(container_left.get_container())
        print("------------------------------------------------------")
        print(container_left.check_minimum_space(drawer2.get_max_num_space()))
        container_left = Carousel(self.__height, 1)
        container_left.add_drawer(True, drawer)
        print("------------------------------------------------------")
        print(container_left.get_container())
        print("------------------------------------------------------")
        container_left.remove_drawer(drawer)
        print("------------------------------------------------------")
        print(container_left.get_container())
        print("------------------------------------------------------")
        container_left.add_drawer(False, drawer2)
        print("------------------------------------------------------")
        print(container_left.get_container())
        print("------------------------------------------------------")

        self.__container_left = Column(self.__height, 1)
        self.__container_right = Column(self.__height, 0)
        self.__carousel_right = Carousel(self.__height, 0)

    def get_height(self) -> int:
        return self.__height
