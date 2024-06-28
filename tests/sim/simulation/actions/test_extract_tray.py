from unittest import TestCase

from automatic_warehouse.simulation.actions.action_enum import ActionEnum
from automatic_warehouse.simulation.actions.extract_tray import ExtractTray
from automatic_warehouse.simulation.simulation_type.warehouse_simulation import WarehouseSimulation
from status_warehouse.container.enum_container import EnumContainer
from status_warehouse.tray import Tray
from automatic_warehouse.warehouse import Warehouse


class TestExtractTray(TestCase):
    def test_simulate_action_carousel_empty(self):
        # arrange
        warehouse = Warehouse()
        warehouse.cleanup_carousel()
        simulation = WarehouseSimulation(warehouse)
        action = ExtractTray(simulation.env, simulation.warehouse, simulation)

        # act
        simulation.env.process(action.simulate_action(destination=EnumContainer.CAROUSEL))
        simulation.env.run()
        action_performed: list = simulation.get_store_history().items

        self.assertEqual(len(action_performed), 1)
        action_performed: dict = action_performed[0]
        self.assertIsInstance(action_performed, dict)
        self.assertEqual(ActionEnum.EXTRACT_TRAY.value, action_performed['Type of Action'])

    def test_simulate_action_bay_occupied(self):
        # arrange
        warehouse = Warehouse()
        warehouse.cleanup_carousel()
        warehouse.get_carousel().add_tray(Tray())
        simulation = WarehouseSimulation(warehouse)
        action = ExtractTray(simulation.env, simulation.warehouse, simulation)

        # act
        num_entries_occupied_pre_sim = simulation.warehouse.get_carousel().get_num_entries_occupied()
        simulation.env.process(action.simulate_action(destination=EnumContainer.CAROUSEL))
        simulation.env.run()
        action_performed: list = simulation.get_store_history().items

        self.assertEqual(len(action_performed), 1)
        action_performed: dict = action_performed[0]
        self.assertIsInstance(action_performed, dict)
        self.assertEqual(ActionEnum.EXTRACT_TRAY.value, action_performed['Type of Action'])
        self.assertEqual(num_entries_occupied_pre_sim, 1)
        self.assertEqual(simulation.warehouse.get_carousel().get_num_entries_occupied(), 2)
        self.assertIsInstance(simulation.warehouse.get_carousel().get_buffer_tray(), Tray)
