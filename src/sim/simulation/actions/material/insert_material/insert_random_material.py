from datetime import datetime, timedelta
from simpy import Environment

from src.sim.simulation.actions.action_enum import ActionEnum
from src.sim.simulation.actions.material.insert_material.insert_material import InsertMaterial
from src.sim.simulation.simulation import Simulation
from src.sim.warehouse import Warehouse


class InsertRandomMaterial(InsertMaterial):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation, duration: int):
        """
        The insert random material action is the movement
        performed by the person who has put a material from his hand to the deposit (bay).

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
        from src.sim.material import gen_rand_material

        start_time = datetime.now() + timedelta(seconds=self.env.now)

        with self.simulation.get_res_deposit().request() as req:
            yield req
            drawer_output = super().simulate_action()
            # generate random material
            mat_to_put = gen_rand_material()
            # add the material
            drawer_output.add_material(mat_to_put)
            # estimate a time of the action
            yield self.env.timeout(self.duration)

        end_time = datetime.now() + timedelta(seconds=self.env.now)

        yield self.simulation.get_store_history().put({
            'Type of Action': ActionEnum.INSERT_RANDOM_MATERIAL.value,
            'Start'         : start_time,
            'Finish'        : end_time
        })
