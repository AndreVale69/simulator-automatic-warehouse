from __future__ import annotations

from dataclasses import dataclass, asdict, field
from json import loads
from pathlib import Path
from platform import system

from jsonschema import Draft202012Validator

from automatic_warehouse.env_vars import WAREHOUSE_CONFIGURATION


@dataclass
class TrayConfiguration:
    """ `Python Dataclass <https://docs.python.org/3/library/dataclasses.html>`_ - Tray Configuration. """
    length: int
    width: int
    maximum_height: int


@dataclass
class ColumnConfiguration:
    """ `Python Dataclass <https://docs.python.org/3/library/dataclasses.html>`_ - Column Configuration. """
    length: int
    height: int
    x_offset: int
    width: int
    height_last_position: int
    description: str | None = field(default=None)
    offset_formula_description: str | None = field(default=None)

    def __post_init__(self):
        if False in {
            isinstance(self.width, int), isinstance(self.height, int),
            isinstance(self.x_offset, int), isinstance(self.height_last_position, int)
        }:
            raise TypeError("The parameters must be integers")


@dataclass
class CarouselConfiguration:
    """ `Python Dataclass <https://docs.python.org/3/library/dataclasses.html>`_ - Carousel Configuration. """
    length: int
    width: int
    hole_height: int
    bay_height: int
    buffer_height: int
    x_offset: int
    description: str | None = field(default=None)
    offset_formula_description: str | None = field(default=None)

    def __post_init__(self):
        if False in {isinstance(self.width, int), isinstance(self.hole_height, int),
                     isinstance(self.bay_height, int), isinstance(self.buffer_height, int),
                     isinstance(self.x_offset, int)}:
            raise TypeError("The parameters must be integers")


@dataclass
class SimulationConfiguration:
    """ `Python Dataclass <https://docs.python.org/3/library/dataclasses.html>`_ - Simulation Configuration. """
    num_actions: int
    trays_to_gen: int
    materials_to_gen: int
    gen_bay: bool
    gen_buffer: bool
    time: int | None = None


@dataclass
class WarehouseConfiguration:
    """ `Python Dataclass <https://docs.python.org/3/library/dataclasses.html>`_ - Warehouse Configuration. """
    height_warehouse: int
    default_height_space: int
    speed_per_sec: int | float
    tray: TrayConfiguration
    columns: list[ColumnConfiguration]
    carousel: CarouselConfiguration
    simulation: SimulationConfiguration


