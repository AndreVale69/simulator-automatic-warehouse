from simpy import Environment

from src.drawer import Drawer
from src.simulation import Simulation
from src.status_warehouse.Simulate_Events.Move.move import Move
from src.warehouse import Warehouse


class GoToBuffer(Move):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation, drawer: Drawer,
                 destination: str):
        super().__init__(env, warehouse, simulation, destination, drawer)

    # override
    def simulate_action(self):
        print(f"Time {self.env.now:5.2f} - Start go to buffer position")
        yield self.env.process(self.get_warehouse().go_to_buffer())
