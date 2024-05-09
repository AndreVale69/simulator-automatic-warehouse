import logging

from simpy import Environment

from src.sim.simulation.actions.action import Action
from src.sim.simulation.simulation import Simulation
from src.sim.warehouse import Warehouse

logger = logging.getLogger(__name__)


class Buffer(Action):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation):
        """
        The buffer action is the movement from the buffer entry to the deposit (bay) entry.

        :type env: Environment
        :type warehouse: Warehouse
        :type simulation: Simulation
        :param env: the simulation environment (SimPy Environment).
        :param warehouse: the warehouse where the action is performed.
        :param simulation: the simulation where the action is performed.
        """
        super().__init__(env, warehouse, simulation)

    # override
    def simulate_action(self):
        # try to take buffer resource
        with self.simulation.get_res_buffer().request() as req_buf:
            yield req_buf
            # try to take deposit resource
            with self.simulation.get_res_deposit().request() as req_dep:
                yield req_dep
                # check if the deposit and the buffer are empty and full iff the resources are taken
                if self.get_warehouse().get_carousel().is_buffer_full() and \
                        not self.get_warehouse().get_carousel().is_deposit_full():
                    logger.debug(f"Time {self.env.now:5.2f} - Start loading buffer drawer inside the deposit")
                    yield self.env.process(self.simulation.loading_buffer_and_remove())
                    logger.debug(f"Time {self.env.now:5.2f} - Finish loading buffer drawer inside the deposit")
