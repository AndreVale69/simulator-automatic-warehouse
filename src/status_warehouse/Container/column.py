from src.status_warehouse.Container.drawerContainer import DrawerContainer
from src.status_warehouse.Entry.drawerEntry import DrawerEntry
from src.drawer import Drawer


class Column(DrawerContainer):
    def __init__(self, height: int, pos_x: int):
        super().__init__(height, pos_x)

    # override
    def add_drawer(self, index: int, drawer: Drawer):
        how_many = drawer.get_max_num_space()

        while how_many > 0:
            # initialize positions
            drawer_entry = DrawerEntry(super().get_pos_x(), index)
            # connect Drawer to entry
            drawer_entry.add_drawer(drawer)
            # add to container
            self.get_container()[index] = drawer_entry
            index += 1
            how_many -= 1

    # override
    def remove_drawer(self, drawer: Drawer):
        super().remove_drawer(drawer)
