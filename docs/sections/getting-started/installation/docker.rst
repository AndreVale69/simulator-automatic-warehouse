
======
Docker
======

The Simulator Automatic Warehouse repository contains a docker folder which contains three files:
two docker files with two different distros and a docker compose yaml file.

The ``Dockerfile-alpine`` contains the instructions to run a container with the `alpine distro <https://alpinelinux.org/about/>`_.
Here some characteristics of the container:

+-----------+-------------------------+
| **Docker-alpine**                   |
+===========+=========================+
| OS        | Alpine                  |
+-----------+-------------------------+
| Python    | 3.12.4                  |
+-----------+-------------------------+
| Packages  | - Pandas                |
|           |                         |
|           | - SimPy                 |
|           |                         |
|           | - PyYAML                |
|           |                         |
|           | - JsonSchema            |
|           |                         |
|           | And their dependencies. |
+-----------+-------------------------+

The **main advantage** of using this Docker container is its small size (267 MB).
However, some Linux packages are not supported.

The ``Dockerfile-debian`` contains the instructions to run a container with the debian distro.
Here some characteristics of the container:

+-----------+-------------------------+
| **Docker-debian**                   |
+===========+=========================+
| OS        | Debian                  |
+-----------+-------------------------+
| Python    | 3.12.4                  |
+-----------+-------------------------+
| Packages  | - Pandas                |
|           |                         |
|           | - SimPy                 |
|           |                         |
|           | - PyYAML                |
|           |                         |
|           | - JsonSchema            |
|           |                         |
|           | And their dependencies. |
+-----------+-------------------------+

Its light weight is 341 MB.

You can run these docker files using `docker compose <https://docs.docker.com/compose/>`_:

.. code-block:: bash

    $ cd docker
    $ docker compose up alpine-simulator_automatic_warehouse
