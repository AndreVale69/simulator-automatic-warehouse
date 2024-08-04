from logging import getLogger

from simpy import Environment

from automatic_warehouse.simulation.actions.move.move import Move
from automatic_warehouse.simulation.simulation import Simulation
from automatic_warehouse.status_warehouse.container.enum_container import EnumContainer
from automatic_warehouse.warehouse import Warehouse

logger = getLogger(__name__)


class Vertical(Move):
    """
    Vertical movement.

    :type env: Environment
    :type warehouse: Warehouse
    :type simulation: Simulation
    :param env: the simulation environment (SimPy Environment).
    :param warehouse: the warehouse where the action is performed.
    :param simulation: the simulation where the action is performed.
    """

    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation):
        super().__init__(env, warehouse, simulation)

    def simulate_action(self, tray=None, destination=None):
        assert tray is not None, logger.error("The tray cannot be None!")
        assert destination is not None, logger.error("The destination cannot be None!")
        env = self.env
        logger.debug(f"Time {env.now:5.2f} - Start vertical move")
        yield env.process(
            self.simulation.reach_tray_height(tray)
            if destination == EnumContainer.CAROUSEL else
            self.simulation.allocate_best_pos(tray)
        )
