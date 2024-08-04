from logging import getLogger

from simpy import Environment

from automatic_warehouse.simulation.actions.move.move import Move
from automatic_warehouse.simulation.simulation import Simulation
from automatic_warehouse.warehouse import Warehouse

logger = getLogger(__name__)


class GoToBay(Move):
    """
    Movement to go to the bay.

    :type env: Environment
    :type warehouse: Warehouse
    :type simulation: Simulation
    :param env: the simulation environment (SimPy Environment).
    :param warehouse: the warehouse where the action is performed.
    :param simulation: the simulation where the action is performed.
    """
    
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation):
        super().__init__(env, warehouse, simulation)

    # override
    def simulate_action(self, tray=None, destination=None):
        assert tray is None, logger.warning("A go to bay move is the default go to bay move, "
                                              "so the tray parameter is not taken into account.")
        assert destination is None, logger.warning("The default destination parameter is bay, "
                                                   "so the destination parameter is not taken into account.")
        env = self.env
        logger.debug(f"Time {env.now:5.2f} - Start come back to bay position")
        yield env.process(self.simulation.go_to_bay())
