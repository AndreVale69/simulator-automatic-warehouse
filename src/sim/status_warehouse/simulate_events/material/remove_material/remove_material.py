import logging

from abc import abstractmethod

from simpy import Environment

from sim.simulation import Simulation
from sim.status_warehouse.simulate_events.action import Action
from sim.warehouse import Warehouse

logger = logging.getLogger(__name__)


class RemoveMaterial(Action):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation, duration: int):
        super().__init__(env, warehouse, simulation)
        self.duration = duration

    def get_duration(self) -> int:
        return self.duration

    @abstractmethod
    def simulate_action(self):
        logger.debug(f"Time {self.env.now:5.2f} - Start removing material from a drawer")
        # return the drawer that is outside
        return self.get_warehouse().get_carousel().get_deposit_entry().get_drawer()
