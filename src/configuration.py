from os import environ

DOCUMENTATION = """
The configuration file contains all the variables required to run the simulation.
The following variables are required:
- WAREHOUSE_CONFIGURATION_FILE_PATH: a file path to a YAML file and used by the simulator to configure the warehouse.
- (optional, but select only one of the following) 
    * NO_CONSOLE_LOG: If set, console logs are not displayed.
    * DEBUG_LOG: if set, debug logging will be printed to the console.
    * FILENAME_DEBUG_LOG: if set, save the debug log to file (e.g. log).
"""

WAREHOUSE_CONFIGURATION = environ.get('WAREHOUSE_CONFIGURATION_FILE_PATH')
if WAREHOUSE_CONFIGURATION is None:
    from pathlib import Path
    WAREHOUSE_CONFIGURATION = f'{Path(__file__).parent.parent}/configuration/sample_config.yaml'


NO_CONSOLE_LOG = environ.get('NO_CONSOLE_LOG', None)
DEBUG_LOG = environ.get('DEBUG_LOG', None)
FILENAME_DEBUG_LOG = environ.get('FILENAME_DEBUG_LOG', None)
if DEBUG_LOG and FILENAME_DEBUG_LOG and NO_CONSOLE_LOG:
    raise EnvironmentError("Select whether to print the debug log or save the debug log to a file. "
                           "You've selected more than one of the following: "
                           f"{DEBUG_LOG.__name__}, {FILENAME_DEBUG_LOG.__name__} and "
                           f"{NO_CONSOLE_LOG.__name__}")
