
.. _dependencies:

============
Dependencies
============

The Simulator Automatic Warehouse uses 4 dependencies:

- `Pandas <https://github.com/pandas-dev/pandas>`_ (``>= 2.2.0``)
  Mainly used to get the results of the simulation in a comprehensive way.

- `SimPy <https://gitlab.com/team-simpy/simpy>`_ (``>= 3.0``)
  Framework used to run the simulation.

- `PyYAML <https://github.com/yaml/pyyaml>`_ (``>= 5.1``)
  Used to safely parse the yaml configuration file.

- `JsonSchema <https://github.com/python-jsonschema/jsonschema>`_ (``>= 4.0.0``)
  Used to load the json schema of the project. The json schema is used to validate the configuration file given as input.

.. seealso::

    `What is JSON Schema? <https://json-schema.org/overview/what-is-jsonschema>`_
        JSON Schema definition, how it works, benefits and more.
