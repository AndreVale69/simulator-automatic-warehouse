import copy
from abc import abstractmethod
from src.useful_func import open_config
from src.drawer import Drawer
from src.status_warehouse.Entry.emptyEntry import EmptyEntry
from src.status_warehouse.Entry.drawerEntry import DrawerEntry


class DrawerContainer:
    def __init__(self, pos_x: int):
        # initialize main vars
        config: dict = open_config()

        self.container = []
        self.height = config["height_warehouse"]
        self.def_space = config["default_height_space"]
        self.storage = config["columns"][pos_x]["height"] // self.get_def_space()
        self.hole = config["carousel"]["hole_height"] // self.get_def_space()
        self.deposit = config["carousel"]["deposit_height"] // self.get_def_space()
        self.buffer = config["carousel"]["buffer_height"] // self.get_def_space()
        self.num_entries = self.get_height() // self.get_def_space()
        self.pos_x = pos_x

    def __deepcopy__(self, memo):
        newone = type(self)(self.get_pos_x())
        newone.__dict__.update(self.__dict__)
        self.container = copy.deepcopy(self.container, memo)
        self.height = copy.deepcopy(self.height, memo)
        self.def_space = copy.deepcopy(self.def_space, memo)
        self.storage = copy.deepcopy(self.storage, memo)
        self.hole = copy.deepcopy(self.hole, memo)
        self.deposit = copy.deepcopy(self.deposit, memo)
        self.buffer = copy.deepcopy(self.buffer, memo)
        self.num_entries = copy.deepcopy(self.num_entries, memo)
        self.pos_x = copy.deepcopy(self.pos_x, memo)
        return newone

    def get_height(self) -> int:
        return self.height

    def get_def_space(self) -> int:
        return self.def_space

    def get_num_entries(self) -> int:
        return self.num_entries

    def get_container(self) -> list:
        return self.container

    def get_buffer(self) -> int:
        return self.buffer

    def get_deposit(self) -> int:
        return self.deposit

    def get_pos_x(self) -> int:
        return self.pos_x

    def get_storage(self) -> int:
        return self.storage

    def get_hole(self) -> int:
        return self.hole

    def set_num_entries(self, num_entries: int):
        self.num_entries = num_entries

    def add_item_to_container(self, element):
        self.get_container().append(element)

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
