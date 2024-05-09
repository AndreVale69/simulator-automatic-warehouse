from abc import abstractmethod

from simpy import Environment

from src.sim.simulation.actions.action import Action
from src.sim.simulation.simulation import Simulation
from src.sim.status_warehouse.enum_warehouse import EnumWarehouse
from src.sim.warehouse import Warehouse  # , Drawer


class Move(Action):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation, destination: EnumWarehouse,
                 drawer=None):
        """
        Superclass for all simple moves.

        :type env: Environment
        :type warehouse: Warehouse
        :type simulation: Simulation
        :type destination: EnumWarehouse
        :type drawer: Drawer
        :param env: the simulation environment (SimPy Environment).
        :param warehouse: the warehouse where the action is performed.
        :param simulation: the simulation where the action is performed.
        :param destination: the destination of the move.
        :param drawer: the drawer used in the movement.
        """
        super().__init__(env, warehouse, simulation)
        self.drawer = drawer
        self.destination = destination

    def set_drawer(self, drawer):
        """
        Sets the drawer used in the movement.

        :type drawer: Drawer
        :param drawer: drawer used in the movement.
        """
        self.drawer = drawer

    def get_drawer(self):
        """
        Get the drawer used in the movement.

        :rtype: Drawer
        :return: the drawer used in the movement.
        """
        return self.drawer

    def get_destination(self) -> EnumWarehouse:
        """
        Get the destination of the move.

        :rtype: EnumWarehouse
        :return: the destination of the move.
        """
        return self.destination

    @abstractmethod
    def simulate_action(self):
        from src.sim.simulation.actions.move.go_to_deposit import GoToDeposit

        # come back to the deposit iff there is a drawer
        if self.get_warehouse().get_carousel().is_deposit_full():
            yield self.env.process(GoToDeposit(self.get_env(), self.get_warehouse(), self.get_simulation(),
                                               self.get_drawer(), self.get_destination()).simulate_action())
