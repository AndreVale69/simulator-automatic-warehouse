import logging

from simpy import Environment

from sim.status_warehouse.enum_warehouse import EnumWarehouse
from src.sim.simulation import Simulation
from src.sim.status_warehouse.simulate_events.move.move import Move
from src.sim.warehouse import Warehouse, Drawer

logger = logging.getLogger(__name__)


class Unload(Move):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation, drawer: Drawer,
                 destination: EnumWarehouse):
        """
        Horizontal movement from the center of the column to the center of the lift.

        :type env: Environment
        :type warehouse: Warehouse
        :type simulation: Simulation
        :type destination: EnumWarehouse
        :type drawer: Drawer
        :param env: the simulation environment (SimPy Environment).
        :param warehouse: the warehouse where the action is performed.
        :param simulation: the simulation where the action is performed.
        :param destination: the destination of the move.
        :param drawer: the drawer used in the movement.
        """
        super().__init__(env, warehouse, simulation, destination, drawer)

    def simulate_action(self):
        from src.sim.status_warehouse.enum_warehouse import EnumWarehouse
        logger.debug(f"Time {self.env.now:5.2f} - Start unloading a drawer")
        yield self.env.process(self.get_warehouse().unload(
            self.get_drawer(),
            rmv_from_cols=True if self.get_destination() == EnumWarehouse.CAROUSEL else False))
