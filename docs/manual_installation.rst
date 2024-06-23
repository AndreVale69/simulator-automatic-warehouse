
===================
Manual Installation
===================

.. warning::

    This is not recommended for non-expert users because:

        - You must manually download a ``.whl`` release.

    Or worse:

        - You need to install `Hatch <https://hatch.pypa.io/1.12/>`_;

        - Build the project;

        - Errors or warnings may occur during the build.

    In addition, if you choose an environment, you need to set it up, install the requirements,
    run the tests to make sure there are no errors.

    If you have problems using PyPI to install the library,
    please `create a new issue <https://github.com/AndreVale69/simulator-automatic-warehouse/issues>`_.
    Thanks for your cooperation.

Since you are here, you may need to manually install the project.
In this section we suggest 3 different ways to do this.
We will start with the easiest one and come to the last one, which is
*how to create a virtual env and use the library natively*.

The three methods are:

1. Get the ``.whl`` file of a specific release and install it using ``pip``;

2. Clone the project, build it using a `build backend <https://packaging.python.org/en/latest/glossary/#term-Build-Backend>`_ and install it;

3. Create and prepare a `virtual environment <https://docs.python.org/3/library/venv.html>`_,
   and run tests to verify that everything works.

---------------------------------------
Download ``.whl`` from the release page
---------------------------------------

From the `release page on GitHub <https://github.com/AndreVale69/simulator-automatic-warehouse/releases>`_,
choose which release you want to install.
Once you have chosen, click on it and download the ``.whl`` file.

The wheel file can be installed using the following:

.. code-block:: bash
    :caption: Install version 1.0.0 directly from the ``whl`` file.
    :name: download-whl-from-the-release-page

    $ pip install simulator_automatic_warehouse-1.0.0-py3-none-any.whl


-----------------
Build the project
-----------------

To build the project we need to install a `build backend <https://packaging.python.org/en/latest/glossary/#term-Build-Backend>`_.
The Simulator Automatic Warehouse uses `Hatch <https://hatch.pypa.io/1.12/>`_ to do this.
So the first thing you need to do is install it on your system:

.. code-block:: bash

    $ pip install hatch

Now clone the Simulator Automatic Warehouse repository using git (or any other method you like):

.. code-block:: bash

    $ git clone https://github.com/AndreVale69/simulator-automatic-warehouse.git

Go to the repository folder you just cloned and build the project using hatch:

.. code-block:: bash

    $ cd simulator-automatic-warehouse
    $ hatch build

When the build is complete, you should see a new folder called ``dist``.
Inside are two files, and we are interested in the one with the ``.whl`` extension.
It can be installed using ``pip``:

.. code-block:: bash
   :caption: We assume that the version just built is the 1.0.0

    $ cd dist
    $ pip install simulator_automatic_warehouse-1.0.0-py3-none-any.whl


-------------------------
Create and use a ``venv``
-------------------------

Create and use a venv