class WarehouseConfigurationSingleton:
    """
    `Singleton class <https://en.wikipedia.org/wiki/Singleton_pattern>`_ 
    to provide access to a single configuration.

    This class is responsible for safely loading yaml from a file, 
    overriding an existing configuration with a new yaml file or hardcoded configuration. 
    It also calls the :class:`ConfigurationValidator <automatic_warehouse.configuration_validator.ConfigurationValidator>` class to check some additional logical properties.

    Use it as follows: ``WarehouseConfigurationSingleton.get_instance().get_configuration()``.

    :type file_path: str
    :param file_path: the configuration to load into the simulator. 
                      If not specified, the sample configuration will be loaded.
    """
    instance = None

    @staticmethod
    def get_instance():
        """
        Use this method to get an instance and get the configuration file.

        :rtype: WarehouseConfigurationSingleton
        :return: the instance of WarehouseConfigurationSingleton.
        """
        if WarehouseConfigurationSingleton.instance is None:
            WarehouseConfigurationSingleton.instance = WarehouseConfigurationSingleton()

        return WarehouseConfigurationSingleton.instance

    def __init__(self, file_path: str=WAREHOUSE_CONFIGURATION):
        self._json_schema: dict | None = None
        # get project directory
        # https://docs.python.org/3.12/library/platform.html#platform.system
        path = Path(__file__).parent.parent
        self._json_schema_path = (
            f"{path}\\automatic_warehouse-res\\configuration\\json_schema.json"
            if system() == 'Windows' else
            f"{path}/automatic_warehouse-res/configuration/json_schema.json"
        )
        raw_config: dict = self._json_schema_validator_from_file(file_path)
        self.configuration = WarehouseConfiguration(
            height_warehouse=raw_config['height_warehouse'],
            default_height_space=raw_config['default_height_space'],
            speed_per_sec=raw_config['speed_per_sec'],
            tray=TrayConfiguration(
                length=raw_config['tray']['length'],
                width=raw_config['tray']['width'],
                maximum_height=raw_config['tray']['maximum_height']
            ),
            columns=[
                ColumnConfiguration(
                    description=col.get('description'),
                    length=col['length'],
                    width=col['width'],
                    height=col['height'],
                    offset_formula_description=col.get('offset_formula_description'),
                    x_offset=col['x_offset'],
                    height_last_position=col['height_last_position']
                ) for col in raw_config['columns']
            ],
            carousel=CarouselConfiguration(
                description=raw_config['carousel'].get('description'),
                width=raw_config['carousel']['width'],
                length=raw_config['carousel']['length'],
                hole_height=raw_config['carousel']['hole_height'],
                bay_height=raw_config['carousel']['bay_height'],
                buffer_height=raw_config['carousel']['buffer_height'],
                offset_formula_description=raw_config['carousel'].get('offset_formula_description'),
                x_offset=raw_config['carousel']['x_offset']
            ),
            simulation=SimulationConfiguration(
                time=raw_config['simulation'].get('time'),
                num_actions=raw_config['simulation']['num_actions'],
                trays_to_gen=raw_config['simulation']['trays_to_gen'],
                materials_to_gen=raw_config['simulation']['materials_to_gen'],
                gen_bay=raw_config['simulation']['gen_bay'],
                gen_buffer=raw_config['simulation']['gen_buffer']
            )
        )
        from automatic_warehouse.configuration_validator import ConfigurationValidator
        ConfigurationValidator(self.configuration).validate()

    def _json_schema_validator_from_file(self, file_path: str):
        """
        Validation of a configuration from file.

        :type file_path: str
        :param file_path: configuration to load.
        :return: the configuration loaded.
        :raises jsonschema.exceptions.ValidationError: if the instance is invalid.
        :raises FileNotFoundError: if the file is not found.
        """
        schema = self._get_json_schema()

        # take user configuration
        from yaml import safe_load
        with open(file_path, 'r') as file:
            configuration: dict = safe_load(file)

        # check if it's valid, raises jsonschema.exceptions.ValidationError if the instance is invalid
        Draft202012Validator(schema).validate(configuration)

        return configuration

    def _json_schema_validator(self, configuration: WarehouseConfiguration):
        """
        Hardcoded validation of a configuration.

        :type configuration: WarehouseConfiguration
        :param configuration: config to validate.
        :raises jsonschema.exceptions.ValidationError: if the instance is invalid.
        """
        schema = self._get_json_schema()

        # check if it's valid, raises jsonschema.exceptions.ValidationError if the instance is invalid
        Draft202012Validator(schema).validate(asdict(configuration))

    def _get_json_schema(self) -> dict:
        """
        Get the json schema.
        Load the json schema from file iff not already loaded.

        :rtype dict
        :return: json schema.
        """
        # load json_schema iff not in cache
        if schema := self._json_schema:
            return schema
        with open(self._json_schema_path, "r") as json_schema:
            schema = loads(json_schema.read())

        # check that the json schema is valid
        Draft202012Validator.check_schema(schema)

        # if valid, save
        self._json_schema = schema

        return schema

    def get_configuration(self) -> WarehouseConfiguration:
        """
        Get the raw configuration from the environment path specified by the user.

        :rtype: dict
        :return: raw configuration extracted via YAML.
        """
        return self.configuration

    @staticmethod
    def update_config_from_file(file_path: str):
        """
        Update the configuration from a file.

        :type file_path: str
        :rtype: WarehouseConfigurationSingleton
        :param file_path: file path of the file.
        :return: the instance of WarehouseConfigurationSingleton (:attr:`get_instance()`).
        """
        WarehouseConfigurationSingleton.instance = WarehouseConfigurationSingleton(file_path)
        return WarehouseConfigurationSingleton.get_instance()

    def update_config(self, configuration: WarehouseConfiguration):
        """
        Update the configuration from a dataclass (hardcoded).

        :type configuration: WarehouseConfiguration
        :rtype: WarehouseConfigurationSingleton
        :param configuration: hardcoded configuration.
        :return: the instance of WarehouseConfigurationSingleton (:attr:`get_instance()`).
        :raises jsonschema.exceptions.ValidationError: if the instance is invalid.
        """
        self._json_schema_validator(configuration)
        from automatic_warehouse.configuration_validator import ConfigurationValidator
        ConfigurationValidator(self.configuration).validate()
        self.configuration = configuration
        return WarehouseConfigurationSingleton.get_instance()
