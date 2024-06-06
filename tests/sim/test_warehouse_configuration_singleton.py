from unittest import TestCase

from src.warehouse_configuration_singleton import (
    WarehouseConfigurationSingleton,
    WarehouseConfiguration,
    ColumnConfiguration,
    CarouselConfiguration,
    SimulationConfiguration
)


class TestWarehouseConfigurationSingleton(TestCase):
    def tearDown(self):
        WarehouseConfigurationSingleton.get_instance().update_config_from_file('test_config.yaml')

    def test_singleton(self):
        # arrange
        warehouse_configuration_singleton = WarehouseConfigurationSingleton.get_instance()

        # act

        # assert
        self.assertEqual(warehouse_configuration_singleton, WarehouseConfigurationSingleton.get_instance())

    def test_update_config_from_file(self):
        # arrange
        old_config = WarehouseConfigurationSingleton.get_instance().get_configuration()

        # act
        new_instance = WarehouseConfigurationSingleton.get_instance().update_config_from_file('test_config_2.yaml')
        new_config = new_instance.get_configuration()

        # assert
        self.assertNotEqual(old_config, new_config)

    def test_update_config(self):
        # arrange
        old_config = WarehouseConfigurationSingleton.get_instance().get_configuration()

        # act
        new_instance = WarehouseConfigurationSingleton.get_instance().update_config(
            WarehouseConfiguration(
                height_warehouse=1000,
                default_height_space=1000,
                speed_per_sec=1000,
                columns=[
                    ColumnConfiguration(
                        description='description',
                        width=1000,
                        height=1000,
                        offset_formula_description='description',
                        x_offset=1000,
                        height_last_position=1000
                    )
                ],
                carousel=CarouselConfiguration(
                    description='desc',
                    width=1000,
                    hole_height=1000,
                    bay_height=1000,
                    buffer_height=1000,
                    offset_formula_description='desc',
                    x_offset=1000
                ),
                simulation=SimulationConfiguration(
                    time=1000,
                    num_actions=1000,
                    trays_to_gen=1000,
                    materials_to_gen=1000,
                    gen_bay=True,
                    gen_buffer=False
                )
            )
        )
        new_config = new_instance.get_configuration()

        # assert
        self.assertNotEqual(old_config, new_config)
