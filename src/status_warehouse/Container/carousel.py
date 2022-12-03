from src.drawer import Drawer
from src.status_warehouse.Container.drawerContainer import DrawerContainer
from src.status_warehouse.Entry.emptyEntry import EmptyEntry
from src.status_warehouse.Entry.drawerEntry import DrawerEntry


class Carousel(DrawerContainer):
    def __init__(self, pos_x: int):
        super().__init__(pos_x)

        # get first y to start
        first_y = super().get_storage() + super().get_hole()

        # set length of entries
        super().set_num_entries(super().get_deposit() + super().get_buffer())

        # create container
        for i in range(super().get_num_entries()):
            super().add_item_to_container(EmptyEntry(pos_x, i + first_y))

    # override
    def add_drawer(self, to_show: bool, drawer: Drawer) -> bool:
        """
        Add a drawer in buffer area or show as an output.

        :param to_show: True to show a drawer, otherwise False to put it into buffer area
        :param drawer: To show or to save
        :return: True there is space and the operation is successes, False there isn't space and the operation is failed
        """
        store = super().get_storage()
        hole = super().get_hole()
        dep = super().get_deposit()
        first_y = store + hole
        if to_show:
            # check if it's empty
            if isinstance(self.get_container()[0], EmptyEntry):
                for i in range(dep):
                    # initialize positions
                    drawer_entry = DrawerEntry(super().get_pos_x(), first_y + i)
                    # connect Drawer to entry
                    drawer_entry.add_drawer(drawer)
                    # add to container
                    self.get_container()[i] = drawer_entry
                return True
            else:
                return False
        else:
            if isinstance(self.get_container()[dep], EmptyEntry):
                for i in range(dep, len(self.get_container())):
                    # initialize positions
                    drawer_entry = DrawerEntry(super().get_pos_x(), first_y + i)
                    # connect Drawer to entry
                    drawer_entry.add_drawer(drawer)
                    # add to container
                    self.get_container()[i] = drawer_entry
                return True
            else:
                return False

    # override
    def remove_drawer(self, drawer: Drawer):
        super().remove_drawer(drawer)
