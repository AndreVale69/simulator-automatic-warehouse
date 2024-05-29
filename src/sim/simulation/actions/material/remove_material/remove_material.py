from abc import abstractmethod

from simpy import Environment

from src.sim.simulation.actions.action import Action
from src.sim.simulation.simulation import Simulation
from src.sim.warehouse import Warehouse


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
    def simulate_action(self, drawer=None, destination=None):
        raise NotImplementedError
