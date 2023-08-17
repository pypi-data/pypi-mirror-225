``services`` key - Enable system services
=========================================

To automatically start services when the container starts, specify the services to start under the top-level
``services`` key:

.. code:: yaml

    services:
      - service_name  # The name of the service to start and stop

* ``service_name``: The name of the service to start. This must be startable using the ``/usr/sbin/service`` command
  on a Debian system.

The services are started after all :doc:`startup scripts <scripts>` are executed and the OU Container Builder
automatically ensures that the user has the required permissions to do so.

Example
-------

.. code:: yaml

    services:
      - mariadb
