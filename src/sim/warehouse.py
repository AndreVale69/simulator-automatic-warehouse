import logging
from typing import NamedTuple

from src.sim.configuration import NO_CONSOLE_LOG, DEBUG_LOG, FILENAME_DEBUG_LOG

if NO_CONSOLE_LOG:
    logging.basicConfig(format='%(asctime)s - [%(levelname)s] - (%(name)s) - %(message)s')
elif DEBUG_LOG:
    logging.basicConfig(format='%(asctime)s - [%(levelname)s] - (%(name)s) - %(message)s',
                        level=logging.DEBUG)
elif FILENAME_DEBUG_LOG:
    logging.basicConfig(format='%(asctime)s - [%(levelname)s] - (%(name)s) - %(message)s',
                        level=logging.DEBUG, filename=f'{FILENAME_DEBUG_LOG}', filemode='w')
else:
    logging.basicConfig(format='%(asctime)s - [%(levelname)s] - (%(name)s) - %(message)s',
                        level=logging.INFO)


import copy
import random
from src.sim.warehouse_configuration_singleton import WarehouseConfigurationSingleton
from src.sim.drawer import Drawer
from src.sim.status_warehouse.container.carousel import Carousel
from src.sim.status_warehouse.container.column import Column
from src.sim.material import gen_rand_material

logger = logging.getLogger(__name__)
__VERSION__ = '1.0.0'



class MinimumOffsetReturns(NamedTuple):
    """ Values returned by the get_minimum_offset method. """
    index: int
    offset: int


