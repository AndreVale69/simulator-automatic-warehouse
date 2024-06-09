from logging import getLogger

from simpy import Environment

from src.simulation.actions.move.move import Move
from src.simulation.simulation import Simulation
from src.status_warehouse.enum_warehouse import EnumWarehouse
from src.warehouse import Warehouse

logger = getLogger(__name__)


class Unload(Move):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation):
        """
        Horizontal movement from the center of the column to the center of the lift.

        :type env: Environment
        :type warehouse: Warehouse
        :type simulation: Simulation
        :param env: the simulation environment (SimPy Environment).
        :param warehouse: the warehouse where the action is performed.
        :param simulation: the simulation where the action is performed.
        """
        super().__init__(env, warehouse, simulation)

    def simulate_action(self, tray=None, destination=None):
        assert tray is not None, logger.error("The tray cannot be None!")
        assert destination is not None, logger.error("The destination cannot be None!")
        env = self.env
        logger.debug(f"Time {env.now:5.2f} - Start unloading a tray")
        yield env.process(self.simulation.unload(tray, destination == EnumWarehouse.CAROUSEL))