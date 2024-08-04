from __future__ import annotations

from copy import deepcopy
from logging import getLogger

from automatic_warehouse.status_warehouse.container.tray_container import TrayContainer
from automatic_warehouse.status_warehouse.entry.empty_entry import EmptyEntry
from automatic_warehouse.status_warehouse.entry.tray_entry import TrayEntry
from automatic_warehouse.status_warehouse.tray import Tray
from automatic_warehouse.warehouse_configuration_singleton import CarouselConfiguration

logger = getLogger(__name__)


class Carousel(TrayContainer):
    """
    The carousel represents the set of bay and the buffer (tray under the bay).

    :type info: CarouselConfiguration
    :type warehouse: Warehouse
    :param info: class containing information about the carousel (config).
    :param warehouse: the warehouse where the carousel is located.
    """

    def __init__(self, info: CarouselConfiguration, warehouse):
        super().__init__(info.bay_height + info.buffer_height, info.x_offset, info.width, info.length, warehouse)
        self.hole = info.hole_height // (def_space := self.def_space)
        self.bay = info.bay_height // def_space
        self.buffer = info.buffer_height // def_space

        # get first y to start
        first_y = self.num_entries + self.hole

        # create container with only two positions
        # create bay
        self.create_new_space(EmptyEntry(self.offset_x, first_y))
        # create buffer
        self.create_new_space(EmptyEntry(self.offset_x, first_y + (self.bay + self.buffer)))

    def __deepcopy__(self, memo):
        copy_obj = Carousel(CarouselConfiguration(
            length = self.length,
            bay_height = self.bay * (def_space := self.def_space),
            buffer_height = self.buffer * def_space,
            x_offset = self.offset_x,
            width = self.width,
            hole_height= self.hole * def_space
        ), self.warehouse)
        copy_obj.container = deepcopy(self.container, memo)
        return copy_obj

    def __eq__(self, other):
        return (
            isinstance(other, Carousel) and
            TrayContainer.__eq__(self, other) and
            self.buffer == other.buffer and
            self.bay == other.bay and
            self.hole == other.hole and
            self.get_bay_entry() == other.get_bay_entry() and
            self.get_buffer_entry() == other.get_buffer_entry() and
            self.get_num_trays() == other.get_num_trays()
        )

    def __hash__(self):
        return (
            14951 ^
            TrayContainer.__hash__(self) ^
            hash(self.buffer) ^
            hash(self.bay) ^
            hash(self.hole) ^
            hash(self.get_bay_entry()) ^
            hash(self.get_buffer_entry()) ^
            hash(self.get_num_trays())
        )

    def get_buffer(self) -> int:
        """
        Get the height of the buffer of the carousel.

        :rtype: int
        :return: the height of the buffer of the carousel.
        """
        return self.buffer

    def get_bay(self) -> int:
        """
        Get the height of the bay of the carousel.

        :rtype: int
        :return: the height of the bay of the carousel.
        """
        return self.bay

    def get_hole(self) -> int:
        """
        Get the height of the hole.

        The hole is the height from the bay to the start of the column,
        it is the space where a person can place a material inside the warehouse.

        :rtype: int
        :return: the height of the hole.
        """
        return self.hole

    def get_bay_entry(self) -> TrayEntry | EmptyEntry:
        """
        Get the bay entry or an empty entry.

        :rtype: TrayEntry | EmptyEntry
        :return: the bay entry or an empty entry.
        """
        return self.container[0]

    def get_bay_tray(self) -> Tray:
        """
        Get the bay tray.

        :rtype: Tray
        :return: the :class:`Tray <automatic_warehouse.status_warehouse.tray.Tray>` of the bay.
        :raises AttributeError: when the bay is empty and there is no tray.
        """
        return self.container[0].get_tray()

    def get_buffer_entry(self) -> TrayEntry | EmptyEntry:
        """
        Get the buffer entry or an empty entry.

        :rtype: TrayEntry | EmptyEntry
        :return: the buffer entry or an empty entry.
        """
        return self.container[1]

    def get_buffer_tray(self) -> Tray:
        """
        Get the buffer entry or an empty entry.

        :rtype: Tray
        :return: the buffer entry or an empty entry.
        :raises AttributeError: when the buffer is empty and there is no tray.
        """
        return self.container[1].get_tray()

    def get_num_trays(self) -> int:
        """
        Get how many trays there are.

        :rtype: int
        :return: the number of trays there are.
        """
        return isinstance(self.get_bay_entry(), TrayEntry) + isinstance(self.get_buffer_entry(), TrayEntry)

    def get_num_entries_free(self) -> int:
        count = 0
        for entry in self.container:
            if isinstance(entry, EmptyEntry):
                count += 1
        return count

    def is_full(self) -> bool:
        return self.is_buffer_full() and self.is_bay_full()

    def is_empty(self) -> bool:
        return not self.is_buffer_full() and not self.is_bay_full()

    def is_buffer_full(self) -> bool:
        """
        Check if the buffer is full.

        :rtype: bool
        :return: ``True`` if is full, ``False`` otherwise.
        """
        # check if the first position of buffer have a Tray
        return isinstance(self.get_buffer_entry(), TrayEntry)

    def is_bay_full(self) -> bool:
        """
        Check if the bay is full.

        :rtype: bool
        :return: ``True`` if is full, ``False`` otherwise.
        """
        # check if the first position of bay have a Tray
        return isinstance(self.get_bay_entry(), TrayEntry)

    def add_tray(self, tray: Tray):
        """
        Add a tray in the buffer area or show as an output (bay).

        :type tray: Tray
        :param tray: to show or to save.
        :raises RuntimeError: if the tray already exists.
        :raises ValueError: if the tray is longer or wider that the carousel.
        """
        if not (tray.length < self.length and tray.width < self.width):
            logger.error("A tray cannot be longer or wider than the carousel")
            raise ValueError

        first_y = self.num_entries + self.hole + self.bay
        is_bay_full = self.is_bay_full()

        # if the carousel is full, exception
        if self.is_buffer_full() and is_bay_full:
            raise RuntimeError("Collision!")

        # add the trayEntry in the buffer iff the bay is full
        self._create_tray_entry(tray, first_y, is_buffer=is_bay_full)

    def _create_tray_entry(self, tray: Tray, first_y: int, is_buffer: bool):
        """
        Create a tray entry.

        :type tray: Tray
        :type first_y: int
        :type is_buffer: bool
        :param tray: the tray to insert.
        :param first_y: the y position of the tray to insert.
        :param is_buffer: ``True`` if to insert in the buffer position, ``False`` if to insert in the bay position.
        """
        # initialize positions
        if is_buffer:
            first_y += self.buffer
        tray_entry = TrayEntry(self.offset_x, first_y)
        # connect Tray to entry
        tray_entry.add_tray(tray)
        # add to container
        self.container[int(is_buffer)] = tray_entry
        # connect Entry just added to relative Tray
        tray.set_first_tray_entry(tray_entry)

    def remove_tray(self, tray: Tray) -> bool:
        """
        Remove a tray.

        :type tray: Tray
        :rtype: bool
        :param tray: the tray to remove.
        :return: ``True`` if the tray was removed, ``False`` otherwise.
        """
        first_entry: TrayEntry = tray.get_first_tray_entry()
        entry_y_to_rmv = first_entry.get_pos_y()
        entry_x_to_rmv = first_entry.get_offset_x()
        bay_entry: TrayEntry | EmptyEntry = self.container[0]
        buffer_entry: TrayEntry | EmptyEntry = self.container[1]

        if isinstance(bay_entry, TrayEntry) and bay_entry.get_tray() == tray:
            self.container[0] = EmptyEntry(entry_x_to_rmv, entry_y_to_rmv)
            return True
        elif isinstance(buffer_entry, TrayEntry) and buffer_entry.get_tray() == tray:
            self.container[1] = EmptyEntry(entry_x_to_rmv, entry_y_to_rmv)
            return True
        return False
