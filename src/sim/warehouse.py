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
from simpy import Environment
from src.sim.status_warehouse.enum_warehouse import EnumWarehouse
from src.sim.warehouse_configuration_singleton import WarehouseConfigurationSingleton
from src.sim.drawer import Drawer
from src.sim.status_warehouse.container.carousel import Carousel
from src.sim.status_warehouse.container.column import Column
from src.sim.status_warehouse.entry.drawer_entry import DrawerEntry


logger = logging.getLogger(__name__)
__VERSION__ = '0.0.1'



class MinimumOffsetReturns(NamedTuple):
    """ Values returned by the get_minimum_offset method. """
    index: int
    offset: int


def gen_materials_and_drawer(num_drawers: int, num_materials: int,
                             rand_num_drawers: int, col: Column) -> list:
    """
    Generate drawers and materials.

    :type num_drawers: int
    :type num_materials: int
    :type rand_num_drawers: int
    :type col: Column
    :rtype: list
    :param num_drawers: number of drawers to create in the warehouse
    :param num_materials: number of materials to create in the drawers
    :param rand_num_drawers: number of drawers to generate
    :param col: column selected where to put the drawers
    :return: [number of drawers left, number of materials left]
    """
    from src.sim.material import gen_rand_materials

    # generate "rand_num_drawers" drawers
    for rand_num in range(rand_num_drawers):
        num_materials_to_put = 0
        materials = None
        # check if there are materials to generate
        if num_materials > 0:
            # generate a value of materials to insert
            num_materials_to_put = random.randint(1, num_materials)
            materials = gen_rand_materials(num_materials_to_put)

        # check if there is space in warehouse
        remaining_avail_entry = col.get_height_col() - col.get_num_entries_occupied()
        if remaining_avail_entry >= 1:
            # insert empty drawer
            drawer_to_insert = Drawer(materials)
            # looking for the index where put the drawer
            index = check_minimum_space([col], drawer_to_insert.get_max_num_space(), col.get_height_col())[0]
            # if the height is correct, insert
            if index != -1:
                # insert the drawer
                col.add_drawer(drawer_to_insert, index)
                # update local counter
                num_materials -= num_materials_to_put
                num_drawers -= 1
        # if there isn't space in the column
        else:
            # stop to put drawers inside this column
            break

    return [num_drawers, num_materials]


def check_minimum_space(list_cols: list, space_req: int, height_entry_col: int) -> list:
    """
    Algorithm to decide where insert a drawer.

    :type list_cols: list
    :type space_req: int
    :type height_entry_col: int
    :rtype: list
    :param list_cols: list of columns.
    :param space_req: space requested from drawer.
    :param height_entry_col: the height of warehouse
    :return: if there is a space [index_position_where_insert, column_where_insert].
    :raise ValueError: if there is no more space in the warehouse.
    """
    # result struct:
    # [ min_space requested,
    #   highest index found in the column,
    #   pointer to the column ]
    result = [0, height_entry_col, 0]

    # calculate minimum space and search lower index
    for column in list_cols:
        [min_space, start_index] = min_search_alg(column, space_req)
        # start_index < result[1]: to choice the lowest index btw columns
        if min_space != -1 and start_index < result[1]:
            result = [min_space, start_index, column]

    # if warehouse is full
    if result[0] == -1:
        raise ValueError("The warehouse is full! Please, check the check_minimum_space function")

    return [result[1], result[2]]