class Warehouse:
    """
    Representation of the real warehouse.
    It contains all the information about the warehouse and the methods for running a simulation.
    """

    def __init__(self):
        # open YAML configuration file
        config: dict = WarehouseConfigurationSingleton.get_instance().get_configuration()

        self.height = config["height_warehouse"]

        # add all columns taken from YAML
        self.columns_container = []
        # all columns must be added from minimum offset_x to greats offset_x
        # respecting this order
        for col_data in config["columns"]:
            self.add_column(Column(col_data, self))
        self.carousel = Carousel(config["carousel"], self)

        self.def_space = config["default_height_space"]
        self.speed_per_sec = config["speed_per_sec"]
        self.max_height_material = config["carousel"]["buffer_height"] // self.get_def_space()
        self.pos_y_floor = self.carousel.get_deposit_entry().get_pos_y()

        # generate a configuration based on YAML
        self.gen_rand(
            gen_deposit=config["simulation"]["gen_deposit"],
            gen_buffer=config["simulation"]["gen_buffer"],
            num_drawers=config["simulation"]["drawers_to_gen"],
            num_materials=config["simulation"]["materials_to_gen"]
        )

    def __deepcopy__(self, memo):
        copy_oby = Warehouse()
        copy_oby.height = self.get_height()
        copy_oby.columns_container = copy.deepcopy(self.get_cols_container(), memo)
        for col in copy_oby.columns_container:
            col.set_warehouse(copy_oby)
        copy_oby.carousel = copy.deepcopy(self.get_carousel(), memo)
        copy_oby.carousel.set_warehouse(copy_oby)
        copy_oby.def_space = self.get_def_space()
        copy_oby.speed_per_sec = self.get_speed_per_sec()
        return copy_oby

    def __eq__(self, other):
        return (
            isinstance(other, Warehouse) and
            self.get_height() == other.get_height() and
            self.get_cols_container() == other.get_cols_container() and
            self.get_carousel() == other.get_carousel() and
            self.get_def_space() == other.get_def_space() and
            self.get_speed_per_sec() == other.get_speed_per_sec() and
            self.get_max_height_material() == other.get_max_height_material() and
            self.get_pos_y_floor() == other.get_pos_y_floor() and
            self.get_num_drawers() == other.get_num_drawers()
        )

    def __hash__(self):
        return (
            13 ^
            hash(self.get_height()) ^
            hash(tuple(self.get_cols_container())) ^
            hash(self.get_carousel()) ^
            hash(self.get_def_space()) ^
            hash(self.get_speed_per_sec()) ^
            hash(self.get_max_height_material()) ^
            hash(self.get_pos_y_floor()) ^
            hash(self.get_num_drawers())
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
        Get the (index) column of the warehouse.

        :type index: int
        :rtype: Column
        :param index: the index of the column.
        :return: the columns of the warehouse.
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
        Get the height (distance) between two drawers (config value).

        :rtype: int
        :return: the height (distance) between two drawers (config value).
        """
        return self.def_space

    def get_speed_per_sec(self) -> int:
        """
        Get the speed of the platform.
        It's used by the simulator to calculate the time it takes to move between columns and up and down.

        :rtype: int
        :return: the speed of the platform.
        """
        return self.speed_per_sec

    def get_max_height_material(self) -> int:
        """
        Get the maximum height of a material.
        It's the value calculated by dividing the buffer height by the return value of get_def_space().

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

    def get_num_drawers(self) -> int:
        """
        Get the number of drawers in the warehouse.

        :rtype: int
        :return: the number of drawers in the warehouse.
        """
        ris = 0
        for col in self.get_cols_container():
            ris += col.get_num_drawers()
        ris += self.get_carousel().get_num_drawers()
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
        min_offset = self.get_column(0).get_offset_x()
        index = 0
        for i, column in enumerate(self.get_cols_container()):
            if (col_offset_x := column.get_offset_x()) < min_offset:
                min_offset = col_offset_x
                index = i
        return MinimumOffsetReturns(index=index, offset=min_offset)

    def set_pos_y_floor(self, pos: int):
        """
        Set the y-position of the floor.

        :param pos: new position of the floor.
        """
        assert pos >= 0, "y-position of the floor must be positive!"
        self.pos_y_floor = pos

    def add_column(self, col: Column):
        """
        Add a column to the container of the columns the warehouse.

        :type col: Column
        :param col: the column to add.
        """
        assert type(col) is Column, "You cannot add a type other than Column!"
        self.get_cols_container().append(col)

    def pop_column(self, index: int = -1) -> Column:
        """
        Pop a column from the container of the columns the warehouse.
        If no index is given, the last column of the container is removed by default.

        :type index: int
        :rtype: Column
        :param index: the index of the column to pop.
        :raises IndexError: if the index is out of range or the column is empty.
        :return: the column of the warehouse removed.
        """
        return self.get_cols_container().pop(index)

    def remove_column(self, value: Column):
        """
        Remove a column from the container of the warehouse.
        If two or more values are the same, remove the first one found.

        :type value: Column
        :param value: the Column to remove.
        :raises ValueError: if the Column is not in a container.
        """
        self.get_cols_container().remove(value)

    def is_full(self) -> bool:
        """
        Verify if there is a space inside the warehouse.

        :rtype: bool
        :return: True if there is a space inside the warehouse, otherwise False
        """
        return False not in [col.is_full() for col in self.get_cols_container()]

    def gen_rand(self, gen_deposit: bool, gen_buffer: bool, num_drawers: int, num_materials: int):
        """
        Generate a random warehouse.
        Be careful!
        Every entry in the warehouse will be reset!

        :type gen_deposit: bool
        :type gen_buffer: bool
        :type num_drawers: int
        :type num_materials: int
        :param gen_deposit: True generate a drawer in the deposit, otherwise generate an EmptyEntry
        :param gen_buffer: True generate a drawer in the buffer, otherwise generate an EmptyEntry
        :param num_drawers: numbers of drawers
        :param num_materials: numbers of materials
        """
        # cleanup the warehouse
        self.cleanup()

        # generate a drawer in the deposit and/or buffer
        if gen_deposit:
            # create a new one
            self.carousel.add_drawer(drawer=Drawer([gen_rand_material()]))
        if gen_buffer:
            # create a new one
            self.carousel.add_drawer(drawer=Drawer([gen_rand_material()]))

        # populate the columns
        columns: list[Column] = self.get_cols_container()
        # until there are drawers to insert and the warehouse isn't full
        while num_drawers > 0 and not self.is_full():
            # choice a random column
            rand_col: Column = random.choice(columns)
            # generate random number to decide how many drawers insert inside the column
            rand_num_drawers = random.randint(1, num_drawers)
            res = rand_col.gen_materials_and_drawers(rand_num_drawers, num_materials)
            num_drawers -= res.drawers_inserted
            num_materials -= res.materials_inserted
        # if there isn't anything else to add
        if num_drawers == 0 and num_materials == 0:
            logger.info("The creation of random warehouse is completed.")
        else:
            # if there aren't more drawers but some materials...
            if num_drawers == 0:
                logger.warning(f"num_materials left: {num_materials}")
            else:
                # if the warehouse is completely full
                logger.warning(f"The warehouse is full, num_drawers left: {num_drawers}, num_materials left: {num_materials}")

    def choice_random_drawer(self) -> Drawer:
        """
        Choose a random drawer from the warehouse.

        :rtype: Drawer
        :return: the random drawer chosen from the warehouse
        """
        container_drawer_entry = []
        for col in self.get_cols_container():
            container_drawer_entry.extend(col.get_drawers())
        assert len(container_drawer_entry) > 0, "The warehouse is empty!"
        return random.choice(container_drawer_entry)

    def cleanup(self):
        """ Cleanup the warehouse. Each Entry will be EmptyEntry. """
        for column in self.columns_container:
            column.reset_container()
        self.carousel.reset_container()