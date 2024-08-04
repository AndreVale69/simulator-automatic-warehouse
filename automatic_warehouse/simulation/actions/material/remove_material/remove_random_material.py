from datetime import datetime, timedelta
from logging import getLogger
from random import choice

from simpy import Environment

from automatic_warehouse.simulation.actions.action_enum import ActionEnum
from automatic_warehouse.simulation.actions.material.remove_material.remove_material import RemoveMaterial
from automatic_warehouse.simulation.simulation import Simulation
from automatic_warehouse.warehouse import Warehouse

logger = getLogger(__name__)


class RemoveRandomMaterial(RemoveMaterial):
    """
    The remove random material action is the movement
    performed by the person who has removed a material from the bay to their hand.

    :type env: Environment
    :type warehouse: Warehouse
    :type simulation: Simulation
    :type duration: int
    :param env: the simulation environment (SimPy Environment).
    :param warehouse: the warehouse where the action is performed.
    :param simulation: the simulation where the action is performed.
    :param duration: the duration of the action in seconds.
    """

    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation, duration: int):
        super().__init__(env, warehouse, simulation, duration)

    # override
    def simulate_action(self, tray=None, destination=None):
        assert tray is None, logger.warning("A random material is removed from the bay tray, "
                                              "so the tray parameter is not taken into account.")
        assert destination is None, logger.warning("The default destination parameter is bay, "
                                                   "so the destination parameter is not taken into account.")

        env, simulation = self.env, self.simulation
        start_time = datetime.now() + timedelta(seconds=env.now)

        with simulation.get_res_bay().request() as req:
            yield req
            logger.debug(f"Time {env.now:5.2f} - Start removing material from a tray")
            tray_output = self.warehouse.get_carousel().get_bay_tray()
            # check if there is a material to remove
            if tray_output.get_num_materials() != 0:
                # remove a random material
                tray_output.remove_material(choice(tray_output.get_items()))
                # estimate a time of the action
                yield env.timeout(self.duration)
            else:
                logger.debug(f"\nTime {env.now:5.2f} - No materials to remove\n")

        end_time = datetime.now() + timedelta(seconds=env.now)

        yield simulation.get_store_history().put({
            'Type of Action': ActionEnum.REMOVE_RANDOM_MATERIAL.value,
            'Start'         : start_time,
            'Finish'        : end_time
        })
