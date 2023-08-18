"""Pack to handle web_apps setups.

This simply sets the server's default_path, if a web application is set as the default.
"""
from copy import deepcopy
from warnings import warn

from jinja2 import Environment

from ou_container_builder.utils import merge_settings


def process_settings(settings: dict) -> dict:
    """Process the env core settings.

    :param settings: The settings parsed from the configuration file
    :type settings: dict
    :return: The updated settings
    :rtype: dict
    """
    if len(settings["web_apps"]) > 0:
        settings = merge_settings(settings, {"packages": {"pip": ["jupyter-server-proxy>=3.2.1,<4.0.0"]}})
    servers = {}
    for web_app in settings["web_apps"]:
        if "cmdline" in web_app:
            if "command" in web_app:
                warn(
                    "Both cmdline and command specified for a web_app. As cmdline is deprecated in 2.2.0, command takes preceence.",
                    FutureWarning,
                )
            else:
                warn(
                    "The cmdline setting for a web_app is deprecated in 2.2.0 and will be removed for version 3.0.0. Use command instead.",
                    FutureWarning,
                )
                web_app["command"] = web_app["cmdline"]
            del web_app["cmdline"]
        elif "command" not in web_app:
            warn("No command specified for the web_app")
        if "default" in web_app:
            warn(
                "The default setting in the web_app configuration is deprecated in 2.2.0 and will be removed in 3.0.0. Use server.default_path instead",
                FutureWarning,
            )
            if web_app["default"]:
                settings = merge_settings(settings, {"server": {"default_path": web_app["path"]}})
            del web_app["default"]
        path = web_app["path"]
        servers[path] = deepcopy(web_app)
        del servers[path]["path"]
    settings = merge_settings(settings, {"jupyter_server_config": {"ServerProxy": {"servers": servers}}})
    return settings


def generate_files(context: str, env: Environment, settings: dict) -> None:
    """Generate the build files for the web_apps core.

    :param context: The context path within which the generation is running
    :type context: str
    :param env: The Jinja2 environment to use for loading and rendering templates
    :type env: :class:`~jinja2.environment.Environment`
    :param settings: The validated settings
    :type settings: dict
    """
    pass
