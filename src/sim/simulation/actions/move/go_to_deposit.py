from logging import getLogger

from simpy import Environment

from src.sim.simulation.actions.move.move import Move
from src.sim.simulation.simulation import Simulation
from src.sim.warehouse import Warehouse

logger = getLogger(__name__)


class GoToDeposit(Move):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation):
        """
        Movement to go to the deposit.

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
        assert tray is None, logger.warning("A go to deposit move is the default go to deposit move, "
                                              "so the tray parameter is not taken into account.")
        assert destination is None, logger.warning("The default destination parameter is bay, "
                                                   "so the destination parameter is not taken into account.")
        env = self.env
        logger.debug(f"Time {env.now:5.2f} - Start come back to deposit position")
        yield env.process(self.simulation.go_to_deposit())