def min_search_alg(self: Column, space_req: int) -> list:
    """
    Algorithm to calculate a minimum space inside a column.

    :type self: Column
    :type space_req: int
    :rtype: list
    :param self: Column object used to calculate minimum space.
    :param space_req: space requested from drawer.
    :return: negative values if there isn't any space, otherwise [space_requested, index_position_where_insert].
    """
    from src.sim.status_warehouse.entry.empty_entry import EmptyEntry
    min_space = self.get_height_warehouse()
    count = 0
    start_index = self.get_height_last_position()
    container = self.get_container()
    height_last_pos = self.get_height_last_position()
    index = height_last_pos

    ############################
    # Minimum search algorithm #
    ############################

    # verify the highest position
    if type(container[start_index - 1]) is EmptyEntry and space_req <= height_last_pos:
        start_index = start_index - space_req
        min_space = height_last_pos
        return [min_space, start_index]

    for i in range(index, len(container)):
        entry = container[i]
        index += 1
        # if the position is empty
        if type(entry) is EmptyEntry:
            # count number of spaces
            count += 1
        else:
            # otherwise, if it's minimum and there is enough space
            if (count < min_space) & (count >= space_req):
                # update check values
                min_space = count
                start_index = i - count
            # restart the count with reset
            count = 0

    # if warehouse is empty
    if min_space == self.get_height_warehouse():
        if count == 0:
            # double security check
            for entry in container:
                # if it isn't empty
                if type(entry) is Drawer:
                    # raise IndexError("There isn't any space for this drawer.")
                    return [-1, -1]
            min_space = len(container)
        else:
            # update check values
            min_space = count
            start_index = index - count

    # if the last position is better and free
    if space_req < height_last_pos < min_space and type(container[height_last_pos - 1]) is EmptyEntry:
        min_space = space_req
        start_index = height_last_pos - 1
    else:
        # alloc only minimum space
        if min_space >= space_req:
            min_space = space_req
        else:
            # otherwise there isn't any space
            if min_space < space_req:
                # raise IndexError("There isn't any space for this drawer.")
                return [-1, -1]

    return [min_space, start_index]


