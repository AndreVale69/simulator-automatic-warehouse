.. only:: html

    .. figure:: _static/logo/small-logo.png
        :align: center

        Simulator and Digital Twin of an Automatic Warehouse

        `PyPI <https://pypi.python.org/pypi/simulator-automatic-warehouse>`_ |
        `GitHub <https://github.com/AndreVale69/simulator-automatic-warehouse>`_ |
        `Issues
        <https://github.com/AndreVale69/simulator-automatic-warehouse/issues>`_

========
Overview
========

Welcome to the Simulator Automatic Warehouse documentation!

The Simulator Automatic Warehouse is a Python library that provides two main functions:
a `digital twin <https://en.wikipedia.org/wiki/Digital_twin>`_ of an automatic warehouse and a simulator
of an automatic warehouse.

The following code shows a basic example of creating a warehouse,
creating a simulation environment and running a simulation.

.. code-block:: python

    from automatic_warehouse.warehouse import Warehouse
    from automatic_warehouse.simulation.simulation_type.warehouse_simulation import WarehouseSimulation

    # generate a Warehouse
    warehouse = Warehouse()

    # generate a simulation environment
    simulation = WarehouseSimulation(warehouse)

    # run the simulation
    simulation.run_simulation()

    # print the results
    print(simulation.get_store_history_dataframe().to_markdown())


-----------------
Table of Contents
-----------------

.. toctree::
   :maxdepth: 2

   Overview <self>
   description

Try me:

.. autoclass:: automatic_warehouse.warehouse.Warehouse
   :inherited-members:
