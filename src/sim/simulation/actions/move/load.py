from logging import getLogger
from simpy import Environment

from src.sim.simulation.actions.move.move import Move
from src.sim.simulation.simulation import Simulation
from src.sim.status_warehouse.enum_warehouse import EnumWarehouse
from src.sim.warehouse import Warehouse, Drawer

logger = getLogger(__name__)


class Load(Move):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation, drawer: Drawer,
                 destination: EnumWarehouse):
        """
        Horizontal movement from the center of the lift to the center of the column.

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

    def simulate_action(self):
        logger.debug(f"Time {self.env.now:5.2f} - Start loading inside the warehouse")
        yield self.env.process(self.simulation.load(self.drawer, self.destination))
