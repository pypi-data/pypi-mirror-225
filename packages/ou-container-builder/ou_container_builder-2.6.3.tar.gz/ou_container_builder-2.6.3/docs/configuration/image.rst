``image`` key - Base docker image settings
==========================================

The ``image`` key is used to specify the base docker image and user name to use when building the container.
It is structured as following:

.. code:: yaml

    image:
      base:  # docker image tag
      user:  # user name

The keys are all optional.

* ``base``: The ``base`` key specifies the base docker image to use when building the container image. The base image must
  be specified using the standard docker format.
* ``user``: The ``user`` key specifies the name of the user to use for running all processes in the container.

Default Settings
----------------

The default settings are as follows:

.. code:: yaml

    image:
      base: python:3.10-bullseye
      user: ou
