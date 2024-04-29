from abc import abstractmethod

from src.sim.drawer import Drawer
from src.sim.status_warehouse.entry.drawer_entry import DrawerEntry
from src.sim.status_warehouse.entry.empty_entry import EmptyEntry
from src.sim.warehouse_configuration_singleton import WarehouseConfigurationSingleton


class DrawerContainer:
    def __init__(self, height_col: int, offset_x: int, width: int, warehouse):
        """
        A superclass representing the drawer container of a column or carousel.

        :type height_col: int
        :type offset_x: int
        :type width: int
        :type warehouse: Warehouse
        :param height_col: height of the container.
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
        self.height_column = height_col // self.get_def_space()
        self.offset_x = offset_x

    @abstractmethod
    def __deepcopy__(self, memo):
        pass

    def __eq__(self, other):
        return (
            isinstance(other, DrawerContainer) and
            self.get_height_warehouse() == other.get_height_warehouse() and
            self.get_def_space() == other.get_def_space() and
            self.get_container() == other.get_container() and
            self.get_offset_x() == other.get_offset_x() and
            self.get_height_col() == other.get_height_col() and
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
            13 ^
            hash(self.get_height_warehouse()) ^
            hash(self.get_def_space()) ^
            hash(tuple(self.get_container())) ^
            hash(self.get_offset_x()) ^
            hash(self.get_height_col()) ^
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
        pass

    @abstractmethod
    def is_full(self) -> bool:
        """
        Check if the container is full.

        :rtype: bool
        :return: True if the container is full, False otherwise.
        """
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        """
        Check if the container is empty.

        :rtype: bool
        :return: True if the container is empty, False otherwise.
        """
        pass

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

    def get_height_col(self) -> int:
        """
        Get the height of the container.

        :rtype: int
        :return: the height of the container.
        """
        return self.height_column

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
        count = 0
        index = 0
        col: list[DrawerEntry | EmptyEntry] = self.get_container()
        while index < len(col):
            if type(col[index]) is DrawerEntry:
                # how many entries occupies the drawer
                index += col[index].get_drawer().get_max_num_space()
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
            if type(entry) is DrawerEntry:
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
        while index < len(col):
            entry = col[index]
            if type(entry) is DrawerEntry:
                # how many entries occupies the drawer
                index += entry.get_drawer().get_max_num_space()
                drawers.append(entry.get_drawer())
            else:
                index += 1
        return drawers

    def get_entries_occupied(self) -> list[DrawerEntry]:
        """
        Get every DrawerEntry in the container.

        :rtype: list[DrawerEntry]
        :return: a list of DrawerEntry in the container.
        """
        entries_occupied = []
        for entry in self.get_container():
            if type(entry) is DrawerEntry:
                entries_occupied.append(entry)
        return entries_occupied

    def get_num_materials(self) -> int:
        """
        Get how many materials there are.

        :rtype: int
        :return: how many materials there are.
        """
        count = 0
        drawers = self.get_drawers()
        # TODO: improve
        for drawer in drawers:
            count += len(drawer.items)
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
        self.get_container().append(element)

    def remove_drawer(self, drawer: Drawer) -> bool:
        """ Remove a drawer """
        entries_to_rmv: int = drawer.get_max_num_space()
        entries_removed: int = 0

        for index, entry in enumerate(self.get_container()):
            # if is a DrawerEntry element
            # if the drawers are the same (see __eq__ method)
            if isinstance(entry, DrawerEntry) and entry.get_drawer() == drawer:
                self.get_container()[index] = EmptyEntry(entry.get_offset_x(), entry.get_pos_y())
                entries_removed += 1
                if entries_removed == entries_to_rmv:
                    return True

    def reset_container(self):
        """ Clean up the container using EmptyEntry instances. """
        for index, entry in enumerate(self.container):
            # if it's a drawer, remove it (overwriting)
            if isinstance(entry, DrawerEntry):
                self.container[index] = EmptyEntry(offset_x=self.offset_x, pos_y=entry.get_pos_y())

    @abstractmethod
    def add_drawer(self, drawer: Drawer, index: int = None):
        pass
