from simpy import Environment

from src.simulation import Simulation
from src.status_warehouse.Simulate_Events.Move.move import Move
from src.warehouse import Warehouse, Drawer


class Vertical(Move):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation, drawer: Drawer,
                 destination: str):
        super().__init__(env, warehouse, simulation, drawer, destination)

    def simulate_action(self):
        print(f"Time {self.env.now:5.2f} - Start vertical move")
        yield self.env.process(self.get_warehouse().allocate_best_pos(self.get_warehouse().get_drawer_of_support()))
        # yield self.env.process(self.get_warehouse().allocate_best_pos(self.get_drawer()))
