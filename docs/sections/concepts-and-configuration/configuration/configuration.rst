
.. _configuration:

=============
Configuration
=============

This section introduces you to the configuration, a file (or hardcoded Python object) used by the library to create a digital twin of the automatic warehouse and a simulator.

The chapter is divided into two groups: YAML file and hardcoded. The first is strongly recommended for many reasons: it is a file, then you can create different versions; you can use the json schema, which helps to respect some configuration rules, etcetera. The second one is provided by the library to give you the possibility (e.g.) to overwrite the actual configuration at runtime. The second option is not recommended, because it is easy to make mistakes and a large piece of code can reduce the readability of your code.

Note: In the YAML file section, we provide a small guide to understanding how to use a json schema.

---------
YAML file
---------

In the :ref:`modelling process` section you saw an example of a YAML configuration. Here we will explain how to create it and how to model your automatic warehouse and customise your simulator.

The configuration is divided into five groups:

- **General**: general data of the warehouse;
- **Tray**: data about the trays in the store. This data is fundamental because it is used by the library to avoid creating a tray that is too small or too large at runtime;
- **Columns**: data about the columns in the warehouse. This group is a list and each item represents the data about the columns in the warehouse;
- **Carousel**: data about the carousel located in the warehouse. Slightly different from the declaration of a column, as it has only two positions and can have three heights (bay, buffer and hole);
- **Simulation**: data about the simulation.

.. important:: Every measurement is in centimeters.

^^^^^^^
General
^^^^^^^

The general section of the configuration contains some fields that are useful for setting up the warehouse.

- ``height_warehouse``

  **Type**: `integer`

  **Description**: it refers to the total height of the Automatic Warehouse.


- ``default_height_space``

  **Type**: `integer`

  **Description**: it refers to the standard height in the warehouse. As you can see in the :ref:`entries` section, this space is identified by a TrayEntry or an EmptyEntry.


- ``speed_per_sec``

  **Type**: `integer`

  **Description**: it is the speed of the platform. In the centre of the automatic warehouse there is a lift that moves the trays. The `speed_per_sec` field is used in the formula to calculate the time it takes the platform to move between columns (and also up and down). So it's very important to get reliable results.

Example of a warehouse definition with a height of 5 metres (500 centimetres), a default entry height of 25 centimetres and a speed per second of 1:

.. code-block:: yaml

    height_warehouse: 500
    default_height_space: 25
    speed_per_sec: 1


^^^^
Tray
^^^^

The tray section is a general definition of a tray used in the warehouse to store materials. The definition contains the minimum data.
Each of the following fields must be inserted below the ``tray`` field:

- ``length``

  **Type**: `integer`

  **Description**: length of the tray.


- ``width``

  **Type**: `integer`

  **Description**: width of the tray.


- ``maximum_height``

  **Type**: `integer`

  **Description**: the maximum height of a tray is a limit to avoid placing a material too high.


Example of a tray definition with a length of 390 centimetres (3.9 metres), a width of 180 centimetres (1.8 metres) and a maximum height of 140 centimetres (1.4 metres):

.. code-block:: yaml

    tray:
      length: 390
      width: 180
      maximum_height: 140


^^^^^^^
Columns
^^^^^^^

TODO

^^^^^^^^
Carousel
^^^^^^^^

TODO

^^^^^^^^^^
Simulation
^^^^^^^^^^

TODO

---------
Hardcoded
---------

TODO

TODO: Add detailed explanation of each field of the config: yaml and hardcoded.
TODO: Explain how to use the json schema.
