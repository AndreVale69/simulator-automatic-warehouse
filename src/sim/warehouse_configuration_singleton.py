from platform import system
from json import loads
from pathlib import Path
from jsonschema import Draft202012Validator
from yaml import safe_load

from src.sim.configuration import WAREHOUSE_CONFIGURATION


class WarehouseConfigurationSingleton:
    """
    Singleton class to provide access to a single configuration.

    Use it as follows: `WarehouseConfigurationSingleton.get_instance().get_configuration()`
    """
    instance = None

    @staticmethod
    def get_instance():
        """
        Use this method to get an instance and get the configuration file.

        :rtype: WarehouseConfigurationSingleton
        :return: the instance of WarehouseConfigurationSingleton
        """
        if WarehouseConfigurationSingleton.instance is None:
            WarehouseConfigurationSingleton.instance = WarehouseConfigurationSingleton()

        return WarehouseConfigurationSingleton.instance

    def __init__(self):
        # get project directory
        current_dir = Path(__file__)
        project_name = 'simulator-automatic-warehouse'
        project_dir = next(p for p in current_dir.parents if p.parts[-1] == project_name)
        user_configuration_path = f"{project_dir}\\{WAREHOUSE_CONFIGURATION}" if system() == 'Windows' else f"{project_dir}/{WAREHOUSE_CONFIGURATION}"
        json_schema_path = f"{project_dir}\\resources\\configuration\\json_schema.json" if system() == 'Windows' else f"{project_dir}/resources/configuration/json_schema.json"

        # load json_schema
        with open(json_schema_path, "r") as json_schema:
            schema: dict = loads(json_schema.read())

        # check that the json schema is valid
        Draft202012Validator.check_schema(schema)

        # take user configuration
        with open(user_configuration_path, 'r') as file:
            self.configuration: dict = safe_load(file)

        # check if it's valid, raises jsonschema.exceptions.ValidationError if the instance is invalid
        Draft202012Validator(schema).validate(self.configuration)

    def get_configuration(self) -> dict:
        """
        Get the raw configuration from the environment path specified by the user.

        :rtype: dict
        :return: raw configuration extracted via YAML.
        """
        return self.configuration
