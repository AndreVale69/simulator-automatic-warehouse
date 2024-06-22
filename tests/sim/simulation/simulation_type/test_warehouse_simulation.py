from unittest import TestCase

from automatic_warehouse.simulation.simulation_type.warehouse_simulation import WarehouseSimulation
from automatic_warehouse.warehouse import Warehouse
from automatic_warehouse.warehouse_configuration_singleton import WarehouseConfigurationSingleton


class TestWarehouseSimulation(TestCase):
    def setUp(self):
        self.warehouse_simulation = WarehouseSimulation(Warehouse())

    def test_eq(self):
        # arrange
        warehouse_simulation = self.warehouse_simulation

        # act

        # assert
        self.assertTrue(warehouse_simulation.__eq__(warehouse_simulation))

    def test_run_simulation(self):
        # arrange
        warehouse_simulation = self.warehouse_simulation

        # act
        self.assertListEqual(warehouse_simulation.get_store_history().items, [])
        warehouse_simulation.run_simulation()
        res = warehouse_simulation.get_store_history_dataframe().size

        # assert
        self.assertGreater(res, 0)

    def test_new_simulation(self):
        # arrange
        warehouse_simulation = self.warehouse_simulation
        config = WarehouseConfigurationSingleton.get_instance().get_configuration().simulation
        num_actions = config.num_actions
        num_gen_trays = config.trays_to_gen
        num_gen_materials = config.materials_to_gen
        gen_bay = config.gen_bay
        gen_buffer = config.gen_buffer
        time = config.time

        # act
        self.assertListEqual(warehouse_simulation.get_store_history().items, [])
        warehouse_simulation.new_simulation(
            num_actions,
            num_gen_trays,
            num_gen_materials,
            gen_bay,
            gen_buffer,
            time
        )
        res = warehouse_simulation.get_store_history_dataframe().size

        # assert
        self.assertGreater(res, 0)
