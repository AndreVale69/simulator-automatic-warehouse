from abc import abstractmethod
from src.useful_func import obt_value_json
from src.drawer import Drawer
from src.status_warehouse.Entry.emptyEntry import EmptyEntry
from src.status_warehouse.Entry.drawerEntry import DrawerEntry


class DrawerContainer:
    def __init__(self, height: int, pos_x: int):
        # initialize main vars
        self.__container = []
        self.__height = height
        def_space = obt_value_json("default_height_space")
        self.__num_entries = self.__height // def_space
        self.__buffer = obt_value_json("buffer_height") // def_space
        self.__deposit = obt_value_json("deposit_height") // def_space
        self.__pos_x = pos_x

        # create container
        for i in range(self.__num_entries):
            self.__container.append(EmptyEntry(i, self.__pos_x))

    def get_height(self) -> int:
        return self.__height

    def get_num_entries(self) -> int:
        return self.__num_entries

    def get_container(self) -> list:
        return self.__container

    def get_buffer(self) -> int:
        return self.__buffer

    def get_deposit(self) -> int:
        return self.__deposit

    def get_pos_x(self) -> int:
        return self.__pos_x

    @abstractmethod
    def add_drawer(self, index: int, drawer: DrawerEntry):
        pass

    def remove_drawer(self, drawer: Drawer):
        occurrence = 0

        try:
            # finding the first occurrence
            for i in range(len(self.get_container())):
                if isinstance(self.get_container()[i], DrawerEntry):
                    if DrawerEntry.get_drawer(self.get_container()[i]) == drawer:
                        occurrence = self.get_container()[i]
                        break
            # if there isn't any drawer -> error!
            if occurrence == 0:
                raise StopIteration
            else:
                for i in range(len(self.get_container())):
                    if self.get_container()[i] == occurrence:
                        self.get_container()[i] = EmptyEntry(occurrence.get_pos_x(), occurrence.get_pos_y())

        except StopIteration as e:
            print(str(e) + "\nNo element to remove found")
