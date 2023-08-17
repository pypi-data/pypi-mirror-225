``code_server`` pack - Code-Server interface
============================================

The ``code_server`` pack installs and enables the `Code Server <https://github.com/coder/code-server>`_ interface (v4.5).

To enable the pack, add it to the ``packs`` key as follows:

.. code:: yaml

    packs:
      - name: code_server
        options:
          version:     # The version to install
          extensions:  # A list of extensions to install

The Code-Server installation is configured using the ``options`` key, with the following options available:

* ``version``: The version to install. If not specified a default is provided that is updated periodically.
* ``extensions``: A list of extensions to install
