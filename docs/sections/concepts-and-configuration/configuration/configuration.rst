
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

The Columns section is a list of columns that can be found in the automatic warehouse.
As we can see from the :ref:`columns` section, this container is intended to be used for storage.
Each of the following fields must be inserted below the ``columns`` field:

- ``description``

  **Type**: `string`

  **Description**: each column is identified by an **optional** description, which is only used by the user for readability.


- ``length``

  **Type**: `integer`

  **Description**: length of the column.


- ``width``

  **Type**: `integer`

  **Description**: width of the column.


- ``height``

  **Type**: `integer`

  **Description**: height of the column.


- ``offset_formula_description``

  **Type**: `string`

  **Description**: an optional description of the offset formula used during the simulation to calculate the time of the movement. This is an **optional** field and its purpose is to improve the readability of the configuration. If you are an end user, you can omit this field.


- ``x_offset``

  **Type**: `integer`

  **Description**: the position identifier used by the library to understand where a column is located in the environment. See the :ref:`columns` section in the :ref:`concepts` chapter for a practical example.


- ``height_last_position``

  **Type**: `integer`

  **Description**: the height of the last position is a special feature of these automatic warehouses. It is the last position (at the top of the store) where a tray can be found.


Example of a column definition with a length of 400 centimetres (4 metres), a width of 250 centimetres (2.5 metres), a height of 325 centimetres (3.25 metres), an offset of 125 centimetres (1.25 metres) and a height of the last position of 75 centimetres:

.. code-block:: yaml

    columns:
      # description is optional
      - description: "right_column"
        length: 400
        width: 250
        height: 325
        # optional
        # offset_formula_description: "width / 2"
        x_offset: 125
        height_last_position: 75


^^^^^^^^
Carousel
^^^^^^^^

The Carousel section is a definition of the picking area and two trays: bay and buffer.
As we can see from the :ref:`carousel` section, this container is intended to be used as a picking area and to buffer a tray.
Each of the following fields must be inserted below the ``carousel`` field:

- ``description``

  **Type**: `string`

  **Description**: the carousel is identified by an **optional** description, which is only used by the user for readability.


- ``length``

  **Type**: `integer`

  **Description**: length of the carousel.


- ``width``

  **Type**: `integer`

  **Description**: width of the carousel.


- ``hole_height``

  **Type**: `integer`

  **Description**: is the height of the hole. We suggest you look at the illustration on the :ref:`carousel` section to understand.


- ``bay_height``

  **Type**: `integer`

  **Description**: is the height of the bay. Again, we suggest you look at the illustration on the :ref:`carousel` section to understand.


- ``buffer_height``

  **Type**: `integer`

  **Description**: is the height of the buffer, the tray under the bay. Again, we suggest you look at the illustration on the :ref:`carousel` section to understand.


- ``offset_formula_description``

  **Type**: `string`

  **Description**: an optional description of the offset formula used during the simulation to calculate the time of the movement. This is an **optional** field and its purpose is to improve the readability of the configuration. If you are an end user, you can omit this field.


- ``x_offset``

  **Type**: `integer`

  **Description**: the position identifier used by the library to understand where a column is located in the environment. See the :ref:`columns` section in the :ref:`concepts` chapter for a practical example.


Example of a carousel definition with a length of 400 centimetres (4 metres), a width of 250 centimetres (2.5 metres), an hole height of 375 centimetres (3.75 metres), a bay height of 150 centimetres (1.5 meters), a buffer height of 150 centimetres (1.5 metres), an offset of 125 centimetres (1.25 metres):

.. code-block:: yaml

    carousel:
      # optional
      description: "carousel-bay_and_buffer"
      width: 250
      length: 400
      hole_height: 375
      bay_height: 150
      buffer_height: 150
      # optional
      # offset_formula_description: "width / 2"
      x_offset: 125

^^^^^^^^^^
Simulation
^^^^^^^^^^

The Simulation section is a definition of the simulation configuration.
Each of the following fields must be inserted below the ``simulation`` field:

- ``time``

  **Type**: `integer`

  **Description**: the maximum simulation time. If the total time of the actions to be carried out is greater than the time allowed, the execution will be interrupted. The time is not necessary, it is an **optional** field. If you want to be sure that each action will be performed, clear this field.


- ``num_actions``

  **Type**: `integer`

  **Description**: the number of actions to be performed.


- ``trays_to_gen``

  **Type**: `integer`

  **Description**: the number of trays to be generated. Note that the warehouse is filled from top to bottom.


- ``materials_to_gen``

  **Type**: `integer`

  **Description**: the number of materials to be generated. Note that the materials are placed in random trays.


- ``gen_bay``

  **Type**: `boolean`

  **Description**: true if you want to generate a tray in the bay, false otherwise.


- ``gen_buffer``

  **Type**: `boolean`

  **Description**: true if you want to generate a bay in the buffer (position below the bay), false otherwise. Be careful, if ``gen_bay`` is false, this field cannot be true! Because in general, a warehouse cannot have a status with one tray in the buffer and none in the bay.


Example of a simulation definition with no simulation time requested, 100 actions, 5 trays to be generated in the warehouse, 7 materials to be generated randomly and one tray in the buffer and in the bay:

.. code-block:: yaml

    simulation:
      # optional
      # time: 10000
      num_actions: 100
      trays_to_gen: 5
      materials_to_gen: 7
      gen_bay: true
      gen_buffer: true


---------
Hardcoded
---------

TODO

TODO: Add detailed explanation of each field of the config: yaml and hardcoded.
TODO: Explain how to use the json schema.
