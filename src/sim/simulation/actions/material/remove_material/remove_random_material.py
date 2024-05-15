from random import choice
from logging import getLogger
from datetime import datetime, timedelta
from simpy import Environment

from src.sim.simulation.actions.action_enum import ActionEnum
from src.sim.simulation.actions.material.remove_material.remove_material import RemoveMaterial
from src.sim.simulation.simulation import Simulation
from src.sim.warehouse import Warehouse

logger = getLogger(__name__)


class RemoveRandomMaterial(RemoveMaterial):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation, duration: int):
        """
        The remove random material action is the movement
        performed by the person who has removed a material from the deposit (bay) to their hand.

        :type env: Environment
        :type warehouse: Warehouse
        :type simulation: Simulation
        :type duration: int
        :param env: the simulation environment (SimPy Environment).
        :param warehouse: the warehouse where the action is performed.
        :param simulation: the simulation where the action is performed.
        :param duration: the duration of the action in seconds.
        """
        super().__init__(env, warehouse, simulation, duration)

    # override
    def simulate_action(self):
        start_time = datetime.now() + timedelta(seconds=self.get_env().now)

        with self.simulation.get_res_deposit().request() as req:
            yield req
            drawer_output = super().simulate_action()
            # check if there is a material to remove
            if len(drawer_output.get_items()) != 0:
                # choice random material
                mat_to_rmv = choice(drawer_output.get_items())
                # remove the material
                drawer_output.remove_material(mat_to_rmv)
                # estimate a time of the action
                yield self.env.timeout(self.duration)
            else:
                logger.debug(f"\nTime {self.env.now:5.2f} - No materials to remove\n")

        end_time = datetime.now() + timedelta(seconds=self.get_env().now)

        yield self.simulation.get_store_history().put({
            'Type of Action': ActionEnum.REMOVE_RANDOM_MATERIAL.value,
            'Start'         : start_time,
            'Finish'        : end_time
        })
