``content`` key - Distributing content with the container
=========================================================

The OU Container Builder supports distributing module content to the user using the
`OU Container Content <https://github.com/mmh352/ou-container-content>`_. The content to distribute is configured
using the top-level ``content`` key, which contains a list with the following three keys for each list item:

.. code:: yaml

  content:
    - source:     # The source directory or file to copy into the container
      target:     # The target directory or file to copy to in the container
      overwrite:  # Whether newer files should overwrite older files

* ``source``: The path to the source directory or file to copy into the container. If an absolute path is given, then
  this is used as-is. A relative path is interpreted relative to the location of the configuration file.
* ``target``: The name of the directory or file in the container. Only a single directory or filename is supported, no
  paths. If an absolute path is given, then this is used as-is. A relative path is interpreted relative to the user's
  home directory.
* ``overwrite``: As some content should always be kept up-to-date, while other content is there as a starting point and
  can be modified by the user, after which it should not be updated anymore, the distribution functionality has
  multiple overwrite modes:

  * *always*: Content with this setting will always be overwritten with the content distributed with the container.
  * *never*: Content with this setting will never be overwritten with the content distributed with the container.
  * *if-unchanged*: Content with this setting will be overwritten, but only if the user has not modified it.

  .. note::

      This setting will be ignored if the ``target`` is an absolute path, in which case the target is always
      overwritten.

Distribution targets
--------------------

Files can be distributed both to the user's home directory at run-time and to an absolute location at build time.

Distributing files to the user's home directory
+++++++++++++++++++++++++++++++++++++++++++++++

Files are distributed to the user's home directory when the container starts. The reason for this is that if the
container is run via Kubernetes, files in the user's home directory in the image are not automatically copied into
the persistent volume. Thus the distribution can only happen after the container is started and the persistent
volume attached.

To distribute to the user's home directory, the ``target`` **must** be a relative path. The ``source`` can be a
relative or absolute path. In either case distribution happens at startup.

The user can always delete part or all of the content in their home directory and in that case when the container
starts the next time, the deleted content will automatically be replaced with the latest content.

.. note::

    If you remove content that had previously been distributed to users, this content will **not** be removed
    automatically from the user's home directory.

Distributing files to an absolute location
++++++++++++++++++++++++++++++++++++++++++

If the ``target`` is provided as an absolute path, then the files from the ``source`` are distributed to that path
when the container is built. This is often used to distribute configuration files. In this case the ``overwrite``
setting is ignored and the files are always copied.

Default Settings
----------------

By default no content is distributed with the container.

Examples
--------

.. code:: yaml

    content:
      - source: content
        target: notebooks
        overwrite: if-unchanged
      - source: data
        target: data
        overwrite: always

.. code:: yaml

    content:
      - source: config.ini
        target: /var/lib/app/config.ini
        overwrite: always
