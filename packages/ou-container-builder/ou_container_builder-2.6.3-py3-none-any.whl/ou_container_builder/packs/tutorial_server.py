"""Pack to install the tutorial_sever."""
import os
from warnings import warn

from jinja2 import Environment
from pydantic import BaseModel
from typing import Literal

from ou_container_builder.utils import merge_settings, render_template


class Pack(BaseModel):
    name: Literal["tutorial_server"]
    options: dict = {}


def process_settings(settings: dict, pack_settings: dict) -> dict:
    """
    Process the user-provided settings.

    :param settings: The settings parsed from the configuration file
    :type settings: dict
    :param pack_settings: The pack-specific settings parsed from the configuration file
    :type settings: dict
    :return: The updated settings
    :rtype: dict
    """
    warn(
        "Automatically setting tutorial_server as the default is deprecated in 2.2.0 and will be removed in 3.0.0. Instead set server.default_path explicitly.",
        FutureWarning,
    )
    additional_settings = {
        "packages": {
            "pip": [
                "tutorial-server>=1.0.2,<2.0.0",
            ]
        },
        "content": [
            {
                "source": "ou-builder-build/tutorial-server/production.ini",
                "target": "/etc/tutorial-server/production.ini",
                "overwrite": "always",
            }
        ],
        "web_apps": [
            {
                "path": "/tutorial-server",
                "command": [
                    "python",
                    "-m",
                    "tutorial_server",
                    "--config=/etc/tutorial-server/production.ini",
                    "--port={port}",
                    "--basepath={base_url}tutorial-server/",
                ],
                "absolute_url": True,
                "default": True,
            }
        ],
    }
    if "php-cgi" in pack_settings and pack_settings["php-cgi"]:
        additional_settings["packages"]["apt"] = ["php-cgi"]
    settings = merge_settings(settings, additional_settings)
    return settings


def generate_files(context: str, env: Environment, settings: dict, pack_settings: dict) -> dict:
    """Generate the build files for the tutorial-server pack.

    Ensures that the Tutorial Server is installed and set up via the ``web_apps`` setting.

    :param context: The context path within which the generation is running
    :type context: str
    :param env: The Jinja2 environment to use for loading and rendering templates
    :type env: :class:`~jinja2.environment.Environment`
    :param settings: The validated settings
    :type settings: dict
    :param pack_settings: The validated pack-specific settings
    :type settings: dict
    """
    render_template(
        context,
        env,
        "packs/tutorial-server/production.ini",
        os.path.join("ou-builder-build", "tutorial-server", "production.ini"),
        dict(**settings, **pack_settings),
    )
