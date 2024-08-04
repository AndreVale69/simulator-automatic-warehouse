from abc import abstractmethod, ABC

from simpy import Environment

from automatic_warehouse.status_warehouse.container.enum_container import EnumContainer
from automatic_warehouse.status_warehouse.tray import Tray
from automatic_warehouse.warehouse import Warehouse


class Action(ABC):
    """
    Superclass for all actions.

    :type env: Environment
    :type warehouse: Warehouse
    :type simulation: Simulation
    :param env: the simulation environment (SimPy Environment).
    :param warehouse: the warehouse where the action is performed.
    :param simulation: the simulation where the action is performed.
    """

    def __init__(self, env: Environment, warehouse: Warehouse, simulation):
        self.env, self.warehouse, self.simulation = env, warehouse, simulation

    def get_env(self) -> Environment:
        """
        Get the simulation environment (see SimPy Environment).

        :rtype: simpy.Environment
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
    def simulate_action(self, tray: Tray=None, destination: EnumContainer=None):
        """
        Method that simulates the action of the instance.

        :type tray: Tray
        :type destination: EnumContainer
        :param tray: A tray used in the simulation, sometimes it is not useful (e.g. GoToBay).
        :param destination: A destination used in the simulation, sometimes it is not useful (e.g. GoToBay).
        """
        raise NotImplementedError
