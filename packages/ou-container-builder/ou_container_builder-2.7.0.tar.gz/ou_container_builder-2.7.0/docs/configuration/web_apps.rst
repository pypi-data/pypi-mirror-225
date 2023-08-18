``web_apps`` key - Configure custom web applications
====================================================

The ``web_apps`` key makes it possible to configure arbitrary web applications that are then served via the
`Jupyter Server Proxy <https://jupyter-server-proxy.readthedocs.io/en/latest/>`_. They are structured as follows:

.. code:: yaml

    web_apps:
      - path:                      # The path at which the web application is hosted
        command:                   # The command to run the web application
        port:                      # The port the web application listens at
        timeout:                   # The timeout to wait for the web application to start
        absolute_url:              # Whether to forward the absolute url
        environment:               # Extra environment variables to set
        new_browser_tab:           # Whether the launcher should open this in a new browser tab
        request_headers_override:  # Additional headers to set on requests to the web application
        launcher_entry:            # Configuration for the launcher entry

Multiple web applications can be configured by providing multiple blocks. Only the ``path`` and ``cmdline`` keys are
required, all others are optional.

* ``path``: The path under which the web application is hosted. **Must** be an absolute path.
* ``command``: The command to run. This can either be a string, in which case it will be split using
  `shlex.split <https://docs.python.org/3/library/shlex.html>`, or a list. In either case the following to substitution
  variables can be used:

  * ``{port}`` is replaced with the random port the Jupyter proxy has selected for the web application.
  * ``{base_url}`` is replaced with the full path the application is hosted at. This will differ whether the container
    is run directly via Docker or via JupyterHub and this setting handles the distinction.

* ``port`` [optional]: The port the web application listens on. If unspecified, this defaults to 0, which means the
  Jupyter proxy will pick a random port (see above for substitution values for that random port).
* ``timeout`` [optional]: How long to wait for the application to start, before giving up.
* ``absolute_url`` [optional]: Whether to pass an absolute url or a relative url to the ``cmdline`` via the
  ``{base_url}`` substitution.
* ``environment`` [optional]: Additional environment variables to pass to the web application, specified as key-value
  pairs.
* ``new_browser_tab`` [optional]: Whether the launcher should open the web application in a new browser tab or in a
  JupyterLab tab. Only relevant when using JupyterLab.
* ``request_headers_override`` [optional]: Additional headers to add to the request sent to the web application.
* ``launcher_entry`` [optional]: Configuration for the launcher entry item, consists of the following three keys:

  * ``enabled``: Whether the launcher item is enabled. Defaults to ``true``.
  * ``icon_path`` [optional]: A file-path to an SVG icon that is shown in the launcher.
  * ``title`` [optional]: The title to show in the launcher entry. If not specified, uses the ``path`` setting.

.. deprecated:: 2.2.0

  The following keys have been deprecated and will be removed in 3.0.0:

  * ``cmdline``: This has been renamed to ``command``.
  * ``default``: Automatically setting the web application to be the default URL has been removed. Set the
    ``default_path`` in the :doc:`server settings <server>`.

Example
-------

.. code:: yaml

    web_apps:
      - path: /openrefine
        cmdline: /var/openrefine/openrefine-3.5.2/refine -i 0.0.0.0 -p "{port}" -d /home/ou-user/OpenRefine-21J
        timeout: 120
        default: true
