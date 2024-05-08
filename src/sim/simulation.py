import copy
import logging
import simpy
from random import choice

from pandas import DataFrame

from src.sim.utils.decide_position_algorithm.algorithm import decide_position
from src.sim.utils.decide_position_algorithm.enum_algorithm import Algorithm
from src.sim.status_warehouse.entry.drawer_entry import DrawerEntry
from src.sim.drawer import Drawer
from src.sim.warehouse_configuration_singleton import WarehouseConfigurationSingleton
from src.sim.warehouse import Warehouse
from src.sim.status_warehouse.simulate_events.action_enum import ActionEnum
from src.sim.status_warehouse.enum_warehouse import EnumWarehouse

logger = logging.getLogger(__name__)



class Simulation:
    def __init__(self, warehouse: Warehouse):
        """
        The main simulation class.

        :type warehouse: Warehouse
        :param warehouse: the Warehouse used to perform the simulation.
        """
        # TODO: initial time as parameter? Brainstorming...
        self.env = simpy.Environment()
        # start the move process everytime an instance is created.
        self.warehouse = copy.deepcopy(warehouse)

        # allocation of carousel resources
        self.res_buffer = simpy.Resource(self.env, capacity=1)
        self.res_deposit = simpy.Resource(self.env, capacity=1)
        self.store_history = None

        config = WarehouseConfigurationSingleton.get_instance().get_configuration()
        self.sim_time: int | None = config["simulation"].get("time")
        self.sim_num_actions: int = config["simulation"]["num_actions"]
        self.events_to_simulate: list[str] = []

    def __eq__(self, other):
        return (
            isinstance(other, Simulation) and
            self.get_environment() == other.get_environment() and
            self.get_res_buffer() == other.get_res_buffer() and
            self.get_res_deposit() == other.get_res_deposit() and
            self.get_store_history() == other.get_store_history() and
            self.get_sim_time() == other.get_sim_time() and
            self.get_sim_num_actions() == other.get_sim_num_actions() and
            self.get_events_to_simulate() == other.get_events_to_simulate()
        )

    def get_environment(self) -> simpy.Environment:
        """
        Get the environment of SimPy.

        :rtype: simpy.Environment
        :return: the environment of SimPy.
        """
        return self.env

    def get_warehouse(self) -> Warehouse:
        """
        Get the Warehouse used to perform the simulation.

        :rtype: Warehouse
        :return: the Warehouse used to perform the simulation.
        """
        return self.warehouse

    def get_res_buffer(self) -> simpy.Resource:
        """
        Get the resource of the buffer.
        It can be thought of as a resource lock (see SimPy resource).

        :rtype: simpy.Resource
        :return: the resource of the buffer.
        """
        return self.res_buffer

    def get_res_deposit(self) -> simpy.Resource:
        """
        Get the resource of the deposit (bay).
        It can be thought of as a resource lock (see SimPy resource).

        :rtype: simpy.Resource
        :return: the resource of the deposit (bay).
        """
        return self.res_deposit

    def get_store_history(self) -> simpy.Store:
        """
        Get the SimPy store (see SimPy store) of the simulation.
        It is used to store the simulation history.

        :rtype: simpy.Store
        :return: the store of the simulation history.
        """
        return self.store_history

    def get_store_history_dataframe(self) -> DataFrame:
        """
        Get the SimPy store of the simulation as DataFrame object.

        :rtype pandas.DataFrame
        :return: the store of the simulation history as pandas DataFrame
        """
        return DataFrame(self.store_history.items)

    def get_sim_time(self) -> int | None:
        """
        The maximum time of the simulation (config value).

        :rtype: int or None
        :return: time of the simulation or None if it isn't specified.
        """
        return self.sim_time

    def get_sim_num_actions(self) -> int:
        """
        Get the number of actions taken by the simulation (config value).

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

    def _simulate_actions(self, events_generated: list):
        """
        Simulate actions using the list of events generated.

        :type events_generated: list
        :param events_generated: events to be simulated.
        """
        from src.sim.status_warehouse.simulate_events.buffer import Buffer
        from src.sim.status_warehouse.simulate_events.send_back_drawer import SendBackDrawer
        from src.sim.status_warehouse.simulate_events.extract_drawer import ExtractDrawer
        from src.sim.status_warehouse.simulate_events.material.insert_material.insert_random_material import InsertRandomMaterial
        from src.sim.status_warehouse.simulate_events.material.remove_material.remove_random_material import RemoveRandomMaterial

        self.store_history = simpy.Store(self.env, capacity=len(events_generated))
        env = self.get_environment()
        warehouse = self.get_warehouse()
        simulation = self
        column_destination = EnumWarehouse.COLUMN
        carousel_destination = EnumWarehouse.CAROUSEL

        # run "control of buffer" process
        yield env.process(Buffer(env, warehouse, simulation).simulate_action())

        # exec all events
        logger.info("Simulation started.")
        for index, event in enumerate(events_generated):
            match event:
                case ActionEnum.SEND_BACK_DRAWER:
                    logger.debug(f"~ Operation #{index} ~")
                    action = SendBackDrawer(env, warehouse, simulation, column_destination)
                    yield env.process(action.simulate_action())
                    logger.debug(f"Time {env.now:5.2f} - FINISH SEND_BACK\n")

                case ActionEnum.EXTRACT_DRAWER:
                    logger.debug(f"~ Operation #{index} ~")
                    action = ExtractDrawer(env, warehouse, simulation, carousel_destination)
                    yield env.process(action.simulate_action())
                    logger.debug(f"Time {env.now:5.2f} - FINISH EXTRACT_DRAWER\n")

                case ActionEnum.INSERT_RANDOM_MATERIAL:
                    logger.debug(f"~ Operation #{index} ~")
                    action = InsertRandomMaterial(env, warehouse, simulation, 2)
                    yield env.process(action.simulate_action())
                    logger.debug(f"Time {env.now:5.2f} - FINISH INS_MAT\n")

                case ActionEnum.REMOVE_RANDOM_MATERIAL:
                    logger.debug(f"~ Operation #{index} ~")
                    action = RemoveRandomMaterial(env, warehouse, simulation, 2)
                    yield env.process(action.simulate_action())
                    logger.debug(f"Time {env.now:5.2f} - FINISH RMV_MAT\n")

        logger.debug(f"Time {env.now:5.2f} - Finish simulation")
        logger.info("Simulation finished.")

    def run_simulation(self):
        """
        Run a new simulation using the same parameters.
        Note: the simulation will create a new sequence of actions.
        """
        balance_wh = 0
        carousel = self.warehouse.get_carousel()
        # create list of event alias
        alias_events = [ActionEnum.SEND_BACK_DRAWER, ActionEnum.EXTRACT_DRAWER,
                        ActionEnum.INSERT_RANDOM_MATERIAL, ActionEnum.REMOVE_RANDOM_MATERIAL]

        # if the deposit or the buffer are full, then update the counter
        balance_wh += carousel.is_deposit_full()
        balance_wh += carousel.is_buffer_full()

        logger.info("Creating the sequence of actions for the simulation.")
        for num_action in range(self.sim_num_actions):
            good_choice = False
            rand_event = ""
            while good_choice is False:
                # select an event
                rand_event = choice(alias_events)
                # check if the choice is correct
                if 1 <= balance_wh <= 2 and (rand_event == ActionEnum.SEND_BACK_DRAWER or
                                             rand_event == ActionEnum.INSERT_RANDOM_MATERIAL or
                                             rand_event == ActionEnum.REMOVE_RANDOM_MATERIAL):
                    good_choice = True
                    if rand_event == ActionEnum.SEND_BACK_DRAWER:
                        balance_wh -= 1
                elif 0 <= balance_wh < 2 and rand_event == ActionEnum.EXTRACT_DRAWER:
                    good_choice = True
                    balance_wh += 1
            self.events_to_simulate.append(rand_event)
        logger.info("Sequence of actions created.")

        # create the simulation
        self.env.process(self._simulate_actions(self.events_to_simulate))

        # run simulation
        self.env.run(until=self.sim_time)

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
        self.warehouse.gen_rand(gen_deposit, gen_buffer, num_gen_drawers, num_gen_materials)

        # reset events to simulate list
        self.events_to_simulate.clear()

        # run a new simulation
        self.run_simulation()

    def go_to_deposit(self):
        """
        Simulation method used to go to deposit.
        """
        warehouse = self.get_warehouse()
        # take current position (y)
        curr_pos = warehouse.get_pos_y_floor()
        # take destination position (y)
        dep_pos = warehouse.get_carousel().get_deposit_entry().get_pos_y()
        yield self.env.timeout(self.vertical_move(curr_pos, dep_pos))
        # set new y position of the floor
        warehouse.set_pos_y_floor(dep_pos)

    def go_to_buffer(self):
        """
        Simulation method used to go to buffer.
        """
        warehouse = self.get_warehouse()
        # take current position (y)
        curr_pos = warehouse.get_pos_y_floor()
        # take destination position (y)
        buf_pos = warehouse.get_carousel().get_buffer_entry().get_pos_y()
        yield self.env.timeout(self.vertical_move(curr_pos, buf_pos))
        # set new y position of the floor
        warehouse.set_pos_y_floor(buf_pos)

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
        warehouse = self.get_warehouse()
        carousel = warehouse.get_carousel()
        y_dep = carousel.get_deposit_entry().get_pos_y()
        y_buf = carousel.get_buffer_entry().get_pos_y()
        # update the y position
        drawer_to_insert.set_best_y(y_dep)

        # calculate time to move (y)
        if load_in_buffer:
            # if the deposit is full but the buffer isn't full
            if not carousel.is_buffer_full():
                # update the y destination
                drawer_to_insert.set_best_y(y_buf)
                logger.debug(f"Time {self.env.now:5.2f} - Deposit is full! Start vertical move to buffer")
                yield self.env.timeout(self.vertical_move(start_pos=y_dep, end_pos=y_buf))
                # set new y position of the floor
                warehouse.set_pos_y_floor(y_buf)
                logger.debug(f"Time {self.env.now:5.2f} - Start to load in the buffer")
            else:
                raise NotImplementedError("Deposit and buffer are full! Collision!")

        # and load inside the carousel
        yield self.env.process(self.load(drawer_to_insert, destination))

    def loading_buffer_and_remove(self):
        """
        Vertical movement of carousel loading from buffer to deposit.
        """
        carousel = self.get_warehouse().get_carousel()
        buffer: DrawerEntry = carousel.get_buffer_entry()

        # calculate loading buffer time
        start_pos = buffer.get_pos_y()
        end_pos = carousel.get_deposit_entry().get_pos_y()
        loading_buffer_time = self.vertical_move(start_pos, end_pos)

        # exec simulate
        yield self.env.timeout(loading_buffer_time)

        # obtain the drawer inside the buffer
        drawer_to_show = buffer.get_drawer()
        # remove from buffer
        carousel.remove_drawer(drawer_to_show)
        # and insert drawer in correct position (outside)
        carousel.add_drawer(drawer_to_show)

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
        warehouse = self.get_warehouse()
        # calculate the distance of index between two points
        index_distance = abs(end_pos - start_pos)
        # calculate effective distance with real measures
        eff_distance = index_distance * warehouse.get_def_space()
        # formula of vertical move
        return (eff_distance / 100) / warehouse.get_speed_per_sec()

    def allocate_best_pos(self, drawer: Drawer):
        """
        Simulation method used to allocate the best position of the drawer in the warehouse.

        :type drawer: Drawer
        :param drawer: drawer to allocate
        """
        warehouse = self.get_warehouse()
        # start position
        start_pos = warehouse.get_pos_y_floor()
        # calculate destination position
        decide_position_res = decide_position(
            columns=warehouse.get_cols_container(),
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
        warehouse.set_pos_y_floor(pos_to_insert)

    def reach_drawer_height(self, drawer: Drawer):
        """
        Simulation method used to reach the height of the drawer in the warehouse.

        :type drawer: Drawer
        :param drawer: drawer to reach
        """
        warehouse = self.get_warehouse()
        # save coordinates inside drawer
        y = drawer.get_first_drawerEntry().get_pos_y()
        x = drawer.get_first_drawerEntry().get_offset_x()
        drawer.set_best_y(y)
        drawer.set_best_offset_x(x)
        # start the move
        vertical_move = self.vertical_move(start_pos=warehouse.get_pos_y_floor(),
                                           end_pos=y)
        yield self.env.timeout(vertical_move)
        # set new y position of the floor
        warehouse.set_pos_y_floor(y)

    def unload(self, drawer: Drawer, rmv_from_cols: bool):
        """
        Simulation method used to unload a drawer from the carousel or from the columns.

        :type drawer: Drawer
        :type rmv_from_cols: bool
        :param drawer: drawer to unload
        :param rmv_from_cols: True to unload the drawer from the columns, otherwise unload from the carousel
        """
        warehouse = self.get_warehouse()
        # take x offset
        offset_x_drawer = drawer.get_first_drawerEntry().get_offset_x()
        # start the move
        yield self.env.timeout(self.horiz_move(offset_x_drawer))
        # update warehouse
        # if drawer hasn't been removed
        if rmv_from_cols:
            for col in warehouse.get_cols_container():
                if col.remove_drawer(drawer):
                    break
        else:
            warehouse.get_carousel().remove_drawer(drawer)
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
        warehouse = self.get_warehouse()
        # take destination coordinates
        dest_x_drawer = drawer.get_best_offset_x()
        dest_y_drawer = drawer.get_best_y()
        # start the move
        yield self.env.timeout(self.horiz_move(dest_x_drawer))
        # update warehouse
        # if destination is carousel, add
        if destination == EnumWarehouse.CAROUSEL:
            warehouse.get_carousel().add_drawer(drawer)
        else:
            # otherwise, check the offset of column
            for col in warehouse.get_cols_container():
                if col.get_offset_x() == dest_x_drawer:
                    col.add_drawer(drawer, dest_y_drawer)
                    break

    def horiz_move(self, offset_x: int) -> float | None:
        """
        Search in the column/carousel where is the drawer.

        :type offset_x: int
        :rtype: float | None
        :param offset_x: offset of the drawer to search
        :return: the time estimated or None if not found
        """
        warehouse = self.get_warehouse()
        # check the carousel
        if warehouse.get_carousel().get_offset_x() == offset_x:
            return (warehouse.get_carousel().get_width() / 100) / warehouse.get_speed_per_sec()
        # otherwise, check every column
        for col in warehouse.get_cols_container():
            if col.get_offset_x() == offset_x:
                return (col.get_width() / 100) / warehouse.get_speed_per_sec()
