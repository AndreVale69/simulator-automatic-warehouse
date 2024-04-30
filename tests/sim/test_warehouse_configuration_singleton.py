import unittest

from src.sim.warehouse_configuration_singleton import WarehouseConfigurationSingleton


class TestWarehouseConfigurationSingleton(unittest.TestCase):
    def test_singleton(self):
        # arrange
        warehouse_configuration_singleton = WarehouseConfigurationSingleton.get_instance()

        # act

        # assert
        self.assertEqual(warehouse_configuration_singleton, WarehouseConfigurationSingleton.get_instance())
