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
        def_space = obt_value_json("default_height_space")
        store = obt_value_json("storage_height") // def_space
        hole = obt_value_json("hole_height") // def_space
        buf = super().get_buffer()
        dep = super().get_deposit()
        if to_show:
            # check if it's empty
            if isinstance(self.get_container()[0], EmptyEntry):
                for i in range(buf):
                    # initialize positions
                    y = store + hole
                    drawer_entry = DrawerEntry(super().get_pos_x(), y + i)
                    # connect Drawer to entry
                    drawer_entry.add_drawer(drawer)
                    # add to container
                    self.get_container()[i] = drawer_entry
                return True
            else:
                return False
        else:
            if isinstance(self.get_container()[buf], EmptyEntry):
                for i in range(buf, dep + buf):
                    # initialize positions
                    y = store + hole + dep
                    drawer_entry = DrawerEntry(super().get_pos_x(), y + (i - buf))
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
