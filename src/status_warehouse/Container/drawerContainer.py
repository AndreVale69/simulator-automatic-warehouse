from abc import abstractmethod
from src.useful_func import obt_value_json
from src.drawer import Drawer
from src.status_warehouse.Entry.emptyEntry import EmptyEntry
from src.status_warehouse.Entry.drawerEntry import DrawerEntry


class DrawerContainer:
    def __init__(self, pos_x: int):
        # initialize main vars
        self.__container = []
        self.__height = obt_value_json("height_warehouse")
        self.def_space = obt_value_json("default_height_space")
        self.__storage = obt_value_json("storage_height") // self.get_def_space()
        self.__hole = obt_value_json("hole_height") // self.get_def_space()
        self.__deposit = obt_value_json("deposit_height") // self.get_def_space()
        self.__buffer = obt_value_json("buffer_height") // self.get_def_space()
        self.__num_entries = self.get_height() // self.get_def_space()
        self.__pos_x = pos_x

    def get_height(self) -> int:
        return self.__height

    def get_def_space(self) -> int:
        return self.def_space

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

    def get_storage(self) -> int:
        return self.__storage

    def get_hole(self) -> int:
        return self.__hole

    def set_num_entries(self, num_entries: int):
        self.__num_entries = num_entries

    @abstractmethod
    def add_drawer(self, index: int, drawer: Drawer):
        pass

    def remove_drawer(self, drawer: Drawer):
        occurrence = 0

        try:
            # finding the first occurrence
            # search inside the column
            for i in range(len(self.get_container())):
                # if an element of the column is DrawerEntry, so the drawer is full...
                if isinstance(self.get_container()[i], DrawerEntry):
                    # ... and if the DrawerEntry object is linked to the same drawer object
                    # TODO
                    # fix DrawerEntry.get_drawer(self.get_container()[i])
                    # with self.get_container()[i].get_drawer()
                    if self.get_container()[i].get_drawer() == drawer:
                        # take DrawerEntry object
                        occurrence = self.get_container()[i]
                        break
            # if there isn't any drawer raise StopIteration error!
            if occurrence == 0:
                raise StopIteration
            else:
                # search inside the column all the occurrences and substitute with EmptyEntry
                for i in range(len(self.get_container())):
                    if type(self.get_container()[i]) is type(occurrence):
                        if DrawerEntry.get_drawer(self.get_container()[i]) == DrawerEntry.get_drawer(occurrence):
                            self.get_container()[i] = EmptyEntry(occurrence.get_pos_x(), occurrence.get_pos_y())
        except StopIteration as e:
            print(str(e) + "\nNo element to remove found")
