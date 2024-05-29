from copy import deepcopy

from src.sim.drawer import Drawer
from src.sim.status_warehouse.container.drawer_container import DrawerContainer
from src.sim.status_warehouse.entry.drawer_entry import DrawerEntry
from src.sim.status_warehouse.entry.empty_entry import EmptyEntry
from src.sim.warehouse_configuration_singleton import WarehouseConfigurationSingleton


class CarouselInfo:
    """ Support class used as a parameter to help instantiate the Carousel class. """
    def __init__(self, deposit_height: int, buffer_height: int, x_offset: int, width: int):
        if False in {isinstance(deposit_height, int), isinstance(buffer_height, int),
                     isinstance(x_offset, int), isinstance(width, int)}:
            raise TypeError("The parameters must be integers")
        self.deposit_height: int = deposit_height
        self.buffer_height: int = buffer_height
        self.x_offset: int = x_offset
        self.width: int = width


class Carousel(DrawerContainer):
    def __init__(self, info: CarouselInfo, warehouse):
        """
        The carousel represents the set of deposit (bay) and the buffer (drawer under the bay).

        :type info: CarouselInfo
        :type warehouse: Warehouse
        :param info: class containing information about the carousel (config).
        :param warehouse: the warehouse where the carousel is located.
        """
        height_carousel = info.deposit_height + info.buffer_height
        super().__init__(height_carousel, info.x_offset, info.width, warehouse)
        config: dict = WarehouseConfigurationSingleton.get_instance().get_configuration()
        self.hole = config["carousel"]["hole_height"] // self.get_def_space()
        self.deposit = config["carousel"]["deposit_height"] // self.get_def_space()
        self.buffer = config["carousel"]["buffer_height"] // self.get_def_space()

        # get first y to start
        first_y = self.get_height_container() + self.get_hole()

        # create container with only two positions
        # create deposit
        self.create_new_space(EmptyEntry(self.get_offset_x(), first_y))
        # create buffer
        self.create_new_space(EmptyEntry(self.get_offset_x(), first_y + (self.get_deposit() + self.get_buffer())))

    def __deepcopy__(self, memo):
        info = CarouselInfo(
            deposit_height = self.get_deposit() * self.get_def_space(),
            buffer_height = self.get_buffer() * self.get_def_space(),
            x_offset = self.get_offset_x(),
            width = self.get_width()
        )
        copy_obj = Carousel(info, self.get_warehouse())
        copy_obj.container = deepcopy(self.get_container(), memo)
        return copy_obj

    def __eq__(self, other):
        return (
            isinstance(other, Carousel) and
            self.get_buffer() == other.get_buffer() and
            self.get_deposit() == other.get_deposit() and
            self.get_hole() == other.get_hole() and
            self.get_deposit_entry() == other.get_deposit_entry() and
            self.get_buffer_entry() == other.get_buffer_entry() and
            self.get_num_drawers() == other.get_num_drawers() and
            DrawerContainer.__eq__(self, other)
        )

    def __hash__(self):
        return (
            14951 ^
            DrawerContainer.__hash__(self) ^
            hash(self.buffer) ^
            hash(self.deposit) ^
            hash(self.hole) ^
            hash(self.get_deposit_entry()) ^
            hash(self.get_buffer_entry()) ^
            hash(self.get_num_drawers())
        )

    def get_buffer(self) -> int:
        """
        Get the height of the buffer of the carousel.

        :rtype: int
        :return: the height of the buffer of the carousel.
        """
        return self.buffer

    def get_deposit(self) -> int:
        """
        Get the height of the deposit of the carousel.

        :rtype: int
        :return: the height of the deposit of the carousel.
        """
        return self.deposit

    def get_hole(self) -> int:
        """
        Get the height of the hole.
        The hole is the height from the bay to the start of the column,
        it is the space where a person can place a material inside the warehouse.

        :rtype: int
        :return: the height of the hole.
        """
        return self.hole

    def get_deposit_entry(self) -> DrawerEntry | EmptyEntry:
        """
        Get the deposit (bay) entry or an empty entry.

        :rtype: DrawerEntry | EmptyEntry
        :return: the deposit (bay) entry or an empty entry.
        """
        return self.container[0]

    def get_deposit_drawer(self) -> Drawer:
        """
        Get the deposit (bay) drawer.

        :rtype: Drawer
        :return: the Drawer object of the deposit (bay).
        :raises AttributeError: when the deposit (bay) is empty and there is no drawer.
        """
        return self.container[0].get_drawer()

    def get_buffer_entry(self) -> DrawerEntry | EmptyEntry:
        """
        Get the buffer entry or an empty entry.

        :rtype: DrawerEntry | EmptyEntry
        :return: the buffer entry or an empty entry.
        """
        return self.container[1]

    def get_buffer_drawer(self) -> Drawer:
        """
        Get the buffer entry or an empty entry.

        :rtype: Drawer
        :return: the buffer entry or an empty entry.
        :raises AttributeError: when the buffer is empty and there is no drawer.
        """
        return self.container[1].get_drawer()

    def get_num_drawers(self) -> int:
        """
        Get how many drawers there are.

        :rtype: int
        :return: the number of drawers there are.
        """
        return isinstance(self.get_deposit_entry(), DrawerEntry) + isinstance(self.get_buffer_entry(), DrawerEntry)

    def get_num_entries_free(self) -> int:
        count = 0
        for entry in self.get_container():
            if isinstance(entry, EmptyEntry):
                count += 1
        return count

    def is_full(self) -> bool:
        return self.is_buffer_full() and self.is_deposit_full()

    def is_empty(self) -> bool:
        return not self.is_buffer_full() and not self.is_deposit_full()

    def is_buffer_full(self) -> bool:
        """
        Check if the buffer is full.

        :rtype: bool
        :return: True if is full, False otherwise.
        """
        # check if the first position of buffer have a Drawer
        return isinstance(self.get_buffer_entry(), DrawerEntry)

    def is_deposit_full(self) -> bool:
        """
        Check if the deposit (bay) is full.

        :rtype: bool
        :return: True if is full, False otherwise.
        """
        # check if the first position of deposit have a Drawer
        return isinstance(self.get_deposit_entry(), DrawerEntry)

    def add_drawer(self, drawer: Drawer):
        """
        Add a drawer in the buffer area or show as an output (deposit).

        :type drawer: Drawer
        :param drawer: to show or to save.
        :raises RuntimeError: if the drawer already exists.
        """
        first_y = self.get_height_container() + self.hole + self.deposit
        is_deposit_full = self.is_deposit_full()

        # if the carousel is full, exception
        if self.is_buffer_full() and is_deposit_full:
            raise RuntimeError("Collision!")

        # add the drawerEntry in the buffer iff the deposit is full
        self._create_drawerEntry(drawer, first_y, is_buffer=is_deposit_full)

    def _create_drawerEntry(self, drawer: Drawer, first_y: int, is_buffer: bool):
        """
        Create a drawer entry.

        :type drawer: Drawer
        :type first_y: int
        :type is_buffer: bool
        :param drawer: the drawer to insert.
        :param first_y: the y position of the drawer to insert.
        :param is_buffer: True if to insert in the buffer position, False if to insert in the bay position.
        """
        # initialize positions
        if is_buffer:
            first_y += self.get_buffer()
        drawer_entry = DrawerEntry(self.get_offset_x(), first_y)
        # connect Drawer to entry
        drawer_entry.add_drawer(drawer)
        # add to container
        self.get_container()[int(is_buffer)] = drawer_entry
        # connect Entry just added to relative Drawer
        drawer.set_first_drawerEntry(drawer_entry)

    # override
    def remove_drawer(self, drawer: Drawer) -> bool:
        """
        Remove a drawer.

        :type drawer: Drawer
        :rtype: bool
        :param drawer: the drawer to remove.
        :return: True if the drawer was removed, False otherwise.
        """
        first_entry: DrawerEntry = drawer.get_first_drawerEntry()
        entry_y_to_rmv = first_entry.get_pos_y()
        entry_x_to_rmv = first_entry.get_offset_x()
        deposit_entry: DrawerEntry | EmptyEntry = self.container[0]
        buffer_entry: DrawerEntry | EmptyEntry = self.container[1]

        if isinstance(deposit_entry, DrawerEntry) and deposit_entry.get_drawer() == drawer:
            self.container[0] = EmptyEntry(entry_x_to_rmv, entry_y_to_rmv)
            return True
        elif isinstance(buffer_entry, DrawerEntry) and buffer_entry.get_drawer() == drawer:
            self.container[1] = EmptyEntry(entry_x_to_rmv, entry_y_to_rmv)
            return True
        return False
