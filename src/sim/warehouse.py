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
from src.sim.utils.decide_position_algorithm.enum_algorithm import Algorithm
from src.sim.utils.decide_position_algorithm.algorithm import decide_position
from src.sim.status_warehouse.enum_warehouse import EnumWarehouse
from src.sim.warehouse_configuration_singleton import WarehouseConfigurationSingleton
from src.sim.drawer import Drawer
from src.sim.status_warehouse.container.carousel import Carousel
from src.sim.status_warehouse.container.column import Column
from src.sim.status_warehouse.entry.drawer_entry import DrawerEntry


logger = logging.getLogger(__name__)
__VERSION__ = '0.0.2'



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

    def __hash__(self):
        return (
            13 ^
            hash(self.get_height()) ^
            hash(tuple(self.get_cols_container())) ^
            hash(self.get_carousel()) ^
            # hash(self.get_environment()) ^
            # hash(self.get_simulation()) ^
            hash(self.get_def_space()) ^
            hash(self.get_speed_per_sec()) ^
            hash(self.get_max_height_material()) ^
            hash(self.get_pos_y_floor()) ^
            hash(self.get_num_drawers()) ^
            hash(self.get_sim_time()) ^
            hash(self.get_sim_num_actions()) ^
            hash(tuple(self.get_events_to_simulate()))
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

    def get_num_columns(self) -> int:
        """
        Get the number of columns in the warehouse.

        :rtype: int
        :return: the number of columns in the warehouse.
        """
        return len(self.columns_container)

    # TODO: move to Simulation class
    def get_sim_time(self) -> int | None:
        """
        The maximum time of the simulation (config value).

        :rtype: int or None
        :return: time of the simulation or None if it isn't specified.
        """
        return self.sim_time

    # TODO: move to Simulation class
    def get_sim_num_actions(self) -> int:
        """
        Get the number of actions taken by the simulation.

        :rtype: int
        :return: the number of actions taken by the simulation.
        """
        return self.sim_num_actions

    # TODO: move to Simulation class
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
        return False not in [col.is_full() for col in self.get_cols_container()]

    # TODO: simulation method, brainstorming...
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

    # TODO: simulation method, brainstorming...
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

    # TODO: simulation method, brainstorming...
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

    # TODO: simulation method, brainstorming...
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

    # TODO: simulation method, brainstorming...
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

    # TODO: simulation method, brainstorming...
    def allocate_best_pos(self, drawer: Drawer):
        """
        Simulation method used to allocate the best position of the drawer in the warehouse.

        :type drawer: Drawer
        :param drawer: drawer to allocate
        """
        # start position
        start_pos = self.get_pos_y_floor()
        # calculate destination position
        decide_position_res = decide_position(
            columns=self.get_cols_container(),
            space_req=drawer.get_num_space_occupied(),
            algorithm=Algorithm.HIGH_POSITION
        )
        pos_to_insert = decide_position_res.index
        # temporarily save the coordinates
        drawer.set_best_y(pos_to_insert)
        drawer.set_best_offset_x(decide_position_res.column.get_offset_x())
        # start the move
        vertical_move = self.vertical_move(start_pos, pos_to_insert)
        yield self.env.timeout(vertical_move)
        # set new y position of the floor
        self.set_pos_y_floor(pos_to_insert)

    # TODO: simulation method, brainstorming...
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

    # TODO: simulation method, brainstorming...
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

    # TODO: simulation method, brainstorming...
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

    # TODO: simulation method, brainstorming...
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
        from src.sim.material import gen_rand_material

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
        # setting new simulation settings:
        self.sim_time = time
        self.sim_num_actions = num_actions

        # random gen
        self.gen_rand(gen_deposit, gen_buffer, num_gen_drawers, num_gen_materials)

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

    def cleanup(self):
        """ Cleanup the warehouse. Each Entry will be EmptyEntry. """
        for column in self.columns_container:
            column.reset_container()
        self.carousel.reset_container()