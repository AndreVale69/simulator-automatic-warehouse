
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

.. _build-the-project:

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

Once the package is installed, you can remove the repository from your local computer and uninstall Hatch.


-------------------------
Create and use a ``venv``
-------------------------

The following steps can also be applied to the previous section (:ref:`build-the-project`).
It's always recommended to use a virtual environment.

1. First, we create a virtual environment using the command:

   .. code-block:: bash

       $ python3 -m venv ~/.virtualenvs/choose-a-name-for-your-venv

   .. note::

       On Windows, invoke the venv command as follows:

       .. code-block::

           c:\>Python35\python -m venv c:\path\to\myenv

       Alternatively, if you configured the PATH and PATHEXT variables for your Python installation:

       .. code-block::

           c:\>python -m venv c:\path\to\myenv

2. Then, we activate the virtual environment:

   .. code-block:: bash

       $ source ~/.virtualenvs/choose-a-name-for-your-venv/bin/activate

   .. note::

       On Windows, see the following chapter in the
       `Python documentation <https://docs.python.org/3/library/venv.html#how-venvs-work>`_.

3. Once the venv is enabled, you can easily install the package using pip and PyPI (:ref:`pypi` section).

3. If you want to contribute to the project and set up the environment, read on.

   Download the repository using git clone:

   .. code-block:: bash

       $ git clone https://github.com/AndreVale69/simulator-automatic-warehouse.git

4. Go to the repository and install the dependencies of the project.
   The Simulator Automatic Warehouse uses 4 main packages: ``pandas``, ``simpy``, ``PyYAML``, ``jsonschema``.
   See the :ref:`dependencies` section for more information.

   The packages and their required versions can be found in the ``requirements.txt`` file.
   Use the following command to install them:

   .. code-block:: bash

       $ pip install -r requirements.txt

5. Once the dependencies are installed, you are in! You are ready to run the simulator and the digital twin.
   At this stage, **it's a good idea to run the tests and check that everything works**.

   The tests have the ``pytest`` package dependencies.
   The versions and packages to install can be found in ``tests/test-requirements.txt``.
   Then we can simply install them with the command:

   .. code-block:: bash

       $ pip install -r tests/test-requirements.txt

6. Finally, once the pytest dependencies have been successfully installed, run the tests with the command:

   .. code-block:: bash
      :caption: Make sure you are in the project home, not the tests folder.

       $ PYTHONPATH=. pytest --config-file='tests/pytest.ini'

   .. note::

       The project also provides a ``tests/tox.ini`` configuration. You can run it from
       the project root with:

       .. code-block:: bash

           $ tox -c tests/tox.ini

       Or, to run environments in parallel:

       .. code-block:: bash

           $ tox run-parallel -c tests/tox.ini

       These commands assume Python 3.9 through 3.14 are already installed on your system.

   .. note::

       On Windows, the ``PYTHONPATH`` in one line doesn't work.
       If you then open a PowerShell and go to the home of the project,
       you can export the ``PYTHONPATH`` environment variable using the
       `Get-Location <https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-location>`_
       command:

       .. code-block:: bash

           $env:PYTHONPATH=Get-Location
           pytest --config-file='tests/pytest.ini'
