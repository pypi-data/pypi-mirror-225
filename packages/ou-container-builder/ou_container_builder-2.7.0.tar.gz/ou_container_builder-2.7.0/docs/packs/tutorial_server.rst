``tutorial_server`` pack - Tutorial Server
==========================================

The ``tutorial_server`` pack installs and enables the `Tutorial Server <https://pypi.org/project/tutorial-server/>`_

.. code:: yaml

    packs:
      - name: tutorial_server
        options:
          parts:
            - name:       # The name of this part.
              type:       # The type of part this is.
              path:       # The path on the filesystem where the files are stored.
          default:        # The default part to load.
          php_cgi:  # Whether to enable the PHP CGI support

The tutorial server pack configures the Tutorial Server and supports the following options:

* ``parts``: Configures the different parts of the content served by the Tutorial Server. Consists of a list, where
  each entry must have the following three keys:

  * ``name``: The name of the part. This is used to generate the URL, thus all values must be valid within a URL.
  * ``type``: The following values are supported for the type of part

    * ``tutorial``: Static web content that is served as is.
    * ``workspace``: Direct file access, supports GET and PUT requests to fetch the file content and update the file
      content.
    * ``live``: Read-only access to the files. If they are PHP files and ``php-cgi`` is set to ``true``, then they will
      automatically be run via ``php-cgi``

  * ``path``: The path on the filesystem where the files accessed via this part are stored. The path is processed
    relative to the user's home directory.

* ``default``: The ``name`` of the default part to load
* ``php_cgi`` [optional]: Whether to enable the PHP CGI support in the Tutorial Server. The PHP CGI mode allows for running PHP scripts
  from within the Tutorial Server. Defaults to ``false``.
