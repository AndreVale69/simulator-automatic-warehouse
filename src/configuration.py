import os

DOCUMENTATION = """
The configuration file contains all the variables required to run the simulation.
The following variables are required:
- WAREHOUSE_CONFIGURATION_FILE_PATH: a file path to a YAML file and used by the simulator to configure the warehouse.
- (optional, but select only one of the following) 
    * NO_CONSOLE_LOG: If set, console logs are not displayed.
    * DEBUG_LOG: if set, debug logging will be printed to the console.
    * FILENAME_DEBUG_LOG: if set, save the debug log to file (e.g. log).
"""

WAREHOUSE_CONFIGURATION = os.environ.get('WAREHOUSE_CONFIGURATION_FILE_PATH',
                                         '../resources/configuration/json_schema.json')

NO_CONSOLE_LOG = os.environ.get('NO_CONSOLE_LOG', None)
DEBUG_LOG = os.environ.get('DEBUG_LOG', None)
FILENAME_DEBUG_LOG = os.environ.get('FILENAME_DEBUG_LOG', None)
if DEBUG_LOG and FILENAME_DEBUG_LOG and NO_CONSOLE_LOG:
    raise EnvironmentError("Select whether to print the debug log or save the debug log to a file. "
                           "You've selected more than one of the following: "
                           "DEBUG_LOG, FILENAME_DEBUG_LOG and NO_CONSOLE_LOG")
