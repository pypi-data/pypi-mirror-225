``flags`` key - Flags
=====================

The flags are primarily used internally to indicate that that certain functionality is enabled in the container. These
should in general not be set when creating a container and may change in the future:

.. code:: yaml

    ou_container_content:  # Whether the OU Container Content is enabled

* ``ou_container_content``: Flag to indicate that the
  `OU Container Content <https://github.com/mmh352/ou-container-content>`_ is enabled and will be used to distribute
  content, run startup scripts, and start/stop services.
