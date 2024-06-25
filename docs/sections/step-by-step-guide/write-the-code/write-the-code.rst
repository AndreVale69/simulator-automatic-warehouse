
==============
Write the code
==============

Once you have created a model of your warehouse, you can use the Simulator Automatic Warehouse library in your script.

For example, in the same directory where you created the ``yaml`` configuration, you can create your digital twin in Python.
You'll also want to create a simulation and run it to see what happens.

.. code-block:: python

    from automatic_warehouse.warehouse import Warehouse
    from automatic_warehouse.simulation.simulation_type.warehouse_simulation import WarehouseSimulation

    # generate a Warehouse using the YAML configuration
    warehouse = Warehouse()

    # generate a simulation environment
    simulation = WarehouseSimulation(warehouse)

    # run the simulation
    simulation.run_simulation()

    # print the results
    print(simulation.get_store_history_dataframe())

We will call this script ``my-script.py``.

In the next section we will show you how to run the script.
Yes, you can easily write the common line command ``python my-script.py``,
but *how do you link the configuration you have written?*
