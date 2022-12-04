import copy

from src.drawer import Drawer
from src.status_warehouse.Entry.entry import Entry


class DrawerEntry(Entry):
    def __init__(self, pos_x: int, pos_y: int):
        super().__init__(pos_x, pos_y)
        self.__drawer = None

    def __deepcopy__(self, memo):
        newone = super().__deepcopy__(memo)
        self.__drawer = copy.deepcopy(self.__drawer, memo)
        return newone

    def get_drawer(self):
        return self.__drawer

    def add_drawer(self, drawer: Drawer):
        # copy "pointer"
        self.__drawer = drawer
