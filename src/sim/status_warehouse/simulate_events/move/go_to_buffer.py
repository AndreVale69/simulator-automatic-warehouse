import logging

from simpy import Environment

from sim.status_warehouse.enum_warehouse import EnumWarehouse
from src.sim.drawer import Drawer
from src.sim.simulation import Simulation
from src.sim.status_warehouse.simulate_events.move.move import Move
from src.sim.warehouse import Warehouse

logger = logging.getLogger(__name__)


class GoToBuffer(Move):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation, drawer: Drawer,
                 destination: EnumWarehouse):
        """
        Movement to go to the buffer.

        :type env: Environment
        :type warehouse: Warehouse
        :type simulation: Simulation
        :type destination: EnumWarehouse
        :type drawer: Drawer
        :param env: the simulation environment (SimPy Environment).
        :param warehouse: the warehouse where the action is performed.
        :param simulation: the simulation where the action is performed.
        :param destination: the destination of the move.
        :param drawer: the drawer used in the movement.
        """
        super().__init__(env, warehouse, simulation, destination, drawer)

    # override
    def simulate_action(self):
        logger.debug(f"Time {self.env.now:5.2f} - Start go to buffer position")
        yield self.env.process(self.get_warehouse().go_to_buffer())
