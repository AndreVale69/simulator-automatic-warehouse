import copy

from src.sim.drawer import Drawer
from src.sim.status_warehouse.container.drawer_container import DrawerContainer
from src.sim.status_warehouse.entry.drawer_entry import DrawerEntry
from src.sim.status_warehouse.entry.empty_entry import EmptyEntry


class Column(DrawerContainer):
    def __init__(self, info: dict, warehouse):
        """
        The column is a simple column of the warehouse.
        It can't be where there is the bay and the buffer.
        It is thought to store the drawers.

        :type info: dict
        :type warehouse: Warehouse
        :param info: info about the column (config).
        :param warehouse: the warehouse where the column is located.
        """
        super().__init__(info["height"], info["x_offset"], info["width"], warehouse)

        self.width = info["width"]
        self.height_last_position = info["height_last_position"] // self.get_def_space()

        # create container
        for i in range(self.get_height_col()):
            self.create_new_space(EmptyEntry(info["x_offset"], i))

    def __deepcopy__(self, memo):
        info: dict = {
            "height": self.get_height_col() * self.get_def_space(),
            "x_offset": self.get_offset_x(),
            "width": self.get_width(),
            "height_last_position": self.get_height_last_position() * self.get_def_space()
        }
        copy_obj = Column(info, self.get_warehouse())
        copy_obj.container = copy.deepcopy(self.get_container(), memo)
        return copy_obj

    def __eq__(self, other):
        return (
            isinstance(other, Column) and
            self.get_height_last_position() == other.get_height_last_position() and
            DrawerContainer.__eq__(self, other)
        )

    def get_height_last_position(self) -> int:
        """
        Get the height of the last position.

        :rtype: int
        :return: the height of the last position.
        """
        return self.height_last_position

    # override
    def add_drawer(self, drawer: Drawer, index: int = None):
        """
        Add a drawer to the column.

        :type drawer: Drawer
        :type index: int
        :param drawer: drawer to be added.
        :param index: index of the column where to add the drawer.
        """
        how_many = drawer.get_max_num_space() + index

        drawer_entry = self.create_drawerEntry(drawer, index)
        # connect Entry to Drawer
        drawer.set_first_drawerEntry(drawer_entry)
        index += 1

        for index in range(index, how_many):
            self.create_drawerEntry(drawer, index)

    def create_drawerEntry(self, drawer: Drawer, index: int) -> DrawerEntry:
        """
        Create a drawer entry and add it to the column.

        :type drawer: Drawer
        :type index: int
        :rtype: DrawerEntry
        :param drawer: the drawer to be added.
        :param index: where to add the drawer.
        :return: the DrawerEntry created.
        """
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
        """
        Remove a drawer from the column.

        :type drawer: Drawer
        :rtype: bool
        :param drawer: the drawer to be removed.
        :return: True if the drawer was removed, False otherwise.
        """
        return super().remove_drawer(drawer)
