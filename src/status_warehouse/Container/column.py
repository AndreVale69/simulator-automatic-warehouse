import copy

from src.drawer import Drawer
from src.status_warehouse.Container.drawerContainer import DrawerContainer
from src.status_warehouse.Entry.drawerEntry import DrawerEntry
from src.status_warehouse.Entry.emptyEntry import EmptyEntry


class Column(DrawerContainer):
    def __init__(self, info: dict, warehouse):
        super().__init__(info["height"], info["x_offset"], info["width"], warehouse)

        self.width = info["width"]
        self.height_last_position = info["height_last_position"] // self.get_def_space()

        # create container
        for i in range(self.get_height_col()):
            self.create_new_space(EmptyEntry(info["x_offset"], i))

    def __deepcopy__(self, memo):
        info: dict = {
            "height": self.get_height_col(),
            "x_offset": self.get_offset_x(),
            "width": self.get_width(),
            "height_last_position": self.get_height_last_position()
        }
        copy_obj = Column(info, self.get_warehouse())
        copy_obj.container = copy.deepcopy(self.get_container(), memo)
        return copy_obj

    def get_height_last_position(self) -> int:
        return self.height_last_position

    # override
    def add_drawer(self, drawer: Drawer, index: int = None):
        how_many = drawer.get_max_num_space() + index

        drawer_entry = self.create_drawerEntry(drawer, index)
        # connect Entry to Drawer
        drawer.set_first_drawerEntry(drawer_entry)
        index += 1

        for index in range(index, how_many):
            self.create_drawerEntry(drawer, index)

    def create_drawerEntry(self, drawer: Drawer, index: int) -> DrawerEntry:
        # initialize positions
        drawer_entry = DrawerEntry(self.get_offset_x(), index)
        # connect Drawer to Entry
        drawer_entry.add_drawer(drawer)
        # add to container
        self.get_container()[index] = drawer_entry
        # return the drawer entry just added
        return drawer_entry

    # override
    def remove_drawer(self, drawer: Drawer) -> bool:
        """Remove a drawer"""
        return super().remove_drawer(drawer)
