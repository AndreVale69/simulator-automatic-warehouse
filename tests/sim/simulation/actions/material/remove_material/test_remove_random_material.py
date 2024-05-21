from unittest import TestCase

from src.sim.simulation.actions.material.remove_material.remove_random_material import RemoveRandomMaterial
from src.sim.simulation.actions.action_enum import ActionEnum
from src.sim.simulation.simulation_type.warehouse_simulation.warehouse_simulation import WarehouseSimulation
from src.sim.warehouse import Warehouse


class TestRemoveRandomMaterial(TestCase):
    def test_simulate_action(self):
        # arrange
        simulation = WarehouseSimulation(Warehouse())
        duration = 5
        init_num_materials: int = simulation.get_warehouse().get_carousel().get_deposit_drawer().get_num_materials()
        material = RemoveRandomMaterial(simulation.get_environment(), simulation.get_warehouse(), simulation, duration)

        # act
        simulation.env.process(material.simulate_action())
        simulation.env.run()
        action_performed: list = simulation.get_store_history().items

        self.assertEqual(len(action_performed), 1)
        action_performed: dict = action_performed[0]
        self.assertIsInstance(action_performed, dict)
        self.assertEqual(ActionEnum.REMOVE_RANDOM_MATERIAL.value, action_performed['Type of Action'])
        self.assertGreaterEqual((action_performed['Finish']-action_performed['Start']).total_seconds(), duration)
        self.assertLess(simulation.get_warehouse().get_carousel().get_deposit_drawer().get_num_materials(), init_num_materials)
