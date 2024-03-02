import logging

from simpy import Environment

from src.sim.simulation import Simulation
from src.sim.status_warehouse.simulate_events.move.move import Move
from src.sim.warehouse import Warehouse, Drawer

logger = logging.getLogger(__name__)


class Load(Move):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation, drawer: Drawer,
                 destination: str):
        super().__init__(env, warehouse, simulation, destination, drawer)

    def simulate_action(self):
        logger.debug(f"Time {self.env.now:5.2f} - Start loading inside the warehouse")
        yield self.env.process(self.get_warehouse().load(self.get_drawer(), self.get_destination()))
