import logging

from simpy import Environment

from src.sim.simulation import Simulation
from src.sim.status_warehouse.simulate_events.move.move import Move
from src.sim.warehouse import Warehouse, Drawer
from src.sim.status_warehouse.enum_warehouse import EnumWarehouse

logger = logging.getLogger(__name__)


class Vertical(Move):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation, drawer: Drawer,
                 destination: EnumWarehouse):
        super().__init__(env, warehouse, simulation, destination, drawer)

    def simulate_action(self):
        logger.debug(f"Time {self.env.now:5.2f} - Start vertical move")
        if self.get_destination() == EnumWarehouse.CAROUSEL:
            yield self.env.process(self.get_warehouse().reach_drawer_height(self.get_drawer()))
        else:
            yield self.env.process(self.get_warehouse().allocate_best_pos(self.get_drawer()))
