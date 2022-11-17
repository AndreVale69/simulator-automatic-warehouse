from abc import abstractmethod
from src.useful_func import obt_value_json
from src.drawer import Drawer
from src.status_warehouse.Entry.emptyEntry import EmptyEntry
from src.status_warehouse.Entry.drawerEntry import DrawerEntry

class DrawerContainer:
    def __init__(self, height: int, pos_x: int):
        from src.status_warehouse.Container.carousel import Carousel
        from src.status_warehouse.Container.column import Column

        # initialize main vars
        self.__container = []
        self.__height = height
        def_space = obt_value_json("default_height_space")
        self.__storage = obt_value_json("storage_height") // def_space
        self.__hole = obt_value_json("hole_height") // def_space
        self.__deposit = obt_value_json("deposit_height") // def_space
        self.__buffer = obt_value_json("buffer_height") // def_space
        self.__pos_x = pos_x

        # check if is output column or not
        if (type(self) is Column) and self.__pos_x == 0:
            print(type(self))
            self.__num_entries = self.__storage // def_space
        else:
            self.__num_entries = self.__height // def_space

        # check if is carousel to create container
        valid_index = 0
        if type(self) is Carousel:
            valid_index = self.__storage + self.__hole
            # insert None value to indicate that are invalid positions
            for i in range(valid_index):
                self.__container.append(None)

        # create container
        for i in range(valid_index, self.__num_entries):
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

    def get_storage(self) -> int:
        return self.__storage

    def get_hole(self) -> int:
        return self.__hole

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
                    if DrawerEntry.get_drawer(self.get_container()[i]) == drawer:
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
