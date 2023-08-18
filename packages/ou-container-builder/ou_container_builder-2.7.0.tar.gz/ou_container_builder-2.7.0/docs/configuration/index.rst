Configuration File
==================

The OU Container Builder uses a YAML configuration file to define what is included in the final Docker image. The Builder
requires that this file is called ``ContainerConfig.yaml``.

At the top level, the ``ContainerConfig.yaml`` file can contain the following keys:

.. code:: yaml

    module:
    image:
    content:
    packs:
    server:
    sources:
    packages:
    environment:
    web_apps:
    scripts:
    services:
    jupyter_server_config:
    hacks:
    flags:

.. toctree::
    :maxdepth: 1
    :titlesonly:

    module
    image
    content
    packs
    server
    sources
    packages
    environment
    web_apps
    scripts
    services
    jupyter_server_config
    hacks
    flags
