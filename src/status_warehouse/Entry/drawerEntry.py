import copy

from src.drawer import Drawer
from src.status_warehouse.Entry.entry import Entry


class DrawerEntry(Entry):
    def __init__(self, offset_x: int, pos_y: int):
        super().__init__(offset_x, pos_y)
        self.drawer = None

    def __deepcopy__(self, memo):
        copy_obj = DrawerEntry(self.get_offset_x(), self.get_pos_y())
        copy_obj.drawer = copy.deepcopy(self.get_drawer(), memo)
        return copy_obj

    def get_drawer(self) -> Drawer:
        return self.drawer

    def add_drawer(self, drawer: Drawer):
        # copy "pointer"
        self.drawer = drawer
