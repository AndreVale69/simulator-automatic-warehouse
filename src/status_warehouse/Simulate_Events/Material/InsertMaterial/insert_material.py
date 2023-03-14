from abc import abstractmethod

from simpy import Environment

from src.simulation import Simulation
from src.status_warehouse.Simulate_Events.action import Action
from src.warehouse import Warehouse


class InsertMaterial(Action):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation, duration: int):
        super().__init__(env, warehouse, simulation)
        self.duration = duration

    def get_duration(self) -> int:
        return self.duration

    @abstractmethod
    def simulate_action(self):
        print(f"Time {self.env.now:5.2f} - Start putting materials inside a drawer")
        # return the drawer that is outside
        return self.get_warehouse().get_carousel().get_deposit_entry().get_drawer()
