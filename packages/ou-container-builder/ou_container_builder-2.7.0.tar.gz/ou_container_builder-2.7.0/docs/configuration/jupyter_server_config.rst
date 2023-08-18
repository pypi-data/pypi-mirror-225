``jupyter_server_config`` key - Additional Jupyter Server settings
==================================================================

The ``jupyter_server_config`` key can be used to pass arbitrary configuration settings directly to the
`Jupyter Server Configuration <https://jupyter-server.readthedocs.io/en/latest/users/configuration.html>`_.

.. code:: yaml

    jupyter_server_config:  # Jupyter Server Configuration settings

* ``jupyter_server_config``: This is a dictionary that will be saved as is to the Jupyter Server configuration. Any setting
  that is valid for the Jupyter Server can be specified here.
