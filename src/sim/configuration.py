import os

DOCUMENTATION = """
The configuration file contains all the variables required to run the simulation.
The following variables are required:
- WAREHOUSE_CONFIGURATION_FILE_PATH: a file path to a YAML file and used by the simulator to configure the warehouse.
"""

WAREHOUSE_CONFIGURATION = os.environ['WAREHOUSE_CONFIGURATION_FILE_PATH']
