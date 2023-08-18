``scripts`` key - Specify custom scripts
========================================

The OU Container Builder supports running arbitrary scripts during build time and at container startup and shutdown.
These are configured under the top-level ``scripts`` key:

.. code:: yaml

    scripts:
      build:     # Scripts run during the build process
      startup:   # Scripts run at container startup
      shutdown:  # Scripts run at container shutdown

Build scripts are run from the Dockerfile using ``RUN`` commands. Startup and shutdown scripts are run when the
container is started and stopped.

Each script is configured using the following settings:

.. code:: yaml

    - commands:  # Commands to run in this script

* ``commands``: The commands to run for this script. This can either be provided using a list of commands:

  .. code:: yaml

      - commands:
        - touch /etc/notes.txt
        - rm /etc/notes.txt

  or as a block of commands:

  .. code:: yaml

      - commands: |
          touch /etc/notes.txt
          rm /etc/notes.txt


.. note::

    Startup scripts are run **before** any :doc:`services <services>` are started.

    Shutdown scripts are run **after** any :doc:`services <services>` are stopped.

Environment Variables
---------------------

The following environment variables are available for use in scripts:

* ``USER="ou"`` - the name of the user the container is run under
* ``UID="1000"`` - the id of the user the container is run under
* ``GID="100"`` - the group id the container is run under
* ``MODULE_CODE="$SETTING"`` - the module's code. Taken from the :doc:`base module settings <module>`.
* ``MODULE_PRESENTATION="$SETTING"`` - the module's presentatoon. Taken from the :doc:`base module settings <module>`.
* ``HOME="/home/$USER/$MODULE_CODE-$MODULE_PRESENTATION"``

Additionally, any environment variable specified via the :doc:`environment key <environment>` are available.

Example
-------

.. code:: yaml

    scripts:
      build:
        - commands: |
            wget --no-check-certificate https://github.com/OpenRefine/OpenRefine/releases/download/3.5.2/openrefine-linux-3.5.2.tar.gz
            mkdir /var/openrefine
            tar -xzf openrefine-linux-3.5.2.tar.gz --directory /var/openrefine
            rm openrefine-linux-3.5.2.tar.gz