class Warehouse:
    """
    Representation of the real warehouse.
    It contains all the information about the warehouse and the methods for running a simulation.
    """

    def __init__(self):
        from src.sim.material import gen_rand_material

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
        self.env = None
        self.simulation = None
        self.supp_drawer = None
        self.pos_y_floor = self.carousel.get_deposit_entry().get_pos_y()
        self.events_to_simulate = []

        # time of simulation
        self.sim_time = config["simulation"].get("time", None)
        # number of actions
        self.sim_num_actions = config["simulation"]["num_actions"]
        # generate a configuration based on JSON
        if config["simulation"]["gen_deposit"]:
            self.carousel.add_drawer(drawer=Drawer([gen_rand_material()]))
        if config["simulation"]["gen_buffer"]:
            self.carousel.add_drawer(drawer=Drawer([gen_rand_material()]))
        self.gen_rand(num_drawers=config["simulation"]["drawers_to_gen"],
                      num_materials=config["simulation"]["materials_to_gen"])

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
        copy_oby.env = self.get_environment()
        copy_oby.simulation = self.get_simulation()
        copy_oby.events_to_simulate = self.get_events_to_simulate()
        copy_oby.sim_time = self.get_sim_time()
        copy_oby.sim_num_actions = self.get_sim_num_actions()
        return copy_oby

    def __eq__(self, other):
        return (
            isinstance(other, Warehouse) and
            self.get_height() == other.get_height() and
            self.get_cols_container() == other.get_cols_container() and
            self.get_carousel() == other.get_carousel() and
            self.get_environment() == other.get_environment() and
            self.get_simulation() == other.get_simulation() and
            self.get_def_space() == other.get_def_space() and
            self.get_speed_per_sec() == other.get_speed_per_sec() and
            self.get_max_height_material() == other.get_max_height_material() and
            self.get_pos_y_floor() == other.get_pos_y_floor() and
            self.get_num_drawers() == other.get_num_drawers() and
            self.get_sim_time() == other.get_sim_time() and
            self.get_sim_num_actions() == other.get_sim_num_actions() and
            self.get_events_to_simulate() == other.get_events_to_simulate()
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

    def get_environment(self) -> Environment:
        """
        Get the environment object used for the simulation.

        :rtype: Environment
        :return: SimPy environment object used for the simulation.
        """
        return self.env

    def get_simulation(self):
        """
        Get the simulation object used to control the simulation.

        :rtype: Simulation
        :return: the simulation object used to control the simulation.
        """
        return self.simulation

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

    def get_sim_time(self) -> int | None:
        """
        The maximum time of the simulation (config value).

        :rtype: int or None
        :return: time of the simulation or None if it isn't specified.
        """
        return self.sim_time

    def get_sim_num_actions(self) -> int:
        """
        Get the number of actions taken by the simulation.

        :rtype: int
        :return: the number of actions taken by the simulation.
        """
        return self.sim_num_actions

    def get_events_to_simulate(self) -> list[str]:
        """
        Get the list of events to simulate.

        :rtype: list[str]
        :return: a list of events to simulate.
        """
        return self.events_to_simulate

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
        for col in self.get_cols_container():
            if col.get_num_entries_free() > 0:
                return False
        return True

    def go_to_deposit(self):
        """
        Simulation method used to go to deposit.
        """
        # take current position (y)
        curr_pos = self.get_pos_y_floor()
        # take destination position (y)
        dep_pos = self.get_carousel().get_deposit_entry().get_pos_y()
        yield self.env.timeout(self.vertical_move(curr_pos, dep_pos))
        # set new y position of the floor
        self.set_pos_y_floor(dep_pos)

    def go_to_buffer(self):
        """
        Simulation method used to go to buffer.
        """
        # take current position (y)
        curr_pos = self.get_pos_y_floor()
        # take destination position (y)
        buf_pos = self.get_carousel().get_buffer_entry().get_pos_y()
        yield self.env.timeout(self.vertical_move(curr_pos, buf_pos))
        # set new y position of the floor
        self.set_pos_y_floor(buf_pos)

    # TODO: to optimize destination parameter
    def load_in_carousel(self, drawer_to_insert: Drawer, destination: EnumWarehouse, load_in_buffer: bool):
        """
        Simulation method used to load the carousel into the warehouse.

        :type drawer_to_insert: Drawer
        :type destination: EnumWarehouse
        :type load_in_buffer: bool
        :param drawer_to_insert: drawer that will be inserted into the warehouse
        :param destination: destination of the drawer
        :param load_in_buffer: True to load the carousel into the buffer, otherwise into the deposit (bay)
        """
        y_dep = self.get_carousel().get_deposit_entry().get_pos_y()
        y_buf = self.get_carousel().get_buffer_entry().get_pos_y()
        # update the y position
        drawer_to_insert.set_best_y(y_dep)

        # calculate time to move (y)
        if load_in_buffer:
            # if the deposit is full but the buffer isn't full
            if not self.get_carousel().is_buffer_full():
                # update the y destination
                drawer_to_insert.set_best_y(y_buf)
                logger.debug(f"Time {self.env.now:5.2f} - Deposit is full! Start vertical move to buffer")
                yield self.env.timeout(self.vertical_move(start_pos=y_dep, end_pos=y_buf))
                # set new y position of the floor
                self.set_pos_y_floor(y_buf)
                logger.debug(f"Time {self.env.now:5.2f} - Start to load in the buffer")
            else:
                raise NotImplementedError("Deposit and buffer are full! Collision!")

        # and load inside the carousel
        yield self.env.process(self.load(drawer_to_insert, destination))

    def loading_buffer_and_remove(self):
        """
        Vertical movement of carousel loading from buffer to deposit.
        """
        buffer: DrawerEntry = self.get_carousel().get_buffer_entry()

        # calculate loading buffer time
        start_pos = buffer.get_pos_y()
        end_pos = self.get_carousel().get_deposit_entry().get_pos_y()
        loading_buffer_time = self.vertical_move(start_pos, end_pos)

        # exec simulate
        yield self.env.timeout(loading_buffer_time)

        # obtain the drawer inside the buffer
        drawer_to_show = buffer.get_drawer()
        # remove from buffer
        self.get_carousel().remove_drawer(drawer_to_show)
        # and insert drawer in correct position (outside)
        self.get_carousel().add_drawer(drawer_to_show)

    def vertical_move(self, start_pos: int, end_pos: int) -> float:
        """
        A simple vertical movement of the floor or the drawer inside the carousel (buffer to deposit).

        :type start_pos: int
        :type end_pos: int
        :rtype: float
        :param start_pos: starting position
        :param end_pos: ending position
        :return: distance travelled divided by speed per second
        """
        # calculate the distance of index between two points
        index_distance = abs(end_pos - start_pos)
        # calculate effective distance with real measures
        eff_distance = index_distance * self.get_def_space()
        # formula of vertical move
        vertical_move = (eff_distance / 100) / self.get_speed_per_sec()
        return vertical_move

    def allocate_best_pos(self, drawer: Drawer):
        """
        Simulation method used to allocate the best position of the drawer in the warehouse.

        :type drawer: Drawer
        :param drawer: drawer to allocate
        """
        # start position
        start_pos = self.get_pos_y_floor()
        # calculate destination position
        minimum = check_minimum_space(self.get_cols_container(),
                                      drawer.get_max_num_space(),
                                      self.get_height() // self.get_def_space())
        pos_to_insert = minimum[0]
        # temporarily save the coordinates
        drawer.set_best_y(minimum[0])
        drawer.set_best_offset_x(minimum[1].get_offset_x())
        # start the move
        vertical_move = self.vertical_move(start_pos, pos_to_insert)
        yield self.env.timeout(vertical_move)
        # set new y position of the floor
        self.set_pos_y_floor(pos_to_insert)

    def reach_drawer_height(self, drawer: Drawer):
        """
        Simulation method used to reach the height of the drawer in the warehouse.

        :type drawer: Drawer
        :param drawer: drawer to reach
        """
        # save coordinates inside drawer
        y = drawer.get_first_drawerEntry().get_pos_y()
        x = drawer.get_first_drawerEntry().get_offset_x()
        drawer.set_best_y(y)
        drawer.set_best_offset_x(x)
        # start the move
        vertical_move = self.vertical_move(start_pos=self.get_pos_y_floor(),
                                           end_pos=y)
        yield self.env.timeout(vertical_move)
        # set new y position of the floor
        self.set_pos_y_floor(y)

    def unload(self, drawer: Drawer, rmv_from_cols: bool):
        """
        Simulation method used to unload a drawer from the carousel or from the columns.

        :type drawer: Drawer
        :type rmv_from_cols: bool
        :param drawer: drawer to unload
        :param rmv_from_cols: True to unload the drawer from the columns, otherwise unload from the carousel
        """
        # take x offset
        offset_x_drawer = drawer.get_first_drawerEntry().get_offset_x()
        # start the move
        yield self.env.timeout(self.horiz_move(offset_x_drawer))
        # update warehouse
        # if drawer hasn't been removed
        if rmv_from_cols:
            for col in self.get_cols_container():
                if col.remove_drawer(drawer):
                    break
        else:
            self.get_carousel().remove_drawer(drawer)
        # if not self.get_carousel().remove_drawer(drawer):
        #     # find in a column and terminate
        #     for col in self.get_cols_container():
        #         if col.remove_drawer(drawer):
        #             break

    def load(self, drawer: Drawer, destination: EnumWarehouse):
        """
        Simulation method used to load the drawer into the warehouse.

        :type drawer: Drawer
        :type destination: EnumWarehouse
        :param drawer: drawer to load
        :param destination: destination of the drawer
        """
        from src.sim.status_warehouse.enum_warehouse import EnumWarehouse
        # take destination coordinates
        dest_x_drawer = drawer.get_best_offset_x()
        dest_y_drawer = drawer.get_best_y()
        # start the move
        yield self.env.timeout(self.horiz_move(dest_x_drawer))
        # update warehouse
        # if destination is carousel, add
        if destination == EnumWarehouse.CAROUSEL:
            self.get_carousel().add_drawer(drawer, dest_y_drawer)
        else:
            # otherwise, check the offset of column
            for col in self.get_cols_container():
                if col.get_offset_x() == dest_x_drawer:
                    col.add_drawer(drawer, dest_y_drawer)
                    break

    def horiz_move(self, offset_x: int) -> float:
        """
        Search in the column/carousel where is the drawer.

        :type offset_x: int
        :rtype: float
        :param offset_x: offset of the drawer to search
        :return: the time estimated
        """
        # check the carousel
        if self.get_carousel().get_offset_x() == offset_x:
            return (self.get_carousel().get_width() / 100) / self.get_speed_per_sec()
        else:
            # check every column
            for col in self.get_cols_container():
                if col.get_offset_x() == offset_x:
                    return (col.get_width() / 100) / self.get_speed_per_sec()

    def gen_rand(self, num_drawers: int, num_materials: int):
        """
        Generate a random warehouse.

        :type num_drawers: int
        :type num_materials: int
        :param num_drawers: numbers of drawers
        :param num_materials: numbers of materials
        """
        warehouse_is_full = False

        # until there are drawers to insert and the warehouse isn't full
        # TODO: rmv warehouse_is_full and use directly the method
        while num_drawers > 0 and not warehouse_is_full:
            # check available space in warehouse
            if self.is_full():
                warehouse_is_full = True
            else:
                # choice a random column
                rand_col: Column = random.choice(self.get_cols_container())
                # generate random number to decide how many drawers insert inside the column
                rand_num_drawers = random.randint(1, num_drawers)
                [num_drawers, num_materials] = gen_materials_and_drawer(num_drawers, num_materials,
                                                                        rand_num_drawers, rand_col)
        # if there aren't anything else to add
        if num_drawers == 0 and num_materials == 0:
            logger.info("The creation of random warehouse is completed.")
        else:
            # if there aren't more drawers but some materials...
            if num_drawers == 0:
                logger.warning(f"num_materials left: {num_materials}")
            else:
                # if the warehouse is completely full
                logger.warning(f"The warehouse is full, num_drawers left: {num_drawers}, num_materials left: {num_materials}")

    def run_simulation(self):
        """
        Run a new simulation using the same parameters.
        Note: the simulation will create a new sequence of actions.
        """
        from src.sim.simulation import Simulation

        self.env = Environment()
        self.simulation = Simulation(self.env, self)

        balance_wh = 0
        # create list of event alias
        alias_events = ["send_back", "extract_drawer", "ins_mat", "rmv_mat"]

        # if the deposit or the buffer are full, then update the counter
        if type(self.get_carousel().get_deposit_entry()) is DrawerEntry:
            balance_wh += 1
        if type(self.get_carousel().get_buffer_entry()) is DrawerEntry:
            balance_wh += 1

        logger.info("Creating the sequence of actions for the simulation.")
        for num_action in range(self.get_sim_num_actions()):
            good_choice = False
            rand_event = ""
            while good_choice is False:
                # select an event
                rand_event = random.choice(alias_events)
                # check if the choice is correct
                if 1 <= balance_wh <= 2 and (rand_event == "send_back" or
                                             rand_event == "ins_mat" or
                                             rand_event == "rmv_mat"):
                    good_choice = True
                    if rand_event == "send_back":
                        balance_wh -= 1
                else:
                    if 0 <= balance_wh < 2 and rand_event == "extract_drawer":
                        good_choice = True
                        balance_wh += 1
            self.get_events_to_simulate().append(rand_event)
        logger.info("Sequence of actions created.")

        # create the simulation
        self.get_environment().process(self.get_simulation().simulate_actions(self.get_events_to_simulate()))

        # run simulation
        self.get_environment().run(until=self.sim_time)

    def new_simulation(self, num_actions: int, num_gen_drawers: int, num_gen_materials: int,
                       gen_deposit: bool, gen_buffer: bool, time: int=None):
        """
        Run a new simulation using custom parameters.

        :type num_actions: int
        :type num_gen_drawers: int
        :type num_gen_materials: int
        :type gen_deposit: bool
        :type gen_buffer: bool
        :type time: int or None
        :param num_actions: number of actions to simulate
        :param num_gen_drawers: number of drawers to generate in the warehouse
        :param num_gen_materials: number of materials to generate in the warehouse
        :param gen_deposit: True to generate a drawer in the deposit, False otherwise
        :param gen_buffer: True to generate a drawer in the buffer, False otherwise
        :param time: the maximum time of the simulation, otherwise None to remove the limit
        """
        from src.sim.material import gen_rand_material

        # clean warehouse datas:
        # - clean all columns entry
        for column in self.columns_container:
            column.reset_container()
        # - clean all carousel entry
        self.carousel.reset_container()

        # setting new simulation settings:
        self.sim_time = time
        self.sim_num_actions = num_actions
        if gen_deposit:
            # create a new one
            self.carousel.add_drawer(drawer=Drawer([gen_rand_material()]))
        if gen_buffer:
            # create a new one
            self.carousel.add_drawer(drawer=Drawer([gen_rand_material()]))

        # generate drawers and materials
        self.gen_rand(num_drawers=num_gen_drawers, num_materials=num_gen_materials)

        # reset events to simulate list
        self.events_to_simulate.clear()

        # run a new simulation
        self.run_simulation()


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
