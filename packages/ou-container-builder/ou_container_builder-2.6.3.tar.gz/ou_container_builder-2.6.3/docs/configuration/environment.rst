``environment`` key - Set environment variables
===============================================

The ``environment`` key can be used to add environment variables. It is structured as follows:

.. code:: yaml

    environment:
      - name:     # Name of the environment variable
        value:    # Value of the environment variable

Multiple ``name / value`` pairs can be used to specify multiple environment variables. The environment variables are
set for both build time and when the container is run.

* ``name`` - the name of the environment variable to set
* ``value`` - the value of the environment variable to set. This **must** be a string

Example
-------

.. code:: yaml

    environment:
      - name: LICENSE
        value: MIT
      - name: VERSION
        value: "1.0.0"
      - name: DEBUG
        value: "true"
