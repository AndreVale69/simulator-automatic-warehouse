from datetime import datetime, timedelta
from logging import getLogger

from simpy import Environment

from automatic_warehouse.simulation.actions.action_enum import ActionEnum
from automatic_warehouse.simulation.actions.material.insert_material.insert_material import InsertMaterial
from automatic_warehouse.simulation.simulation import Simulation
from automatic_warehouse.warehouse import Warehouse

logger = getLogger(__name__)


class InsertRandomMaterial(InsertMaterial):
    """
    The insert random material action is the movement
    performed by the person who has put a material from his hand to the bay.

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
        assert tray is None, logger.warning("A random material is added to the bay tray, "
                                              "so the tray parameter is not taken into account.")
        assert destination is None, logger.warning("The default destination parameter is bay, "
                                                   "so the destination parameter is not taken into account.")
        from automatic_warehouse.status_warehouse.material import gen_rand_material

        env, simulation = self.env, self.simulation

        start_time = datetime.now() + timedelta(seconds=env.now)

        with simulation.get_res_bay().request() as req:
            yield req
            # add random material
            logger.debug(f"Time {env.now:5.2f} - Start putting materials inside a tray")
            self.warehouse.get_carousel().get_bay_entry().get_tray().add_material(gen_rand_material())
            # estimate a time of the action
            yield env.timeout(self.duration)

        end_time = datetime.now() + timedelta(seconds=env.now)

        yield simulation.get_store_history().put({
            'Type of Action': ActionEnum.INSERT_RANDOM_MATERIAL.value,
            'Start'         : start_time,
            'Finish'        : end_time
        })
