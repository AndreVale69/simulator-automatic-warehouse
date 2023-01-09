import copy
from abc import abstractmethod

from src.drawer import Drawer
from src.status_warehouse.Entry.drawerEntry import DrawerEntry
from src.status_warehouse.Entry.emptyEntry import EmptyEntry


class DrawerContainer:
    def __init__(self, height_col: int, offset_x: int, width: int):
        from src.useful_func import open_config

        # initialize main vars
        config: dict = open_config()
        self.container = []
        self.height_warehouse = config["height_warehouse"]
        self.def_space = config["default_height_space"]
        self.hole = config["carousel"]["hole_height"] // self.get_def_space()
        self.deposit = config["carousel"]["deposit_height"] // self.get_def_space()
        self.buffer = config["carousel"]["buffer_height"] // self.get_def_space()
        self.width = width
        self.height_column = height_col // self.get_def_space()
        self.offset_x = offset_x

    def __deepcopy__(self, memo):
        # TODO: implementare nelle sottoclassi + metodo abs in drawerContainer
        info: dict = {
            "height": self.get_height_col(),
            "x_offset": self.get_offset_x(),
            "width": self.get_width(),
            "deposit_height": self.get_deposit() * self.get_def_space(),
            "buffer_height": self.get_buffer() * self.get_def_space()
        }
        copy_obj = type(self)(info)
        copy_obj.container = copy.deepcopy(self.container, memo)
        copy_obj.height_warehouse = self.get_height()
        copy_obj.def_space = self.get_def_space()
        copy_obj.height_column = self.get_height_col()
        copy_obj.hole = self.get_hole()
        copy_obj.deposit = self.get_deposit()
        copy_obj.buffer = self.get_buffer()
        copy_obj.offset_x = self.get_offset_x()
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

    def get_offset_x(self) -> int:
        return self.offset_x

    def get_height_col(self) -> int:
        return self.height_column

    def get_hole(self) -> int:
        return self.hole

    def get_width(self) -> int:
        return self.width

    def create_new_space(self, element):
        self.get_container().append(element)

    @abstractmethod
    def add_drawer(self, drawer: Drawer, index: int = None):
        pass

    def remove_drawer(self, drawer: Drawer):
        is_remove: bool = False
        first_entry: DrawerEntry = drawer.get_first_drawerEntry()
        entry_y: int = first_entry.get_pos_y()
        entry_x: int = first_entry.get_offset_x()

        for index, element in enumerate(self.get_container()):
            # if is a DrawerEntry element
            # if they've the same coordinates
            # if the drawers are the same (see __eq__ method)
            if isinstance(element, DrawerEntry) and \
                    element.get_pos_y() == entry_y and \
                    element.get_drawer() == drawer:
                self.get_container()[index] = EmptyEntry(entry_x, entry_y + index)
                is_remove = True
                entry_y += 1

        if not is_remove:
            print("Drawer doesn't removed.")
