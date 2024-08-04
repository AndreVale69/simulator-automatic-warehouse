from logging import basicConfig, DEBUG, INFO, getLogger
from dataclasses import dataclass

from automatic_warehouse.env_vars import NO_CONSOLE_LOG, DEBUG_LOG, FILENAME_DEBUG_LOG

if NO_CONSOLE_LOG:
    basicConfig(format='%(asctime)s - [%(levelname)s] - (%(name)s) - %(message)s')
elif DEBUG_LOG:
    basicConfig(format='%(asctime)s - [%(levelname)s] - (%(name)s) - %(message)s', level=DEBUG)
elif FILENAME_DEBUG_LOG:
    basicConfig(format='%(asctime)s - [%(levelname)s] - (%(name)s) - %(message)s', level=DEBUG,
                filename=f'{FILENAME_DEBUG_LOG}', filemode='w')
else:
    basicConfig(format='%(asctime)s - [%(levelname)s] - (%(name)s) - %(message)s', level=INFO)


from copy import deepcopy
from random import randint, choice
from automatic_warehouse.warehouse_configuration_singleton import WarehouseConfigurationSingleton, WarehouseConfiguration, ColumnConfiguration, CarouselConfiguration
from automatic_warehouse.status_warehouse.tray import Tray
from automatic_warehouse.status_warehouse.container.carousel import Carousel
from automatic_warehouse.status_warehouse.container.column import Column
from automatic_warehouse.status_warehouse.material import gen_rand_material

logger = getLogger(__name__)


@dataclass
class MinimumOffsetReturns:
    """ `Python Dataclass <https://docs.python.org/3/library/dataclasses.html>`_ - Values returned by the :attr:`Warehouse.get_minimum_offset` method. """
    index: int
    "Index of the minimum offset found."
    offset: int
    "Offset found."


