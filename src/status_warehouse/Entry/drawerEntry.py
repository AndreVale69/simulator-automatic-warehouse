import copy

from src.status_warehouse.Entry.entry import Entry
from src.drawer import Drawer


class DrawerEntry(Entry):
    def __init__(self, offset_x: int, pos_y: int):
        super().__init__(offset_x, pos_y)
        self.drawer = None

    def __deepcopy__(self, memo):
        copy_obj = super().__deepcopy__(memo)
        copy_obj.drawer = copy.deepcopy(self.drawer, memo)
        return copy_obj

    def get_drawer(self) -> Drawer:
        return self.drawer

    def add_drawer(self, drawer: Drawer):
        # copy "pointer"
        self.drawer = drawer
