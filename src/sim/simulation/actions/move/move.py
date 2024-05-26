from simpy import Environment

from src.sim.simulation.actions.action import Action
from src.sim.simulation.actions.buffer import Buffer
from src.sim.simulation.simulation import Simulation
from src.sim.warehouse import Warehouse


class Move(Action):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation):
        """
        Superclass for all simple moves.

        :type env: Environment
        :type warehouse: Warehouse
        :type simulation: Simulation
        :param env: the simulation environment (SimPy Environment).
        :param warehouse: the warehouse where the action is performed.
        :param simulation: the simulation where the action is performed.
        """
        super().__init__(env, warehouse, simulation)
        self.buffer = Buffer(env, warehouse, simulation)

    def get_buffer(self) -> Buffer:
        """
        Get the buffer pointer, useful during simulation.

        :rtype Buffer
        :return: the buffer pointer.
        """
        return self.buffer

    def simulate_action(self, drawer=None, destination=None):
        pass
