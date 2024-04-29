import copy

from src.sim.drawer import Drawer
from src.sim.status_warehouse.entry.entry import Entry


class DrawerEntry(Entry):
    def __init__(self, offset_x: int, pos_y: int):
        """
        It is an entry of the warehouse where the drawer is located.

        :type offset_x: int
        :type pos_y: int
        :param offset_x: offset x of the drawer entry.
        :param pos_y: y of the drawer entry.
        """
        super().__init__(offset_x, pos_y)
        self.drawer = None

    def __deepcopy__(self, memo):
        copy_obj = DrawerEntry(self.get_offset_x(), self.get_pos_y())
        copy_obj.drawer = copy.deepcopy(self.get_drawer(), memo)
        if copy_obj == self.get_drawer().get_first_drawerEntry():
            copy_obj.drawer.set_first_drawerEntry(copy_obj)
        return copy_obj

    def __eq__(self, other):
        return (
            isinstance(other, DrawerEntry) and
            Entry.__eq__(self, other)
        )

    def __hash__(self):
        return 13 ^ Entry.__hash__(self)

    def get_drawer(self) -> Drawer:
        """
        Get the pointer to the drawer to which the DrawerEntry belongs.

        :rtype: Drawer
        :return: the Drawer pointer.
        """
        return self.drawer

    def add_drawer(self, drawer: Drawer):
        """
        Add the drawer pointer to the local reference.

        :type drawer: Drawer
        :param drawer: drawer pointer.
        """
        # copy "pointer"
        self.drawer = drawer
