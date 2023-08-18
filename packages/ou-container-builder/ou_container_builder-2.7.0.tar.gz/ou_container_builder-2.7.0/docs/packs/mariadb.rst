``mariadb`` pack - Mariadb Database
===================================

The ``mariadb`` pack installs and enables the MariaDB server. It configures the MariaDB server so that the
database is persistet via the user's home directory.

To enable the pack, add it to the ``packs`` key as follows:

.. code:: yaml

    packs:
      - name: mariadb
        options:
          database:  # Name of the database to create
          username:  # Name of the user to use for db access
          password:  # Password for the user to use for db access

The MariaDB installation is configured using the ``options`` key, with the following options available:

* ``database``: The name of the database to automatically generate if it does not exist.
* ``username``: The name of the user to use for accessing the configured database.
* ``password``: The password to use for authenticating access to the database.
