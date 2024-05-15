from datetime import datetime, timedelta
from simpy import Environment

from src.sim.simulation.actions.action_enum import ActionEnum
from src.sim.simulation.actions.buffer import Buffer
from src.sim.simulation.actions.move.load import Load
from src.sim.simulation.actions.move.move import Move
from src.sim.simulation.actions.move.unload import Unload
from src.sim.simulation.actions.move.vertical import Vertical
from src.sim.simulation.simulation import Simulation
from src.sim.warehouse import Warehouse


class SendBackDrawer(Move):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation, destination):
        """
        The send-back of a drawer (SendBackDrawer action)
        is the movement of a drawer from the bay to one of the columns.

        :type env: Environment
        :type warehouse: Warehouse
        :type simulation: Simulation
        :param env: the simulation environment (SimPy Environment).
        :param warehouse: the warehouse where the action is performed.
        :param simulation: the simulation where the action is performed.
        """
        super().__init__(env, warehouse, simulation, destination)

    def simulate_action(self):
        start_time = datetime.now() + timedelta(seconds=self.env.now)

        with self.simulation.get_res_deposit().request() as req:
            # try to take the drawer inside the deposit
            yield req
            # set the drawer
            self.set_drawer(self.warehouse.get_carousel().get_deposit_entry().get_drawer())
            # unloading drawer
            yield self.env.process(
                Unload(self.env, self.warehouse, self.simulation, self.drawer,
                       self.destination).simulate_action())

        # exec Buffer process
        wait_buff = self.env.process(Buffer(self.env, self.warehouse, self.simulation).simulate_action())

        # move the floor
        yield self.env.process(Vertical(self.env, self.warehouse, self.simulation, self.drawer,
                                        self.destination).simulate_action())
        # loading drawer
        yield self.env.process(Load(self.env, self.warehouse, self.simulation, self.drawer,
                                    self.destination).simulate_action())

        # check GoToDeposit move
        yield self.env.process(super().simulate_action())
        # wait the buffer process
        yield wait_buff

        end_time = datetime.now() + timedelta(seconds=self.env.now)

        yield self.simulation.get_store_history().put({
            'Type of Action': ActionEnum.SEND_BACK_DRAWER.value,
            'Start'         : start_time,
            'Finish'        : end_time
        })
