import logging

from simpy import Environment

from sim.drawer import Drawer
# from src.drawer import Drawer
from sim.simulation import Simulation
from sim.status_warehouse.simulate_events.move.move import Move
from sim.warehouse import Warehouse

logger = logging.getLogger(__name__)


class GoToDeposit(Move):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation, drawer: Drawer,
                 destination: str):
        super().__init__(env, warehouse, simulation, destination, drawer)

    # override
    def simulate_action(self):
        logger.debug(f"Time {self.env.now:5.2f} - Start come back to deposit position")
        yield self.env.process(self.get_warehouse().go_to_deposit())
