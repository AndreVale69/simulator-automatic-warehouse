from logging import getLogger
from datetime import datetime, timedelta
from simpy import Environment

from sim.simulation.actions.action_enum import ActionEnum
from src.sim.simulation.actions.material.remove_material.remove_material import RemoveMaterial

# from src.drawer import Drawer
from src.sim.material import Material
from src.sim.simulation.simulation import Simulation
from src.sim.warehouse import Warehouse

logger = getLogger(__name__)


class RemoveManualMaterial(RemoveMaterial):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation,
                 duration: int, materials: list[Material]):
        """
        The remove manual material action is the movement
        performed by the person who has removed a material from the deposit (bay) to their hand.

        :type env: Environment
        :type warehouse: Warehouse
        :type simulation: Simulation
        :type duration: int
        :type materials: list[Material]
        :param env: the simulation environment (SimPy Environment).
        :param warehouse: the warehouse where the action is performed.
        :param simulation: the simulation where the action is performed.
        :param duration: the duration of the action in seconds.
        :param materials: the materials to be removed.
        """
        super().__init__(env, warehouse, simulation, duration)
        self.materials = materials.copy()

    def get_materials(self) -> list[Material]:
        """
        Get the list of materials to be removed.

        :rtype: list[Material]
        :return: the list of materials to be removed.
        """
        return self.materials

    # override
    def simulate_action(self):
        start_time = datetime.now() + timedelta(seconds=self.get_env().now)

        with self.simulation.get_res_deposit().request() as req:
            yield req
            drawer_output = super().simulate_action()
            if len(drawer_output.get_items()) != 0:
                for material in self.materials:
                    # remove the material
                    drawer_output.remove_material(material)
                # estimate a time of the action
                yield self.env.timeout(self.duration)
            else:
                logger.debug(f"\nTime {self.env.now:5.2f} - No materials to remove\n")

        end_time = datetime.now() + timedelta(seconds=self.get_env().now)

        yield self.simulation.get_store_history().put({
            'Type of Action': ActionEnum.REMOVE_MANUAL_MATERIAL.value,
            'Start': start_time,
            'Finish': end_time
        })
