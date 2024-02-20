from sim.configuration import WAREHOUSE_CONFIGURATION
from pathlib import Path
from yaml import safe_load
from json import loads
from jsonschema import Draft202012Validator


class WarehouseConfigurationSingleton:
    """
    Singleton class to provide access to a single configuration.
    Use it as follows: <code>WarehouseConfigurationSingleton.get_instance().get_configuration()</code>
    """
    instance = None

    @staticmethod
    def get_instance():
        if WarehouseConfigurationSingleton.instance is None:
            WarehouseConfigurationSingleton.instance = WarehouseConfigurationSingleton()

        return WarehouseConfigurationSingleton.instance

    def __init__(self):
        # get project directory
        current_dir = Path(__file__)
        project_name = 'simulator-automatic-warehouse'
        project_dir = next(p for p in current_dir.parents if p.parts[-1] == project_name)

        # load json_schema
        with open(f"{project_dir}/resources/configuration/json_schema.json", "r") as json_schema:
            schema: dict = loads(json_schema.read())

        # check that the json schema is valid
        Draft202012Validator.check_schema(schema)

        # take user configuration
        with open(f"{project_dir}/{WAREHOUSE_CONFIGURATION}", 'r') as file:
            self.configuration: dict = safe_load(file)

        # check if it's valid, raises jsonschema.exceptions.ValidationError if the instance is invalid
        Draft202012Validator(schema).validate(self.configuration)

    def get_configuration(self) -> dict:
        """
        Get the raw configuration from the environment path specified by the user.<br><br>
        @return: raw configuration extracted via YAML.
        """
        return self.configuration
