import logging

from simpy import Environment

from sim.simulation import Simulation
from sim.status_warehouse.simulate_events.move.move import Move
from sim.warehouse import Warehouse, Drawer

logger = logging.getLogger(__name__)


class Unload(Move):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation, drawer: Drawer,
                 destination: str):
        super().__init__(env, warehouse, simulation, destination, drawer)

    def simulate_action(self):
        from sim.status_warehouse.enum_warehouse import EnumWarehouse
        logger.debug(f"Time {self.env.now:5.2f} - Start unloading a drawer")
        yield self.env.process(self.get_warehouse().unload(
            self.get_drawer(),
            rmv_from_cols=True if self.get_destination() == EnumWarehouse.CAROUSEL else False))
