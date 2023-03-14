from simpy import Environment

from src.simulation import Simulation
from src.status_warehouse.Simulate_Events.Move.move import Move
from src.warehouse import Warehouse, Drawer


class Unload(Move):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation, drawer: Drawer,
                 destination: str):
        super().__init__(env, warehouse, simulation, drawer, destination)

    def simulate_action(self):
        print(f"Time {self.env.now:5.2f} - Start unloading a drawer")
        yield self.env.process(self.get_warehouse().unload(self.get_drawer()))