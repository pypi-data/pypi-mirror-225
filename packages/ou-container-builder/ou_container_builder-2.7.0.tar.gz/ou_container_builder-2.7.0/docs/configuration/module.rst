``module`` key - Required module settings
=========================================

.. important::

    The ``module:`` key is the only required key in the ``ContainerConfig.yaml`` and provides module-level meta-data.

The module meta-data is used to create the internal directory structure within which the container files are made
available to the user. This ensures that when the user runs containers for multiple modules, they do not overwrite
each other's files. The module metadata consists of two values:

.. code:: yaml

    module:
      code:          # The module code
      presentation:  # The module presentation

Both values **must** be provided as strings and in the container are concatenated ``code-presentation``.

Example
-------

.. code:: yaml

    module:
      code: DemoModule
      presentation: "1"
