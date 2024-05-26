from logging import getLogger

from simpy import Environment

from src.sim.simulation.actions.move.move import Move
from src.sim.simulation.simulation import Simulation
from src.sim.warehouse import Warehouse

logger = getLogger(__name__)


class Load(Move):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation):
        """
        Horizontal movement from the center of the lift to the center of the column.

        :type env: Environment
        :type warehouse: Warehouse
        :type simulation: Simulation
        :param env: the simulation environment (SimPy Environment).
        :param warehouse: the warehouse where the action is performed.
        :param simulation: the simulation where the action is performed.
        """
        super().__init__(env, warehouse, simulation)

    def simulate_action(self, drawer=None, destination=None):
        assert drawer is not None, logger.error("The drawer cannot be None!")
        assert destination is not None, logger.error("The destination cannot be None!")
        env = self.env
        logger.debug(f"Time {env.now:5.2f} - Start loading inside the warehouse")
        yield env.process(self.simulation.load(drawer, destination))
