from abc import abstractmethod

from src.sim.drawer import Drawer
from src.sim.status_warehouse.entry.drawer_entry import DrawerEntry
from src.sim.status_warehouse.entry.empty_entry import EmptyEntry
from src.sim.warehouse_configuration_singleton import WarehouseConfigurationSingleton


class DrawerContainer:
    def __init__(self, height: int, offset_x: int, width: int, warehouse):
        """
        A superclass representing the drawer container of a column or carousel.

        :type height: int
        :type offset_x: int
        :type width: int
        :type warehouse: Warehouse
        :param height: height of the container.
        :param offset_x: x offset of the container.
        :param width: width of the container.
        :param warehouse: warehouse where the container is stored.
        """
        # initialize main vars
        config: dict = WarehouseConfigurationSingleton.get_instance().get_configuration()
        self.warehouse = warehouse
        self.container = []
        self.height_warehouse = config["height_warehouse"]
        self.def_space = config["default_height_space"]
        self.width = width
        self.height_container = height // self.get_def_space()
        self.offset_x = offset_x

    def __eq__(self, other):
        return (
                isinstance(other, DrawerContainer) and
                self.get_height_warehouse() == other.get_height_warehouse() and
                self.get_def_space() == other.get_def_space() and
                self.get_container() == other.get_container() and
                self.get_offset_x() == other.get_offset_x() and
                self.get_height_container() == other.get_height_container() and
                self.get_width() == other.get_width() and
                self.get_num_drawers() == other.get_num_drawers() and
                self.get_num_entries_occupied() == other.get_num_entries_occupied() and
                self.get_num_entries_free() == other.get_num_entries_free() and
                self.get_drawers() == other.get_drawers() and
                self.get_entries_occupied() == other.get_entries_occupied() and
                self.get_num_materials() == other.get_num_materials()
        )

    def __hash__(self):
        return (
                1093 ^
                hash(self.get_height_warehouse()) ^
                hash(self.get_def_space()) ^
                hash(tuple(self.get_container())) ^
                hash(self.get_offset_x()) ^
                hash(self.get_height_container()) ^
                hash(self.get_width()) ^
                hash(self.get_num_drawers()) ^
                hash(self.get_num_entries_occupied()) ^
                hash(self.get_num_entries_free()) ^
                hash(tuple(self.get_drawers())) ^
                hash(tuple(self.get_entries_occupied())) ^
                hash(self.get_num_materials())
        )

    @abstractmethod
    def get_num_entries_free(self) -> int:
        """
        Get how many seats are available.

        :rtype: int
        :return: how many seats are available.
        """
        raise NotImplementedError

    @abstractmethod
    def is_full(self) -> bool:
        """
        Check if the container is full.

        :rtype: bool
        :return: True if the container is full, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def is_empty(self) -> bool:
        """
        Check if the container is empty.

        :rtype: bool
        :return: True if the container is empty, False otherwise.
        """
        raise NotImplementedError

    def get_warehouse(self):
        """
        Get the warehouse where the container is stored.

        :rtype: Warehouse
        :return: the warehouse where the container is stored.
        """
        return self.warehouse

    def get_height_warehouse(self) -> int:
        """
        Get the height of the warehouse.

        :rtype: int
        :return: the height of the warehouse.
        """
        return self.height_warehouse

    def get_def_space(self) -> int:
        """
        Get the default height space of the container.

        :rtype: int
        :return: the default height space of the container.
        """
        return self.def_space

    def get_container(self) -> list[DrawerEntry | EmptyEntry]:
        """
        Get the full list of entries for the container in the warehouse.

        :rtype: list[DrawerEntry | EmptyEntry]
        :return: the full list of entries for the container in the warehouse.
        """
        return self.container

    def get_offset_x(self) -> int:
        """
        Get the x offset of the container.

        :rtype: int
        :return: the x offset of the container.
        """
        return self.offset_x

    def get_height_container(self) -> int:
        """
        Get the height of the container.

        :rtype: int
        :return: the height of the container.
        """
        return self.height_container

    def get_width(self) -> int:
        """
        Get the width of the container.

        :rtype: int
        :return: the width of the container.
        """
        return self.width

    def get_num_drawers(self) -> int:
        """
        Get how many drawers there are in the container.

        :rtype: int
        :return: how many drawers there are in the container.
        """
        count = index = 0
        col: list[DrawerEntry | EmptyEntry] = self.get_container()
        len_col = len(col)
        while index < len_col:
            entry = col[index]
            if isinstance(entry, DrawerEntry):
                # how many entries occupies the drawer
                index += entry.get_drawer().get_num_space_occupied()
                count += 1
            else:
                index += 1
        return count

    def get_num_entries_occupied(self) -> int:
        """
        Get how many entries occupied there are.

        :rtype: int
        :return: how many entries occupied there are.
        """
        num_entry_occupied = 0
        for entry in self.get_container():
            if isinstance(entry, DrawerEntry):
                num_entry_occupied += 1
        return num_entry_occupied

    def get_drawers(self) -> list[Drawer]:
        """
        Get every Drawer in the container.

        :rtype: list[Drawer]
        :return: a list of Drawers in the container.
        """
        drawers = []
        index = 0
        col: list[DrawerEntry | EmptyEntry] = self.get_container()
        len_col = len(col)
        while index < len_col:
            entry = col[index]
            if isinstance(entry, DrawerEntry):
                # how many entries occupies the drawer
                drawer = entry.get_drawer()
                index += drawer.get_num_space_occupied()
                drawers.append(drawer)
            else:
                index += 1
        return drawers

    def get_entries_occupied(self) -> list[DrawerEntry]:
        """
        Get every DrawerEntry in the container.

        :rtype: list[DrawerEntry]
        :return: a list of DrawerEntry in the container.
        """
        return [entry for entry in self.container if isinstance(entry, DrawerEntry)]

    def get_num_materials(self) -> int:
        """
        Get how many materials there are.

        :rtype: int
        :return: how many materials there are.
        """
        count = 0
        for drawer in self.get_drawers():
            count += drawer.get_num_materials()
        return count

    def set_warehouse(self, new_warehouse):
        """
        Set a new warehouse where the container is stored.

        :type new_warehouse: Warehouse
        :param new_warehouse: a new warehouse where the container is stored.
        """
        self.warehouse = new_warehouse

    def create_new_space(self, element: EmptyEntry | DrawerEntry):
        """
        Create a new space inside the container.

        :type element: EmptyEntry | DrawerEntry
        :param element: entry of the new space to be created.
        """
        self.container.append(element)

    def reset_container(self):
        """ Clean up the container using EmptyEntry instances. """
        offset_x, ptr_container = self.offset_x, self.container
        for index, entry in enumerate(ptr_container):
            # if it's a drawer, remove it (overwriting)
            if isinstance(entry, DrawerEntry):
                ptr_container[index] = EmptyEntry(offset_x, entry.get_pos_y())
