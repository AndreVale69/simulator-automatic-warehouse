from os import environ
from platform import system
from pathlib import Path

DOCUMENTATION = """
The configuration file contains all the variables required to run the simulation.
The following variables are required:
- WAREHOUSE_CONFIGURATION_FILE_PATH.
- (optional, but select only one of the following) 
    * NO_CONSOLE_LOG: if set, console logs are not displayed.
    * DEBUG_LOG: if set, debug logging will be printed to the console.
    * FILENAME_DEBUG_LOG: if set, save the debug log to file (e.g. log).
"""

config_file_path = Path(__file__).parent.parent
WAREHOUSE_CONFIGURATION = environ.get(
    'WAREHOUSE_CONFIGURATION_FILE_PATH',
    f'{config_file_path}\\automatic_warehouse-config\\sample_config.yaml' if system() == 'Windows'
    else f'{config_file_path}/automatic_warehouse-config/sample_config.yaml'
)
"""
It takes the value of the ``WAREHOUSE_CONFIGURATION_FILE_PATH`` environment variable.
It represents a file path to a YAML file used by the simulator to configure the warehouse.
The default value is ``automatic_warehouse-config/sample_config.yaml``.
"""

NO_CONSOLE_LOG = environ.get('NO_CONSOLE_LOG', None)
"""
Takes the value of the ``NO_CONSOLE_LOG`` environment variable.
If set, console logs are not displayed.
"""

DEBUG_LOG = environ.get('DEBUG_LOG', None)
"""
Takes the value of the ``DEBUG_LOG`` environment variable.
If set, debug logging will be printed to the console.
"""

FILENAME_DEBUG_LOG = environ.get('FILENAME_DEBUG_LOG', None)
"""
Takes the value of the ``FILENAME_DEBUG_LOG`` environment variable.
If set, save the debug log to file (e.g. log).
"""

if DEBUG_LOG and FILENAME_DEBUG_LOG and NO_CONSOLE_LOG:
    raise EnvironmentError("Select whether to print the debug log or save the debug log to a file. "
                           "You've selected more than one of the following: "
                           f"{DEBUG_LOG.__name__}, {FILENAME_DEBUG_LOG.__name__} and "
                           f"{NO_CONSOLE_LOG.__name__}")
