``server`` key - Configuring server settings
============================================

The ``server`` key is used to specify how the Jupyter Server inside the container is run. It uses the
following structure:

.. code:: yaml

    server:
      default_path:  # The default path to open
      access_token:  # The fixed access token to use for limiting access
      wrapper_host:  # The host that will wrapp the container

The keys are all optional.

* ``default_path``: The ``default_path`` specifies the default path that is loaded when the user runs the container.
* ``access_token``: By default the Jupyter Server generates a random access token and shows this on the command-line when launching
  the container. Set the ``access_token`` key if you wish to specify a fixed access token.
* ``wrapper_host``: By default the Jupyter Server does not allow for the interface to be displayed inside an ``<iframe>``. If you
  wish to display the interface inside an ``<iframe>``, then set the ``wrapper_host`` to the host that hosts the
  ``<iframe>``.

Default Settings
----------------

The default settings are as follows:

.. code:: yaml

    server:
      default_path: '/'

Example
-------

.. code:: yaml

    server:
      default_path: /custom
      access_token: let-me-in
      wrapper_host: hosting.example.com
