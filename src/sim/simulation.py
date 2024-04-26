import copy
import logging

import simpy
from simpy import Environment

from src.sim.warehouse import Warehouse

logger = logging.getLogger(__name__)



class Simulation:
    def __init__(self, env: Environment, warehouse: Warehouse):
        """
        The main simulation class.

        :type env: Environment
        :type warehouse: Warehouse
        :param env: the environment of SimPy.
        :param warehouse: the Warehouse used to perform the simulation.
        """
        self.env = env
        # start the move process everytime an instance is created.
        self.warehouse = copy.deepcopy(warehouse)

        # allocation of carousel resources
        self.res_buffer = simpy.Resource(env, capacity=1)
        self.res_deposit = simpy.Resource(env, capacity=1)
        self.store_history = None

    def simulate_actions(self, events_generated: list):
        """
        Simulate actions using the list of events generated.

        :type events_generated: list
        :param events_generated: events to be simulated.
        """
        from src.sim.status_warehouse.enum_warehouse import EnumWarehouse
        from src.sim.status_warehouse.simulate_events.buffer import Buffer
        from src.sim.status_warehouse.simulate_events.send_back_drawer import SendBackDrawer
        from src.sim.status_warehouse.simulate_events.extract_drawer import ExtractDrawer
        from src.sim.status_warehouse.simulate_events.material.insert_material.insert_random_material \
            import InsertRandomMaterial
        from src.sim.status_warehouse.simulate_events.material.remove_material.remove_random_material \
            import RemoveRandomMaterial

        self.store_history = simpy.Store(self.get_environment(), capacity=len(events_generated))

        # run "control of buffer" process
        yield self.env.process(Buffer(self.env, self.get_warehouse(), self).simulate_action())

        # exec all events
        logger.info("Simulation started.")
        for index, event in enumerate(events_generated):
            match event:
                case "send_back":
                    logger.debug(f"~ Operation #{index} ~")
                    action = SendBackDrawer(self.get_environment(), self.get_warehouse(), self,
                                            EnumWarehouse.COLUMN)
                    yield self.env.process(action.simulate_action())
                    logger.debug(f"Time {self.env.now:5.2f} - FINISH SEND_BACK\n")

                case "extract_drawer":
                    logger.debug(f"~ Operation #{index} ~")
                    action = ExtractDrawer(self.get_environment(), self.get_warehouse(), self,
                                           EnumWarehouse.CAROUSEL)
                    yield self.env.process(action.simulate_action())
                    logger.debug(f"Time {self.env.now:5.2f} - FINISH EXTRACT_DRAWER\n")

                case "ins_mat":
                    logger.debug(f"~ Operation #{index} ~")
                    action = InsertRandomMaterial(self.get_environment(), self.get_warehouse(), self, duration=2)
                    yield self.env.process(action.simulate_action())
                    logger.debug(f"Time {self.env.now:5.2f} - FINISH INS_MAT\n")

                case "rmv_mat":
                    logger.debug(f"~ Operation #{index} ~")
                    action = RemoveRandomMaterial(self.get_environment(), self.get_warehouse(), self, duration=2)
                    yield self.env.process(action.simulate_action())
                    logger.debug(f"Time {self.env.now:5.2f} - FINISH RMV_MAT\n")

        logger.debug(f"Time {self.env.now:5.2f} - Finish simulation")
        logger.info("Simulation finished.")

    def get_environment(self) -> simpy.Environment:
        """
        Get the environment of SimPy.

        :rtype: simpy.Environment
        :return: the environment of SimPy.
        """
        return self.env

    def get_warehouse(self) -> Warehouse:
        """
        Get the Warehouse used to perform the simulation.

        :rtype: Warehouse
        :return: the Warehouse used to perform the simulation.
        """
        return self.warehouse

    def get_res_buffer(self) -> simpy.Resource:
        """
        Get the resource of the buffer.
        It can be thought of as a resource lock (see SimPy resource).

        :rtype: simpy.Resource
        :return: the resource of the buffer.
        """
        return self.res_buffer

    def get_res_deposit(self) -> simpy.Resource:
        """
        Get the resource of the deposit (bay).
        It can be thought of as a resource lock (see SimPy resource).

        :rtype: simpy.Resource
        :return: the resource of the deposit (bay).
        """
        return self.res_deposit

    def get_store_history(self) -> simpy.Store:
        """
        Get the SimPy store (see SimPy store) of the simulation.
        It is used to store the simulation history.

        :rtype: simpy.Store
        :return: the store of the simulation history.
        """
        return self.store_history

    #def get_store_history_items(self) -> list[dict]:
    #    """
    #        Attention! Use yield!
    #    """
    #    return self.store_history.get().items()
