from simpy import Environment

from src.simulation import Simulation
from src.status_warehouse.Simulate_Events.Move.load import Load
from src.status_warehouse.Simulate_Events.Move.move import Move
from src.status_warehouse.Simulate_Events.Move.unload import Unload
from src.status_warehouse.Simulate_Events.Move.vertical import Vertical
from src.warehouse import Warehouse, Drawer


class SendBackDrawer(Move):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation, drawer: Drawer,
                 destination: str):
        super().__init__(env, warehouse, simulation, drawer, destination)

    def simulate_action(self):
        # TODO: l'argomento è già nella classe warehouse
        # TODO: le righe vanno direttamente in warehouse
        # TODO: si prende il drawer come parametro
        # unloading drawer
        yield self.env.process(Unload(self.get_env(), self.get_warehouse(), self.get_simulation(), self.get_drawer(),
                                      self.get_destination()).simulate_action())
        # move the floor
        yield self.env.process(Vertical(self.get_env(), self.get_warehouse(), self.get_simulation(), self.get_drawer(),
                                        self.get_destination()).simulate_action())
        # loading drawer
        yield self.env.process(Load(self.get_env(), self.get_warehouse(), self.get_simulation(), self.get_drawer(),
                                    self.get_destination()).simulate_action())
