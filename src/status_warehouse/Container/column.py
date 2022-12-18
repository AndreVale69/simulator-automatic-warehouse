from src.status_warehouse.Container.drawerContainer import DrawerContainer
from src.status_warehouse.Entry.drawerEntry import DrawerEntry
from src.drawer import Drawer
from src.status_warehouse.Entry.emptyEntry import EmptyEntry


class Column(DrawerContainer):
    def __init__(self, info: dict):
        super().__init__(info["x_offset"])

        # create container
        for i in range(self.get_height_col()):
            self.add_item_to_container(EmptyEntry(info["x_offset"], i))

    def __deepcopy__(self, memo):
        return super().__deepcopy__(memo)

    # override
    def add_drawer(self, index: int, drawer: Drawer):
        how_many = drawer.get_max_num_space() + index

        drawer_entry = self.__create_drawerEntry(drawer, index)
        # connect Entry to Drawer
        drawer.set_first_drawerEntry(drawer_entry)
        index += 1

        for index in range(index, how_many):
            self.__create_drawerEntry(drawer, index)

    def __create_drawerEntry(self, drawer: Drawer, index: int) -> DrawerEntry:
        # initialize positions
        drawer_entry = DrawerEntry(self.get_pos_x(), index)
        # connect Drawer to Entry
        drawer_entry.add_drawer(drawer)
        # add to container
        self.get_container()[index] = drawer_entry
        # return the drawer entry just added
        return drawer_entry

    # override
    def remove_drawer(self, drawer: Drawer):
        super().remove_drawer(drawer)
