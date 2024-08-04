from abc import abstractmethod

from simpy import Environment

from automatic_warehouse.simulation.actions.action import Action
from automatic_warehouse.simulation.simulation import Simulation
from automatic_warehouse.warehouse import Warehouse


class RemoveMaterial(Action):
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
    
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation, duration: int):
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
    def simulate_action(self, tray=None, destination=None):
        raise NotImplementedError
