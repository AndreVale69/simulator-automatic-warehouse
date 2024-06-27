
=================
Run the simulator
=================

The Simulator Automatic Warehouse can be dominated using the environment variables!

An environment variable is a user-definable value that can affect the way running processes will behave on a computer [1]_.

The library accepts four environment variables:

- To check which configuration you want to load:

    - ``WAREHOUSE_CONFIGURATION_FILE_PATH``. It represents a file path to a YAML file used by the simulator to configure the warehouse.

  The **default value** is ``automatic_warehouse-config/sample_config.yaml``.

- To control the console output:

    - ``NO_CONSOLE_LOG``. If set, console logs are not displayed.

    - ``DEBUG_LOG``. If set, debug logging will be printed to the console.

    - ``FILENAME_DEBUG_LOG``. If set, save the debug log to file (e.g. log).

  The **default value** is ``INFO``, so you will only see the minimum on the console.

  .. warning::

        You need to specify only one (or none) environment variable for the console output,
        otherwise the library throws an exception.


After modelling and writing the code, it's time to run our Python code!
Let us assume that our workspace is as follows:

.. code-block:: bash

    .
    ├── my-config.yaml
    └── my-script.py

    0 directories, 2 files

Open a terminal, and write the following command line:

.. code-block::

    $ WAREHOUSE_CONFIGURATION_FILE_PATH='./my-config.yaml' python3 my-script.py

We export the ``WAREHOUSE_CONFIGURATION_FILE_PATH`` environment variable to tell the library
"*hey, take my configuration file, you can find it in the ./my-config.yaml path*".

.. note::

    On Windows you cannot use single line execution, you must export the environment variable using ``$env``:

    .. code-block:: bash

        $env:WAREHOUSE_CONFIGURATION_FILE_PATH='.\my-config.yaml'
        python3.exe my-script.py

The result on the console will be similar to the following:

.. code-block:: bash

    2024-06-25 15:39:02,453 - [INFO] - (automatic_warehouse.warehouse) - The creation of random warehouse is completed.
    2024-06-25 15:39:02,453 - [INFO] - (automatic_warehouse.simulation.simulation_type.warehouse_simulation) - Create a copy of the Warehouse
    2024-06-25 15:39:02,453 - [INFO] - (automatic_warehouse.warehouse) - The creation of random warehouse is completed.
    2024-06-25 15:39:02,454 - [INFO] - (automatic_warehouse.simulation.simulation_type.warehouse_simulation) - Simulation started.
    2024-06-25 15:39:02,463 - [INFO] - (automatic_warehouse.simulation.simulation_type.warehouse_simulation) - Simulation finished. Total time: 0:00:00.009181
              Type of Action                      Start                     Finish
    0            ExtractTray 2024-06-25 15:39:02.454425 2024-06-25 15:39:16.454600
    1           SendBackTray 2024-06-25 15:39:16.454633 2024-06-25 15:39:27.704747
    2            ExtractTray 2024-06-25 15:39:27.704766 2024-06-25 15:39:39.454893
    3   InsertRandomMaterial 2024-06-25 15:39:39.454916 2024-06-25 15:39:41.454962
    4            ExtractTray 2024-06-25 15:39:41.454981 2024-06-25 15:40:03.955119
    ..                   ...                        ...                        ...
    95  RemoveRandomMaterial 2024-06-25 15:53:59.463154 2024-06-25 15:54:01.463174
    96  InsertRandomMaterial 2024-06-25 15:54:01.463195 2024-06-25 15:54:03.463230
    97          SendBackTray 2024-06-25 15:54:03.463249 2024-06-25 15:54:23.463378
    98  RemoveRandomMaterial 2024-06-25 15:54:23.463396 2024-06-25 15:54:25.463417
    99          SendBackTray 2024-06-25 15:54:25.463435 2024-06-25 15:54:37.463528

    [100 rows x 3 columns]

On the left is a human readable time (``yyyy-mm-dd hh:mm:ss``),
in the square brackets is the chosen level (``INFO`` by default,
``DEBUG`` if you choose ``DEBUG_LOG``),
in the round brackets is the file that writes this log, and finally there is the message.

At the end, the simulator also prints the total time taken to run the simulation.

In this console you can also see the history of the actions simulated.
There are four main actions in the warehouse: ``ExtractTray``, ``SendBackTray``, ``InsertRandomMaterial`` and ``RemoveRandomMaterial``.
These will be explained later.

.. [1] `Wikipedia <https://en.wikipedia.org/wiki/Environment_variable>`_
