"""Pack to handle setting up jupyter_server."""
import json
import os.path

from jinja2 import Environment

from ou_container_builder.utils import merge_settings


def process_settings(settings: dict) -> dict:
    """Process the jupyter_server core settings.

    :param settings: The settings parsed from the configuration file
    :type settings: dict
    :return: The updated settings
    :rtype: dict
    """
    settings = merge_settings(
        settings,
        {
            "packages": {"apt": ["sudo"], "pip": ["jupyter_server<4.0.0", "jupyterhub>=3.0.0,<4"]},
            "content": [
                {
                    "source": "ou-builder-build/ou_core_config.json",
                    "target": "/usr/local/etc/jupyter/jupyter_server_config.json",
                    "overwrite": "always",
                }
            ],
            "jupyter_server_config": {
                "ServerApp": {
                    "ip": "0.0.0.0",
                    "port": 8888,
                    "quit_button": False,
                    "trust_xheaders": True,
                    "iopub_data_rate_limit": 10000000,
                },
                "NotebookApp": {"quit_button": False},
            },
        },
    )
    if "access_token" in settings["server"] and settings["server"]["access_token"]:
        settings = merge_settings(
            settings, {"jupyter_server_config": {"ServerApp": {"token": settings["server"]["access_token"]}}}
        )
    if "wrapper_host" in settings["server"] and settings["server"]["wrapper_host"]:
        settings = merge_settings(
            settings,
            {
                "jupyter_server_config": {
                    "ServerApp": {
                        "tornado_settings": {
                            "headers": {
                                "Content-Security-Policy": f"frame-ancestors 'self' {settings['server']['wrapper_host']}",
                                "Access-Control-Allow-Origin": f'{settings["server"]["wrapper_host"]}',
                            }
                        }
                    }
                }
            },
        )
    return settings


def generate_files(context: str, env: Environment, settings: dict, user_settings) -> dict:
    """Generate the build files the jupyter_server core.

    :param context: The context path within which the generation is running
    :type context: str
    :param env: The Jinja2 environment to use for loading and rendering templates
    :type env: :class:`~jinja2.environment.Environment`
    :param settings: The validated settings
    :type settings: dict
    """
    if "server" in user_settings and "default_path" in user_settings["server"]:
        settings = merge_settings(
            settings, {"jupyter_server_config": {"ServerApp": {"default_url": user_settings["server"]["default_path"]}}}
        )
    with open(os.path.join(context, "ou-builder-build", "ou_core_config.json"), "w") as out_f:
        json.dump(settings["jupyter_server_config"], out_f)
