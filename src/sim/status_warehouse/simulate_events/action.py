from abc import abstractmethod

from simpy import Environment

from src.sim.warehouse import Warehouse


class Action:
    def __init__(self, env: Environment, warehouse: Warehouse, simulation):
        """
        Superclass for all actions.

        :type env: Environment
        :type warehouse: Warehouse
        :type simulation: Simulation
        :param env: the simulation environment (SimPy Environment).
        :param warehouse: the warehouse where the action is performed.
        :param simulation: the simulation where the action is performed.
        """
        self.env = env
        self.warehouse = warehouse
        self.simulation = simulation

    def get_env(self) -> Environment:
        """
        Get the simulation environment (see SimPy Environment).

        :rtype: Environment
        :return: the simulation environment.
        """
        return self.env

    def get_warehouse(self):
        """
        Get the warehouse where the action is performed.

        :rtype: Warehouse
        :return: the warehouse where the action is performed.
        """
        return self.warehouse

    def get_simulation(self):
        """
        Get the simulation where the action is performed.

        :rtype: Simulation
        :return: the simulation where the action is performed.
        """
        return self.simulation

    @abstractmethod
    def simulate_action(self):
        """
        Abstract method that simulates the action of the instance.
        """
        pass
