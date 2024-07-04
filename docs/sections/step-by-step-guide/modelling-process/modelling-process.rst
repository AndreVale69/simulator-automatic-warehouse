
.. _modelling process:

=================
Modelling process
=================

When you want to buy something, you usually read the specifications of the item you want.
For example, if you want to buy a new car, you might want to know how much it costs, how much horsepower it has,
how much fuel it consumes, and so on.

With the same logic, the Simulator Automatic Warehouse library wants to know from the user
*How is your environment modelled?*.
In our case, the subject of modelling is an automatic warehouse.

A user should start here, from the modelling process of his industrial automatic warehouse.

The modelling can be digitised using a ``YAML`` file.
In this file you can write the dimensions of your warehouse and the parameters of the simulation.

In the following code we can see a sample configuration where we use every available field allowed by the schema.
The Json Schema used to validate your configuration can be found in the package you install from pip
(in the ``automatic_warehouse-res`` folder), or
`online in the repository <https://github.com/AndreVale69/simulator-automatic-warehouse/blob/main/automatic_warehouse-res/configuration/json_schema.json>`_.

.. code-block:: yaml

    height_warehouse: 1000
    default_height_space: 25
    speed_per_sec: 1

    tray:
      length: 390
      width: 180
      maximum_height: 140

    columns:
      - description: "right_column"
        length: 400
        width: 250
        height: 325
        offset_formula_description: "width / 2"
        x_offset: 125
        height_last_position: 75

      - description: "left_column"
        length: 400
        width: 200
        height: 1000
        offset_formula_description: "(left_column.width / 2) + right_column.offset + 250"
        x_offset: 475
        height_last_position: 75

    carousel:
      description: "carousel-bay_and_buffer"
      width: 250
      length: 400
      hole_height: 375
      bay_height: 150
      buffer_height: 150
      offset_formula_description: "width / 2"
      x_offset: 125

    simulation:
      time: 10000
      num_actions: 100
      trays_to_gen: 5
      materials_to_gen: 3
      gen_bay: false
      gen_buffer: false

A full explanation of each field in the configuration can be found in the dedicated section (:ref:`configuration`).
Here we present a sample configuration that you can use to run your first code.
Don't worry if you don't understand some of the fields, we have a special section where we talked about that.
Also, this section should be a step-by-step guide to understand *how to approach* the library.

As you can see in the configuration, we have a warehouse with a height of 1000.
The warehouse has two columns and a carousel.
Each tray that you can find in the warehouse has some specifications.
Finally, the simulation is set to perform 100 actions and create a warehouse filled with 5 trays and 3 materials.

Then we will save the configuration in a YAML file, e.g. ``my-config.yaml``.
