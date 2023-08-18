"""Pack to install the Nbclassic notebook interface."""
import os

from importlib import resources
from jinja2 import Environment
from pydantic import BaseModel
from typing import Literal
from warnings import warn

from ou_container_builder.utils import merge_settings


class Options(BaseModel):
    pass


class Pack(BaseModel):
    name: Literal["nbclassic"]
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
        "Automatically setting Nbclassic as the default is deprecated in 2.2.0 and will be removed in 3.0.0. Instead set server.default_path explicitly.",
        FutureWarning,
    )
    settings = merge_settings(
        settings,
        {
            "packages": {"pip": ["nbclassic>=0.4.8,<1.0.0"]},
            "server": {"default_path": "/tree"},
            "scripts": {
                "build": [
                    {"commands": ["pip uninstall -y notebook", "jupyter server extension enable --system nbclassic"]}
                ]
            },
            "content": [
                {
                    "source": "ou-builder-build/packs/nbclassic/custom",
                    "target": ".jupyter/custom",
                    "overwrite": "always",
                },
            ],
            "jupyter_server_config": {"NotebookApp": {"show_banner": False}},
        },
    )
    return settings


def generate_files(context: str, env: Environment, settings: dict, pack_settings: dict) -> dict:
    """Generate the build files for the nbclassic pack.

    This ensures that the the nbclassic package is installed

    :param context: The context path within which the generation is running
    :type context: str
    :param env: The Jinja2 environment to use for loading and rendering templates
    :type env: :class:`~jinja2.environment.Environment`
    :param settings: The validated settings
    :type settings: dict
    :param pack_settings: The validated pack-specific settings
    :type settings: dict
    """
    source = resources.files("ou_container_builder") / "templates" / "packs" / "nbclassic" / "custom.css"
    target_path = os.path.join(context, "ou-builder-build", "packs", "nbclassic", "custom", "custom.css")
    if not os.path.exists(os.path.dirname(target_path)):
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with resources.as_file(source) as in_path:
        with open(in_path, "rb") as in_f:
            with open(target_path, "wb") as out_f:
                out_f.write(in_f.read())
    source = resources.files("ou_container_builder") / "templates" / "packs" / "nbclassic" / "logo.svg"
    target_path = os.path.join(context, "ou-builder-build", "packs", "nbclassic", "custom", "logo.svg")
    if not os.path.exists(os.path.dirname(target_path)):
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with resources.as_file(source) as in_path:
        with open(in_path, "rb") as in_f:
            with open(target_path, "wb") as out_f:
                out_f.write(in_f.read())
