
.. _dependencies:

============
Dependencies
============

The Simulator Automatic Warehouse uses 4 dependencies:

- `Pandas <https://github.com/pandas-dev/pandas>`_ (`v2.2.3 <https://github.com/pandas-dev/pandas/releases/tag/v2.2.3>`_)
  Mainly used to get the results of the simulation in a comprehensive way.

- `SimPy <https://gitlab.com/team-simpy/simpy>`_ (`4.1.1 <https://gitlab.com/team-simpy/simpy/-/tree/4.1.1?ref_type=tags>`_)
  Framework used to run the simulation.

- `PyYAML <https://github.com/yaml/pyyaml>`_ (`6.0.2 <https://github.com/yaml/pyyaml/releases/tag/6.0.2>`_)
  Used to safely parse the yaml configuration file.

- `JsonSchema <https://github.com/python-jsonschema/jsonschema>`_ (`4.22.0 <https://github.com/python-jsonschema/jsonschema/releases/tag/v4.22.0>`_)
  Used to load the json schema of the project. The json schema is used to validate the configuration file given as input.

.. seealso::

    `What is JSON Schema? <https://json-schema.org/overview/what-is-jsonschema>`_
        JSON Schema definition, how it works, benefits and more.
