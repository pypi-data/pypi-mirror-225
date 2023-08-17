Building Containers
===================

The OU Container Builder is configured using the ``ContainerConfig.yaml`` :doc:`configuration file <configuration/index>`.

To then run the OU Container Builder use the following command in the same directory as your ``ContainerConfig.yaml`` file:

.. sourcecode:: console

    $ ou-container-builder

The ``ou-container-builder`` supports a range of command-line switches to configure the output:

* ``-b``, ``--build``: Automatically build the Docker image [Default behaviour].
* ``-c``, ``--context``: The context directory that contains the ``ContainerConfig.yaml`` [Default: .].
* ``--clean``: Clean all temporary files generated for the Docker build [Default behaviour].
* ``--help``: Show all available command-line switches.
* ``-nb``, ``--no-build``: Generate the Dockerfile, but do not build it. This implies ``--no-clean``.
* ``--no-clean``: Do not clean the temporary files generated for the Docker build.
* ``--tag {TAG}``: Tag the resulting Docker image with the given ``TAG``. This option can be provided multiple times
  to attach multiple tags.