class Warehouse:
    """
    Representation of the real warehouse.
    It contains all the information about the warehouse and 
    the methods for calculating the internal movements of its components.
    """

    def __init__(self):
        # open YAML configuration file
        config: WarehouseConfiguration = WarehouseConfigurationSingleton.get_instance().get_configuration()

        self.height = config.height_warehouse

        # add all columns taken from YAML
        self.columns_container: list[Column] = []
        self._columns_x_offset = set()
        # all columns must be added from minimum offset_x to greats offset_x
        # respecting this order
        for col_data in config.columns:
            self.add_column(Column(
                ColumnConfiguration(
                    length=col_data.length,
                    height=col_data.height,
                    x_offset=col_data.x_offset,
                    width=col_data.width,
                    height_last_position=col_data.height_last_position
                ),
                self
            ))
        self.carousel = Carousel(
            CarouselConfiguration(
                length=config.carousel.length,
                width=config.carousel.width,
                hole_height=config.carousel.hole_height,
                bay_height=config.carousel.bay_height,
                buffer_height=config.carousel.buffer_height,
                x_offset=config.carousel.x_offset
            ),
            self
        )

        self.def_space = config.default_height_space
        self.speed_per_sec = config.speed_per_sec
        self.max_height_material = config.carousel.buffer_height // self.def_space
        self.pos_y_floor = self.carousel.get_bay_entry().get_pos_y()

        # generate a configuration based on YAML
        self.gen_rand(
            gen_bay=config.simulation.gen_bay,
            gen_buffer=config.simulation.gen_buffer,
            num_trays=config.simulation.trays_to_gen,
            num_materials=config.simulation.materials_to_gen
        )

    def __deepcopy__(self, memo):
        copy_oby = Warehouse()
        copy_oby.height = self.height
        copy_oby.columns_container = deepcopy(self.columns_container, memo)
        for col in copy_oby.columns_container:
            col.set_warehouse(copy_oby)
        copy_oby.carousel = deepcopy(self.carousel, memo)
        copy_oby.carousel.set_warehouse(copy_oby)
        copy_oby.def_space = self.def_space
        copy_oby.speed_per_sec = self.speed_per_sec
        return copy_oby

    def __eq__(self, other):
        return (
            isinstance(other, Warehouse) and
            self.height == other.height and
            self.columns_container == other.columns_container and
            self.carousel == other.carousel and
            self.def_space == other.def_space and
            self.speed_per_sec == other.speed_per_sec and
            self.max_height_material == other.max_height_material and
            self.pos_y_floor == other.pos_y_floor and
            self.get_num_trays() == other.get_num_trays()
        )

    def __hash__(self):
        return (
            32831 ^
            hash(self.height) ^
            hash(tuple(self.columns_container)) ^
            hash(self.carousel) ^
            hash(self.def_space) ^
            hash(self.speed_per_sec) ^
            hash(self.max_height_material) ^
            hash(self.pos_y_floor) ^
            hash(self.get_num_trays())
        )

    def get_height(self) -> int:
        """
        Get the height of the warehouse.

        :rtype: int
        :return: the height of the warehouse.
        """
        return self.height

    def get_cols_container(self) -> list[Column]:
        """
        Get all the columns of the warehouse.

        :rtype: list[Column]
        :return: the columns of the warehouse.
        """
        return self.columns_container

    def get_column(self, index: int) -> Column:
        """
        Get the (i-)column of the warehouse.

        :type index: int
        :rtype: Column
        :param index: the index of the column.
        :return: get the column of the warehouse with the given index.
        :raises IndexError: list index out of range.
        """
        return self.columns_container[index]

    def get_carousel(self) -> Carousel:
        """
        Get the carousel of the warehouse.

        :rtype: Carousel
        :return: the carousel of the warehouse.
        """
        return self.carousel

    def get_def_space(self) -> int:
        """
        Get the height (distance) between two trays (config value).

        :rtype: int
        :return: the height (distance) between two trays (config value).
        """
        return self.def_space

    def get_speed_per_sec(self) -> int:
        """
        Get the speed of the platform (config value).
        It's used by the simulator to calculate the time it takes to move between columns and up and down.

        :rtype: int
        :return: the speed of the platform (config value).
        """
        return self.speed_per_sec

    def get_max_height_material(self) -> int:
        """
        Get the maximum height of a :class:`Material`.
        It's the value calculated by dividing the buffer height by 
        the return value of :attr:`get_def_space` method.

        :rtype: int
        :return: the maximum height of a material.
        """
        return self.max_height_material

    def get_pos_y_floor(self) -> int:
        """
        Get the y-position of the floor.
        It is used by the simulator to calculate the time it takes to move between columns and up and down.

        :rtype: int
        :return: the y-position of the floor.
        """
        return self.pos_y_floor

    def get_num_trays(self) -> int:
        """
        Get the number of trays in the warehouse.

        :rtype: int
        :return: the number of trays in the warehouse.
        """
        ris = 0
        for col in self.columns_container:
            ris += col.get_num_trays()
        ris += self.carousel.get_num_trays()
        return ris

    def get_num_columns(self) -> int:
        """
        Get the number of columns in the warehouse.

        :rtype: int
        :return: the number of columns in the warehouse.
        """
        return len(self.columns_container)

    def get_minimum_offset(self) -> MinimumOffsetReturns:
        """
        Calculate the minimum offset between the columns of the warehouse.

        :rtype: MinimumOffsetReturns
        :return: the index of the list and the offset.
        """
        min_offset, index = self.columns_container[0].get_offset_x(), 0
        for i, column in enumerate(self.columns_container):
            if (col_offset_x := column.get_offset_x()) < min_offset:
                min_offset, index = col_offset_x, i
        return MinimumOffsetReturns(index=index, offset=min_offset)

    def set_pos_y_floor(self, pos: int):
        """
        Set the y-position of the floor.

        :param pos: new position of the floor.
        :raises AssertionError: if the ``pos`` parameter is not greater than or equal to zero.
        """
        assert pos >= 0, "y-position of the floor must be positive!"
        self.pos_y_floor = pos

    def add_column(self, col: Column):
        """
        Add a column to the warehouse column container.

        :type col: Column
        :param col: the column to add.
        :raises ValueError: if the column ``x_offset`` is not unique.
        """
        assert type(col) is Column, "You cannot add a type other than Column!"
        if (offset_x := col.get_offset_x()) in self._columns_x_offset:
            raise ValueError(f"Each column should have a unique x_offset; Duplicate found: {offset_x}")
        self.columns_container.append(col)
        self._columns_x_offset.add(offset_x)

    def pop_column(self, index: int = -1) -> Column:
        """
        Remove a :class:`Column` from the column container in the warehouse.
        If no index is given, the last column of the container is removed by default.

        :type index: int
        :rtype: Column
        :param index: the index of the column to pop.
        :raises IndexError: if the index is out of range or the column is empty.
        :return: the column of the warehouse removed.
        """
        self._columns_x_offset.remove((col_removed := self.columns_container.pop(index)).get_offset_x())
        return col_removed

    def remove_column(self, value: Column):
        """
        Remove a column from the container of the warehouse.
        If two or more values are the same, remove the first one found.

        :type value: Column
        :param value: the column to remove.
        :raises ValueError: if the column is not in a container.
        """
        self.columns_container.remove(value)
        self._columns_x_offset.remove(value.get_offset_x())

    def is_full(self) -> bool:
        """
        Verify if there is a space inside the warehouse.

        :rtype: bool
        :return: ``True`` if there is a space inside the warehouse, otherwise ``False``.
        """
        return False not in [col.is_full() for col in self.columns_container]

    def gen_rand(self, gen_bay: bool, gen_buffer: bool, num_trays: int, num_materials: int):
        """
        Generate a random warehouse.
        **Be careful!
        Every entry in the warehouse will be reset!**

        :type gen_bay: bool
        :type gen_buffer: bool
        :type num_trays: int
        :type num_materials: int
        :param gen_bay: ``True`` generate a :class:`Tray` in the bay, otherwise generate an :class:`EmptyEntry`.
        :param gen_buffer: ``True`` generate a :class:`Tray` in the buffer, otherwise generate an :class:`EmptyEntry`.
        :param num_trays: numbers of trays.
        :param num_materials: numbers of materials.
        """
        # cleanup the warehouse
        self.cleanup()

        # generate a tray in the bay and/or buffer
        if gen_bay:
            # create a new one
            self.carousel.add_tray(tray=Tray(items=[gen_rand_material()]))
        if gen_buffer:
            # create a new one
            self.carousel.add_tray(tray=Tray(items=[gen_rand_material()]))

        # populate the columns
        columns = self.columns_container
        # until there are trays to insert and the warehouse isn't full
        while num_trays > 0 and not self.is_full():
            # choice a random column
            rand_col: Column = choice(columns)
            # generate random number to decide how many trays insert inside the column
            rand_num_trays = randint(1, num_trays)
            res = rand_col.gen_materials_and_trays(rand_num_trays, num_materials)
            num_trays -= res.trays_inserted
            num_materials -= res.materials_inserted
        # if there isn't anything else to add
        if num_trays == 0 and num_materials == 0:
            logger.info("The creation of random warehouse is completed.")
        else:
            logger.warning(f"The creation of random warehouse is not completed at 100%: "
                           f"trays left: {num_trays}, materials left: {num_materials}")

    def choice_random_tray(self) -> Tray:
        """
        Pick a random tray from the columns in the warehouse.

        :rtype: Tray
        :return: the random tray chosen from the columns in the warehouse.
        :raises AssertionError: if each column doesn't have a tray.
        """
        container_tray_entry = []
        for col in self.columns_container:
            container_tray_entry.extend(col.get_trays())
        assert len(container_tray_entry) > 0, "The warehouse is empty!"
        return choice(container_tray_entry)

    def cleanup(self):
        """ Cleanup the warehouse (columns and carousel). Each :class:`Entry` will be :class:`EmptyEntry`. """
        self.cleanup_columns()
        self.cleanup_carousel()

    def cleanup_columns(self):
        """ Cleanup the columns of the warehouse. Each :class:`Entry` will be :class:`EmptyEntry`. """
        for column in self.columns_container:
            column.reset_container()

    def cleanup_carousel(self):
        """ Cleanup the carousel of the warehouse. Each :class:`Entry` will be :class:`EmptyEntry`. """
        self.carousel.reset_container()
