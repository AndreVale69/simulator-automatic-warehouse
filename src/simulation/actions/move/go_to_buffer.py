from logging import getLogger

from simpy import Environment

from src.simulation.actions.move.move import Move
from src.simulation.simulation import Simulation
from src.warehouse import Warehouse

logger = getLogger(__name__)


class GoToBuffer(Move):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation):
        """
        Movement to go to the buffer.

        :type env: Environment
        :type warehouse: Warehouse
        :type simulation: Simulation
        :param env: the simulation environment (SimPy Environment).
        :param warehouse: the warehouse where the action is performed.
        :param simulation: the simulation where the action is performed.
        """
        super().__init__(env, warehouse, simulation)

    # override
    def simulate_action(self, tray=None, destination=None):
        assert tray is None, logger.warning("A go to buffer move is the default go to buffer move, "
                                              "so the tray parameter is not taken into account.")
        assert destination is None, logger.warning("The default destination parameter is buffer, "
                                                   "so the destination parameter is not taken into account.")
        env = self.env
        logger.debug(f"Time {env.now:5.2f} - Start go to buffer position")
        yield env.process(self.simulation.go_to_buffer())