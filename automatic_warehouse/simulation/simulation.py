from __future__ import annotations

from abc import ABC, abstractmethod
from logging import getLogger

from pandas import DataFrame
from simpy import Environment, Store

from automatic_warehouse.warehouse_configuration_singleton import WarehouseConfigurationSingleton

logger = getLogger(__name__)


class Simulation(ABC):
    """ The abstract simulation class. """

    def __init__(self):
        self.env = Environment()

        config = WarehouseConfigurationSingleton.get_instance().get_configuration().simulation
        self.sim_time: int | None = config.time
        self.sim_num_actions: int = config.num_actions
        self.events_to_simulate: list[str] = []
        # create the store
        self.store_history = Store(self.env, self.sim_num_actions)

    def __eq__(self, other):
        return (
            isinstance(other, Simulation) and
            self.env == other.env and
            self.store_history == other.store_history and
            self.sim_time == other.sim_time and
            self.sim_num_actions == other.sim_num_actions and
            self.events_to_simulate == other.events_to_simulate
        )

    def get_environment(self) -> Environment:
        """
        Get the environment (see `SimPy environment <https://simpy.readthedocs.io/en/latest/api_reference/simpy.core.html#simpy.core.Environment>`_) of SimPy.

        :rtype: simpy.Environment
        :return: the environment of SimPy.
        """
        return self.env

    def get_store_history(self) -> Store:
        """
        Get the SimPy store (see `SimPy store <https://simpy.readthedocs.io/en/latest/api_reference/simpy.resources.html#module-simpy.resources.store>`_) of the simulation.
        
        It is used to store the simulation history.

        :rtype: simpy.Store
        :return: the store of the simulation history.
        """
        return self.store_history

    def get_store_history_dataframe(self) -> DataFrame:
        """
        Get the SimPy store of the simulation as DataFrame object.

        :rtype: pandas.DataFrame
        :return: the store of the simulation history as pandas DataFrame
        """
        return DataFrame(self.store_history.items)

    def get_sim_time(self) -> int | None:
        """
        The maximum time of the simulation (config value).

        :rtype: int | None
        :return: time of the simulation or None if it isn't specified.
        """
        return self.sim_time

    def get_sim_num_actions(self) -> int:
        """
        Get the number of actions taken by the simulation (config value).

        :rtype: int
        :return: the number of actions taken by the simulation.
        """
        return self.sim_num_actions

    def get_events_to_simulate(self) -> list[str]:
        """
        Get the list of events to simulate.

        :rtype: list[str]
        :return: a list of events to simulate.
        """
        return self.events_to_simulate

    @abstractmethod
    def run_simulation(self):
        """
        Run a new simulation.

        Note: the simulation will create a new sequence of actions.
        """
        raise NotImplementedError
