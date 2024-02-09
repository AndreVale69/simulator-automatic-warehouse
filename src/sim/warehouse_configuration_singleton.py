import json
from configuration import WAREHOUSE_CONFIGURATION
from pathlib import Path


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

        with open(f"{project_dir}/{WAREHOUSE_CONFIGURATION}", 'r') as json_file:
            self.configuration: dict = json.load(json_file)

    def get_configuration(self) -> dict:
        """
        Get the raw configuration from the environment path specified by the user.<br><br>
        @return: raw configuration extracted via JSON.
        """
        return self.configuration
