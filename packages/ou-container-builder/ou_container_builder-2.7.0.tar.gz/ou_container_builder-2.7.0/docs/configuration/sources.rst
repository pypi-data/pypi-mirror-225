``sources`` key - Configuring additional sources
================================================

To add additional APT sources use the top-level ``sources`` key:

.. code:: yaml

    sources:
      apt:
        - name:            # Name of the repository
          key_url:         # The URL to fetch the repository's signing key from
          dearmor:         # Whether to remove a
          deb:
            url:           # The URL of the repository
            distribution:  # The distribution within the repository
            component:     # The component within the distribution

* ``name``: The name of the repository. Is used to generate the filenames that the ``key`` and ``deb`` entries are
  stored in.
* ``key_url``: The URL from which to fetch the repository's signing key. This will be stored in a file called
  ``/etc/apt/trusted.gpg.d/{name}.gpg``.
* ``dearmor``: Whether to run dearmor to remove any PGP armor. Defaults to `True`
* ``deb``: The entry of the repository's source file. This specifies where the packages for this additional repository
  are fetched from. This value will be stored in a file called ``/etc/apt/sources.list.d/{name}.list``. It has the following
  keys:

  * ``url``: The URL of the repository
  * ``distribution``: The distribution to install and use within the repository
  * ``component``: The component(s) to use within the distribution

Multiple sources can be added by repeating creating more list items with the same three keys.

.. note::

    The sources are, obviously, added before the package installation, thus all packages provided by the new sources
    are available when installing :doc:`additional packages <packages>`.

Default Settings
----------------

By default no additional sources are configured.

Example
-------

.. code:: yaml

    sources:
      apt:
        - name: nodesource
          key_url: https://deb.nodesource.com/gpgkey/nodesource.gpg.key
          deb:
            url: https://deb.nodesource.com/node_18.x
            distribution: bullseye
            component: main
