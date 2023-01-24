from abc import abstractmethod

from simpy import Environment

from src.simulation import Simulation
from src.status_warehouse.Simulate_Events.action import Action
from src.warehouse import Warehouse, Drawer


class Move(Action):
    # TODO: aggiugno due parametri: drawer, destinazione (enum: colonna, carousel)
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation, drawer: Drawer,
                 destination: str):
        super().__init__(env, warehouse, simulation)
        self.drawer = drawer
        self.destination = destination

    def get_drawer(self):
        return self.drawer

    def get_destination(self):
        return self.destination

    @abstractmethod
    def simulate_action(self):
        pass
