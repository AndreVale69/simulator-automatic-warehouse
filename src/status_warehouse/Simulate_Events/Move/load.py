from simpy import Environment

from src.simulation import Simulation
from src.status_warehouse.Simulate_Events.Move.move import Move
from src.warehouse import Warehouse, Drawer


class Load(Move):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation, drawer: Drawer,
                 destination: str):
        super().__init__(env, warehouse, simulation, destination, drawer)

    def simulate_action(self):
        print(f"Time {self.env.now:5.2f} - Start loading inside the warehouse")
        yield self.env.process(self.get_warehouse().load(self.get_drawer(), self.get_destination()))
