import copy
from abc import abstractmethod
from src.drawer import Drawer
from src.status_warehouse.Entry.emptyEntry import EmptyEntry
from src.status_warehouse.Entry.drawerEntry import DrawerEntry


class DrawerContainer:
    def __init__(self, pos_x: int):
        from src.useful_func import open_config

        # initialize main vars
        config: dict = open_config()
        self.container = []
        self.height_warehouse = config["height_warehouse"]
        self.def_space = config["default_height_space"]
        self.height_column = config["columns"][pos_x]["height"] // self.get_def_space()
        self.hole = config["carousel"]["hole_height"] // self.get_def_space()
        self.deposit = config["carousel"]["deposit_height"] // self.get_def_space()
        self.buffer = config["carousel"]["buffer_height"] // self.get_def_space()
        self.pos_x = pos_x

    def __deepcopy__(self, memo):
        tmp_dict = {"x_offset": self.get_pos_x()}
        copy_obj = type(self)(tmp_dict)
        copy_obj.container = copy.deepcopy(self.container, memo)
        copy_obj.height_warehouse = self.height_warehouse
        copy_obj.def_space = self.def_space
        copy_obj.height_column = self.height_column
        copy_obj.hole = self.hole
        copy_obj.deposit = self.deposit
        copy_obj.buffer = self.buffer
        copy_obj.pos_x = self.pos_x
        return copy_obj

    def get_height(self) -> int:
        return self.height_warehouse

    def get_def_space(self) -> int:
        return self.def_space

    def get_container(self) -> list:
        return self.container

    def get_buffer(self) -> int:
        return self.buffer

    def get_deposit(self) -> int:
        return self.deposit

    def get_pos_x(self) -> int:
        return self.pos_x

    def get_height_col(self) -> int:
        return self.height_column

    def get_hole(self) -> int:
        return self.hole

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
                    # fix DrawerEntry.get_drawer(self.get_cols_container()[i])
                    # with self.get_cols_container()[i].get_drawer()
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
