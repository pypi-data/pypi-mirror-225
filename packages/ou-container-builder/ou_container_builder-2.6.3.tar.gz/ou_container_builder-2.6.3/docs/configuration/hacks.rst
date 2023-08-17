``hacks`` key - Enable pre-configured hacks
===========================================

The OU Container Builder uses a minimal Debian-based base image (~100MB), to keep the final image size small. In general
this is not a problem, but some packages make assumptions about how things have been set up in a more common base image.
You should not enable any of these hacks unless you know that your setup fails because they are not enabled:

.. code:: yaml

    hacks:
      - missing-man1  # The /usr/share/man/man1 file is missing

* ``missing-man1``: Create the directory ``/usr/share/man/man1``. Some packages assume that this directory exists. Setting
  this hack creates the directory during the build process.

.. note::

    Where certain packages or settings are known to require a hack, then this is automatically activated.
