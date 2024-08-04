from simpy import Environment

from automatic_warehouse.simulation.actions.action import Action
from automatic_warehouse.simulation.actions.buffer import Buffer
from automatic_warehouse.simulation.simulation import Simulation
from automatic_warehouse.warehouse import Warehouse


class Move(Action):
    """
    Superclass for all simple moves.

    :type env: Environment
    :type warehouse: Warehouse
    :type simulation: Simulation
    :param env: the simulation environment (SimPy Environment).
    :param warehouse: the warehouse where the action is performed.
    :param simulation: the simulation where the action is performed.
    """

    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation):
        super().__init__(env, warehouse, simulation)
        self.buffer = Buffer(env, warehouse, simulation)

    def get_buffer(self) -> Buffer:
        """
        Get the buffer pointer, useful during simulation.

        :rtype Buffer
        :return: the buffer pointer.
        """
        return self.buffer

    def simulate_action(self, tray=None, destination=None):
        raise NotImplementedError
