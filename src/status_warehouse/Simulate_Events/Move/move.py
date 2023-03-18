from abc import abstractmethod

from simpy import Environment

from src.simulation import Simulation
from src.status_warehouse.Simulate_Events.action import Action
from src.warehouse import Warehouse, Drawer


class Move(Action):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation, destination, drawer=None):
        super().__init__(env, warehouse, simulation)
        self.drawer = drawer
        self.destination = destination

    def set_drawer(self, drawer):
        self.drawer = drawer

    def get_drawer(self):
        return self.drawer

    def get_destination(self):
        return self.destination

    @abstractmethod
    def simulate_action(self):
        from src.status_warehouse.Simulate_Events.Move.go_to_deposit import GoToDeposit

        # come back to the deposit iff there is a drawer
        if self.get_warehouse().get_carousel().is_deposit_full():
            yield self.env.process(GoToDeposit(self.get_env(), self.get_warehouse(), self.get_simulation(),
                                               self.get_drawer(), self.get_destination()).simulate_action())
