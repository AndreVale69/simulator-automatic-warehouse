from unittest import TestCase

from src.sim.warehouse_configuration_singleton import WarehouseConfigurationSingleton
from src.sim.warehouse import Warehouse
from src.sim.simulation.simulation_type.warehouse_simulation.warehouse_simulation import WarehouseSimulation


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
        self.assertIsNone(warehouse_simulation.get_store_history())
        warehouse_simulation.run_simulation()
        res = warehouse_simulation.get_store_history_dataframe().size

        # assert
        self.assertGreater(res, 0)

    def test_new_simulation(self):
        # arrange
        warehouse_simulation = self.warehouse_simulation
        config = WarehouseConfigurationSingleton.get_instance().get_configuration()
        simulation = config["simulation"]
        num_actions = simulation["num_actions"]
        num_gen_drawers = simulation["drawers_to_gen"]
        num_gen_materials = simulation["materials_to_gen"]
        gen_deposit = simulation["gen_deposit"]
        gen_buffer = simulation["gen_buffer"]
        time = simulation["time"]

        # act
        self.assertIsNone(warehouse_simulation.get_store_history())
        warehouse_simulation.new_simulation(
            num_actions,
            num_gen_drawers,
            num_gen_materials,
            gen_deposit,
            gen_buffer,
            time
        )
        res = warehouse_simulation.get_store_history_dataframe().size

        # assert
        self.assertGreater(res, 0)
