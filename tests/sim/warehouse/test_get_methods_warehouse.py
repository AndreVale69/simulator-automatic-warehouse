import unittest

from src.sim.status_warehouse.container.column import Column
from src.sim.warehouse import Warehouse, MinimumOffsetReturns
from src.sim.warehouse_configuration_singleton import WarehouseConfigurationSingleton


class TestGetMethodsWarehouse(unittest.TestCase):
    def setUp(self):
        self.warehouse = Warehouse()

    def test_get_height(self):
        # arrange
        warehouse = self.warehouse

        # act
        height_get = warehouse.get_height()
        height_expected = warehouse.height

        # assert
        self.assertEqual(height_get, height_expected)

    def test_get_cols_container(self):
        # arrange
        warehouse = self.warehouse

        # act
        cols_container_get = warehouse.get_cols_container()
        cols_container_expected = warehouse.columns_container

        # assert
        self.assertEqual(cols_container_get, cols_container_expected)

    def test_get_column(self):
        # arrange
        warehouse = self.warehouse

        # act
        column_get = warehouse.get_column(0)
        column_expected = warehouse.get_cols_container()[0]

        # assert
        self.assertEqual(column_get, column_expected)

    def test_get_carousel(self):
        # arrange
        warehouse = self.warehouse

        # act
        carousel_get = warehouse.get_carousel()
        carousel_expected = warehouse.carousel

        # assert
        self.assertEqual(carousel_get, carousel_expected)

    def test_get_environment(self):
        # arrange
        warehouse = self.warehouse

        # act
        environment_get = warehouse.get_environment()
        environment_expected = warehouse.env

        # assert
        self.assertEqual(environment_get, environment_expected)

    def test_get_simulation(self):
        # arrange
        warehouse = self.warehouse

        # act
        simulation_get = warehouse.get_simulation()
        simulation_expected = warehouse.simulation

        # assert
        self.assertEqual(simulation_get, simulation_expected)

    def test_get_def_space(self):
        # arrange
        warehouse = self.warehouse

        # act
        def_space_get = warehouse.get_def_space()
        def_space_expected = warehouse.def_space

        # assert
        self.assertEqual(def_space_get, def_space_expected)

    def test_get_speed_per_sec(self):
        # arrange
        warehouse = self.warehouse

        # act
        speed_per_sec_get = warehouse.get_speed_per_sec()
        speed_per_sec_expected = warehouse.speed_per_sec

        # assert
        self.assertEqual(speed_per_sec_get, speed_per_sec_expected)

    def test_get_max_height_material(self):
        # arrange
        warehouse = self.warehouse

        # act
        max_height_material_get = warehouse.get_max_height_material()
        max_height_material_expected = warehouse.max_height_material

        # assert
        self.assertEqual(max_height_material_get, max_height_material_expected)

    def test_get_pos_y_floor(self):
        # arrange
        warehouse = self.warehouse

        # act
        pos_y_floor_get = warehouse.get_pos_y_floor()
        pos_y_floor_expected = warehouse.pos_y_floor

        # assert
        self.assertEqual(pos_y_floor_get, pos_y_floor_expected)

    def test_get_num_drawers(self):
        # arrange
        warehouse = self.warehouse
        config = WarehouseConfigurationSingleton.get_instance().get_configuration()

        # act
        drawers_expected: int = config['simulation']['drawers_to_gen']

        # assert
        self.assertEqual(warehouse.get_num_drawers(), drawers_expected)

    def test_get_minimum_offset(self):
        # arrange
        warehouse = Warehouse()
        col = Column({
            'width': 200,
            'height': 1000,
            'x_offset': 1,
            'height_last_position': 75
        }, warehouse)
        warehouse.add_column(col)

        # act
        minimum_offset: MinimumOffsetReturns = warehouse.get_minimum_offset()

        # assert
        self.assertIn(col, warehouse.get_cols_container())
        self.assertEqual(minimum_offset.index, len(warehouse.get_cols_container())-1)
        self.assertEqual(minimum_offset.offset, 1)
