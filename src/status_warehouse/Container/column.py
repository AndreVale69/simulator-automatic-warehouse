from src.status_warehouse.Container.drawerContainer import DrawerContainer
from src.status_warehouse.Entry.drawerEntry import DrawerEntry
from src.drawer import Drawer
from src.status_warehouse.Entry.emptyEntry import EmptyEntry


class Column(DrawerContainer):
    def __init__(self, pos_x: int):
        super().__init__(pos_x)
        # different height if the column match at the output
        if pos_x == 0:
            self.set_num_entries(self.get_storage())

        # create container
        for i in range(self.get_num_entries()):
            self.add_item_to_container(EmptyEntry(pos_x, i))

    def __deepcopy__(self, memo):
        return super().__deepcopy__(memo)

    # override
    def add_drawer(self, index: int, drawer: Drawer):
        how_many = drawer.get_max_num_space()

        # initialize positions
        drawer_entry = DrawerEntry(self.get_pos_x(), index)
        # connect Drawer to entry
        drawer_entry.add_drawer(drawer)

        while how_many > 0:
            # add to container
            self.get_container()[index] = drawer_entry
            index += 1
            how_many -= 1

    # override
    def remove_drawer(self, drawer: Drawer):
        super().remove_drawer(drawer)
