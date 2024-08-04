from copy import deepcopy
from datetime import datetime
from logging import getLogger
from random import choice

from simpy import Resource, Store

from automatic_warehouse.simulation.actions.action_enum import ActionEnum
from automatic_warehouse.simulation.actions.buffer import Buffer
from automatic_warehouse.simulation.actions.extract_tray import ExtractTray
from automatic_warehouse.simulation.actions.material.insert_material.insert_random_material import InsertRandomMaterial
from automatic_warehouse.simulation.actions.material.remove_material.remove_random_material import RemoveRandomMaterial
from automatic_warehouse.simulation.actions.send_back_tray import SendBackTray
from automatic_warehouse.simulation.simulation import Simulation
from automatic_warehouse.status_warehouse.entry.tray_entry import TrayEntry
from automatic_warehouse.status_warehouse.container.enum_container import EnumContainer
from automatic_warehouse.status_warehouse.tray import Tray
from automatic_warehouse.utils.decide_position_algorithm.algorithm import decide_position
from automatic_warehouse.utils.decide_position_algorithm.enum_algorithm import Algorithm
from automatic_warehouse.warehouse import Warehouse

logger = getLogger(__name__)



class WarehouseSimulation(Simulation):
    """
    The warehouse simulation class.

    :type warehouse: Warehouse
    :param warehouse: the warehouse used to perform the simulation.
    """

    def __init__(self, warehouse: Warehouse):
        super().__init__()
        # start the move process everytime an instance is created
        logger.info("Create a copy of the Warehouse")
        self.warehouse = deepcopy(warehouse)

        # allocation of carousel resources
        self.res_buffer = Resource(self.env, 1)
        self.res_bay = Resource(self.env, 1)

    def __eq__(self, other):
        return (
            isinstance(other, WarehouseSimulation) and
            Simulation.__eq__(self, other) and
            self.warehouse == other.warehouse and
            self.res_buffer == other.res_buffer and
            self.res_bay == other.res_bay
        )

    def get_warehouse(self) -> Warehouse:
        """
        Get the Warehouse used to perform the simulation.

        :rtype: Warehouse
        :return: the Warehouse used to perform the simulation.
        """
        return self.warehouse

    def get_res_buffer(self) -> Resource:
        """
        Get the resource of the buffer.
        It can be thought of as a resource lock (see `SimPy resource <https://simpy.readthedocs.io/en/latest/api_reference/simpy.resources.html#module-simpy.resources.resource>`_).

        :rtype: simpy.Resource
        :return: the resource of the buffer.
        """
        return self.res_buffer

    def get_res_bay(self) -> Resource:
        """
        Get the resource of the bay.
        It can be thought of as a resource lock (see `SimPy resource <https://simpy.readthedocs.io/en/latest/api_reference/simpy.resources.html#module-simpy.resources.resource>`_).

        :rtype: simpy.Resource
        :return: the resource of the bay.
        """
        return self.res_bay

    def _simulate_actions(self):
        """ Simulate actions. """
        # TODO if the actions are too many, divide them into groups (batches py3.12)
        carousel = self.warehouse.get_carousel()
        # if the bay or the buffer are full, then update the counter
        balance_wh = carousel.is_bay_full() + carousel.is_buffer_full()
        # get variables to reduce memory accesses
        env = self.env
        warehouse = self.warehouse
        send_back_tray = SendBackTray(env, warehouse, self)
        extract_tray = ExtractTray(env, warehouse, self)
        insert_random_material = InsertRandomMaterial(env, warehouse, self, 2)
        remove_random_material = RemoveRandomMaterial(env, warehouse, self, 2)
        column_val = EnumContainer.COLUMN
        carousel_val = EnumContainer.CAROUSEL
        extract_tray_val = ActionEnum.EXTRACT_TRAY.value
        send_back_tray_val = ActionEnum.SEND_BACK_TRAY.value
        insert_random_material_val = ActionEnum.INSERT_RANDOM_MATERIAL.value
        remove_random_material_val = ActionEnum.REMOVE_RANDOM_MATERIAL.value
        # prepare domains
        case_1 = [send_back_tray_val, extract_tray_val,
                  insert_random_material_val, remove_random_material_val]
        case_2 = [send_back_tray_val, insert_random_material_val, remove_random_material_val]
        # run "control of buffer" process
        yield env.process(Buffer(env, warehouse, self).simulate_action())
        start = datetime.now()
        logger.info("Simulation started.")
        for num_action in range(self.sim_num_actions):
            logger.debug(f"~ Operation #{num_action} ~")
            # before the random selection, choose the domain to take into account the balance
            rand_event = extract_tray_val
            if balance_wh == 1:
                rand_event = choice(case_1)
            elif balance_wh == 2:
                rand_event = choice(case_2)
            # process the event
            if rand_event == ActionEnum.EXTRACT_TRAY.value:
                balance_wh += 1
                yield env.process(extract_tray.simulate_action(destination=carousel_val))
            elif rand_event == ActionEnum.SEND_BACK_TRAY.value:
                balance_wh -= 1
                yield env.process(send_back_tray.simulate_action(destination=column_val))
            elif rand_event == ActionEnum.INSERT_RANDOM_MATERIAL.value:
                yield env.process(insert_random_material.simulate_action())
            elif rand_event == ActionEnum.REMOVE_RANDOM_MATERIAL.value:
                yield env.process(remove_random_material.simulate_action())

            logger.debug(f"Time {env.now:5.2f} - FINISH {rand_event}\n")

        logger.debug(f"Time {env.now:5.2f} - Finish simulation")
        end = datetime.now()
        logger.info(f"Simulation finished. Total time: {end-start}")

    def run_simulation(self):
        """ Run a simulation. """
        # create the store
        self.store_history = Store(self.env, self.sim_num_actions)

        # create the simulation
        self.env.process(self._simulate_actions())

        # run simulation
        self.env.run(until=self.sim_time)

    def new_simulation(
            self, 
            num_actions: int, 
            num_gen_trays: int, 
            num_gen_materials: int,
            gen_bay: bool, 
            gen_buffer: bool, 
            time: int=None
        ):
        """
        Run a new simulation using custom parameters.

        :type num_actions: int
        :type num_gen_trays: int
        :type num_gen_materials: int
        :type gen_bay: bool
        :type gen_buffer: bool
        :type time: int or None
        :param num_actions: number of actions to simulate.
        :param num_gen_trays: number of trays to generate in the warehouse.
        :param num_gen_materials: number of materials to generate in the warehouse.
        :param gen_bay: ``True`` to generate a tray in the bay, ``False`` otherwise.
        :param gen_buffer: ``True`` to generate a tray in the buffer, ``False`` otherwise.
        :param time: the maximum time of the simulation, otherwise ``None`` to remove the limit.
        """
        # setting new simulation settings:
        self.sim_time = time
        self.sim_num_actions = num_actions

        # random gen
        self.warehouse.gen_rand(gen_bay, gen_buffer, num_gen_trays, num_gen_materials)

        # reset events to simulate list
        self.events_to_simulate.clear()

        # run a new simulation
        self.run_simulation()

    def go_to_bay(self):
        """
        Simulation method used to go to bay.
        """
        # take current position (y)
        curr_pos = (warehouse := self.warehouse).get_pos_y_floor()
        # take destination position (y)
        bay_pos = warehouse.get_carousel().get_bay_entry().get_pos_y()
        yield self.env.timeout(self.vertical_move(curr_pos, bay_pos))
        # set new y position of the floor
        warehouse.set_pos_y_floor(bay_pos)

    def go_to_buffer(self):
        """
        Simulation method used to go to buffer.
        """
        # take current position (y)
        curr_pos = (warehouse := self.warehouse).get_pos_y_floor()
        # take destination position (y)
        buf_pos = warehouse.get_carousel().get_buffer_entry().get_pos_y()
        yield self.env.timeout(self.vertical_move(curr_pos, buf_pos))
        # set new y position of the floor
        warehouse.set_pos_y_floor(buf_pos)

    def load_in_carousel(self, tray_to_insert: Tray, destination: EnumContainer, load_in_buffer: bool):
        """
        Simulation method used to load the carousel into the warehouse.

        :type tray_to_insert: Tray
        :type destination: EnumContainer
        :type load_in_buffer: bool
        :param tray_to_insert: tray that will be inserted into the warehouse.
        :param destination: destination of the tray.
        :param load_in_buffer: ``True`` to load the carousel into the buffer, otherwise into the bay.
        """
        env = self.env
        carousel = (warehouse := self.warehouse).get_carousel()
        y_dep = carousel.get_bay_entry().get_pos_y()
        y_buf = carousel.get_buffer_entry().get_pos_y()
        # update the y position
        tray_to_insert.set_best_y(y_dep)

        # calculate time to move (y)
        if load_in_buffer:
            # if the bay is full but the buffer isn't full
            if carousel.is_buffer_full():
                raise NotImplementedError("Bay and buffer are full! Collision!")
            # update the y destination
            tray_to_insert.set_best_y(y_buf)
            logger.debug(f"Time {env.now:5.2f} - Bay is full! Start vertical move to buffer")
            yield env.timeout(self.vertical_move(start_pos=y_dep, end_pos=y_buf))
            # set new y position of the floor
            warehouse.set_pos_y_floor(y_buf)
            logger.debug(f"Time {env.now:5.2f} - Start to load in the buffer")

        # and load inside the carousel
        yield env.process(self.load(tray_to_insert, destination))

    def loading_buffer_and_remove(self):
        """
        Vertical movement of carousel loading from buffer to bay.
        """
        buffer: TrayEntry = (carousel := self.warehouse.get_carousel()).get_buffer_entry()

        # calculate loading buffer time
        loading_buffer_time = self.vertical_move(buffer.get_pos_y(), carousel.get_bay_entry().get_pos_y())

        # exec simulate
        yield self.env.timeout(loading_buffer_time)

        # obtain the tray inside the buffer
        tray_to_show = buffer.get_tray()
        # remove from buffer
        carousel.remove_tray(tray_to_show)
        # and insert tray in correct position (outside)
        carousel.add_tray(tray_to_show)

    def vertical_move(self, start_pos: int, end_pos: int) -> float:
        """
        A simple vertical movement of the floor or the tray inside the carousel (buffer to bay).

        :type start_pos: int
        :type end_pos: int
        :rtype: float
        :param start_pos: starting position.
        :param end_pos: ending position.
        :return: distance travelled divided by speed per second.
        """
        # calculate the distance of index between two points
        index_distance = abs(end_pos - start_pos)
        # calculate effective distance with real measures
        eff_distance = index_distance * (warehouse := self.get_warehouse()).get_def_space()
        # formula of vertical move
        return (eff_distance / 100) / warehouse.get_speed_per_sec()

    def allocate_best_pos(self, tray: Tray):
        """
        Simulation method used to allocate the best position of the tray in the warehouse.

        :type tray: Tray
        :param tray: tray to allocate.
        """
        # start position
        start_pos = (warehouse := self.warehouse).get_pos_y_floor()
        # calculate destination position
        decide_position_res = decide_position(
            columns=warehouse.get_cols_container(),
            space_req=tray.get_num_space_occupied(),
            algorithm=Algorithm.HIGH_POSITION
        )
        pos_to_insert = decide_position_res.index
        # temporarily save the coordinates
        tray.set_best_y(pos_to_insert)
        tray.set_best_offset_x(decide_position_res.column.get_offset_x())
        # start the move
        vertical_move = self.vertical_move(start_pos, pos_to_insert)
        yield self.env.timeout(vertical_move)
        # set new y position of the floor
        warehouse.set_pos_y_floor(pos_to_insert)

    def reach_tray_height(self, tray: Tray):
        """
        Simulation method used to reach the height of the tray in the warehouse.

        :type tray: Tray
        :param tray: tray to reach.
        """
        # save coordinates inside tray
        y = tray.get_first_tray_entry().get_pos_y()
        x = tray.get_first_tray_entry().get_offset_x()
        tray.set_best_y(y)
        tray.set_best_offset_x(x)
        # start the move
        vertical_move = self.vertical_move(start_pos=(warehouse := self.get_warehouse()).get_pos_y_floor(),
                                           end_pos=y)
        yield self.env.timeout(vertical_move)
        # set new y position of the floor
        warehouse.set_pos_y_floor(y)

    def unload(self, tray: Tray, rmv_from_cols: bool):
        """
        Simulation method used to unload a tray from the carousel or from the columns.

        :type tray: Tray
        :type rmv_from_cols: bool
        :param tray: tray to unload.
        :param rmv_from_cols: True to unload the tray from the columns, otherwise unload from the carousel.
        """
        warehouse = self.warehouse
        # take x offset
        offset_x_tray = tray.get_first_tray_entry().get_offset_x()
        # start the move
        yield self.env.timeout(self.horiz_move(offset_x_tray))
        # update warehouse
        # if tray hasn't been removed
        if rmv_from_cols:
            for col in warehouse.get_cols_container():
                if col.remove_tray(tray):
                    break
        else:
            warehouse.get_carousel().remove_tray(tray)

    def load(self, tray: Tray, destination: EnumContainer):
        """
        Simulation method used to load the tray into the warehouse.

        :type tray: Tray
        :type destination: EnumContainer
        :param tray: tray to load.
        :param destination: destination of the tray.
        :raises ValueError: if the offset of the tray is not equal to any column in the warehouse.
        """
        warehouse = self.warehouse
        # take destination coordinates
        dest_x_tray = tray.get_best_offset_x()
        dest_y_tray = tray.get_best_y()
        # start the move
        yield self.env.timeout(self.horiz_move(dest_x_tray))
        # update warehouse
        # if destination is carousel, add
        if destination == EnumContainer.CAROUSEL:
            return warehouse.get_carousel().add_tray(tray)
        # otherwise, check the offset of column
        for col in warehouse.get_cols_container():
            if col.get_offset_x() == dest_x_tray:
                return col.add_tray(tray, dest_y_tray)
        raise ValueError(f"Offset x not found: {dest_x_tray}")

    def horiz_move(self, offset_x: int) -> float:
        """
        Search in the column/carousel where is the tray.

        :type offset_x: int
        :rtype: float | None
        :param offset_x: offset of the tray to search.
        :return: the time estimated or ``None`` if not found.
        :raises ValueError: if the offset is not valid.
        """
        # check the carousel
        if (warehouse := self.warehouse).get_carousel().get_offset_x() == offset_x:
            return (warehouse.get_carousel().get_width() / 100) / warehouse.get_speed_per_sec()
        # otherwise, check every column
        for col in warehouse.get_cols_container():
            if col.get_offset_x() == offset_x:
                return (col.get_width() / 100) / warehouse.get_speed_per_sec()
        raise ValueError(f"Offset x not found: {offset_x}")
