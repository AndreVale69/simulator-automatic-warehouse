from src.drawer import Drawer
from src.status_warehouse.Container.drawerContainer import DrawerContainer
from src.status_warehouse.Entry.emptyEntry import EmptyEntry
from src.status_warehouse.Entry.drawerEntry import DrawerEntry


class Carousel(DrawerContainer):
    def __init__(self, height: int, pos_y: int):
        super().__init__(height, pos_y)

    # override
    def add_drawer(self, to_show: bool, drawer: Drawer) -> bool:
        """
        Add a drawer in buffer area or show as an output.

        :param to_show: True to show a drawer, otherwise False to put it into buffer area
        :param drawer: To show or to save
        :return: True there is space and the operation is successes, False there isn't space and the operation is failed
        """
        buf = super().get_buffer()
        hole = super().get_hole()
        if to_show:
            # check if it's empty
            if isinstance(self.get_container()[0], EmptyEntry):  # TODO BUG?
                for i in range(buf):
                    # initialize positions
                    drawer_entry = DrawerEntry(i, super().get_pos_y())
                    # connect Drawer to entry
                    drawer_entry.add_drawer(drawer)
                    # add to container
                    self.get_container()[i] = drawer_entry
                return True
            else:
                return False
        else:
            if isinstance(self.get_container()[buf], EmptyEntry):  # TODO BUG?
                for i in range(buf, hole + buf):
                    # initialize positions
                    drawer_entry = DrawerEntry(i, super().get_pos_y())
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
