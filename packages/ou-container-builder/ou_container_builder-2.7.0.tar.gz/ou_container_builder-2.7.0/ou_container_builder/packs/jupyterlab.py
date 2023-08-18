"""Pack to install the Jupyterlab interface."""
from jinja2 import Environment
from pydantic import BaseModel
from typing import Literal
from warnings import warn

from ou_container_builder.utils import merge_settings


class Options(BaseModel):
    version: Literal[3] | Literal[4] = 3


class Pack(BaseModel):
    name: Literal["jupyterlab"]
    options: Options = Options()


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
        "Automatically setting JupyterLab as the default is deprecated in 2.2.0 and will be removed in 3.0.0. Instead set server.default_path explicitly.",
        FutureWarning,
    )
    if pack_settings["version"] == 3:
        settings = merge_settings(
            settings,
            {
                "packages": {"pip": ["jupyterlab>=3.4.3,<4.0.0"]},
            },
        )
    elif pack_settings["version"] == 4:
        settings = merge_settings(
            settings,
            {
                "packages": {"pip": ["jupyterlab>=4.0.2,<5.0.0"]},
            },
        )
    settings = merge_settings(
        settings,
        {
            "server": {"default_path": "/lab"},
        },
    )
    return settings


def generate_files(context: str, env: Environment, settings: dict, pack_settings: dict) -> None:
    """Generate the build files for the jupyterlab pack.

    This ensures that the the jupyterlab package is installed

    :param context: The context path within which the generation is running
    :type context: str
    :param env: The Jinja2 environment to use for loading and rendering templates
    :type env: :class:`~jinja2.environment.Environment`
    :param settings: The validated settings
    :type settings: dict
    :param pack_settings: The validated pack-specific settings
    :type settings: dict
    """
    pass
