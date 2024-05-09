import logging
from abc import abstractmethod

from simpy import Environment

from src.sim.simulation.actions.action import Action
from src.sim.simulation.simulation import Simulation
from src.sim.warehouse import Warehouse

logger = logging.getLogger(__name__)


class RemoveMaterial(Action):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation, duration: int):
        """
        A superclass of remove material action.

        :type env: Environment
        :type warehouse: Warehouse
        :type simulation: Simulation
        :type duration: int
        :param env: the simulation environment (SimPy Environment).
        :param warehouse: the warehouse where the action is performed.
        :param simulation: the simulation where the action is performed.
        :param duration: the duration of the action in seconds.
        """
        super().__init__(env, warehouse, simulation)
        self.duration = duration

    def get_duration(self) -> int:
        """
        Get the duration of the action in seconds.

        :rtype: int
        :return: the duration of the action in seconds.
        """
        return self.duration

    @abstractmethod
    def simulate_action(self):
        logger.debug(f"Time {self.env.now:5.2f} - Start removing material from a drawer")
        # return the drawer that is outside
        return self.get_warehouse().get_carousel().get_deposit_entry().get_drawer()
