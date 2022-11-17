from src.useful_func import obt_value_json
from src.drawer import Drawer
from src.status_warehouse.Container.drawerContainer import DrawerContainer
from src.status_warehouse.Entry.emptyEntry import EmptyEntry
from src.status_warehouse.Entry.drawerEntry import DrawerEntry


class Carousel(DrawerContainer):
    def __init__(self, height: int, pos_x: int):
        super().__init__(height, pos_x)

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
        buf = super().get_buffer()
        dep = super().get_deposit()
        valid_index = store + hole
        if to_show:
            # check if it's empty
            if isinstance(self.get_container()[valid_index], EmptyEntry):
                for i in range(buf):
                    # initialize positions
                    drawer_entry = DrawerEntry(super().get_pos_x(), valid_index + i)
                    # connect Drawer to entry
                    drawer_entry.add_drawer(drawer)
                    # add to container
                    self.get_container()[valid_index + i] = drawer_entry
                return True
            else:
                return False
        else:
            valid_index = valid_index + dep
            if isinstance(self.get_container()[valid_index], EmptyEntry):
                for i in range(valid_index, len(self.get_container())):
                    # initialize positions
                    drawer_entry = DrawerEntry(super().get_pos_x(), i)
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
