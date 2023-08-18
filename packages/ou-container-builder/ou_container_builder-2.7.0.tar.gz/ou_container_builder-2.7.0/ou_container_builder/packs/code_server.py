"""Pack to install the Code Server interface."""
import os
from importlib import resources
from pydantic import BaseModel
from typing import Literal
from warnings import warn

from jinja2 import Environment

from ou_container_builder.utils import merge_settings


class Options(BaseModel):
    version: str = "4.14.1"
    extensions: list[str] = []


class Pack(BaseModel):
    name: Literal["code_server"]
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
    version = pack_settings["version"]
    warn(
        "Automatically setting the code_server as the default web-app is deprecated in 2.2.0 and will be removed in 3.0.0. Instead set server.default_path explicitly.",
        FutureWarning,
    )
    settings = merge_settings(
        settings,
        {
            "sources": {
                "apt": [
                    {
                        "name": "nodesource",
                        "key_url": "https://deb.nodesource.com/gpgkey/nodesource.gpg.key",
                        "dearmor": True,
                        "deb": {
                            "url": "https://deb.nodesource.com/node_18.x",
                            "distribution": "bullseye",
                            "component": "main",
                        },
                    }
                ],
            },
            "packages": {
                "apt": ["nodejs", "yarn"],
            },
            "scripts": {
                "build": [
                    {
                        "commands": [
                            "cd /opt",
                            f"curl -L --output code-server.tar.gz https://github.com/coder/code-server/releases/download/v{version}/code-server-{version}-linux-amd64.tar.gz",  # noqa: E501
                            "tar -zxvf code-server.tar.gz",
                            f"ln -s /opt/code-server-{version}-linux-amd64/bin/code-server /usr/local/bin",
                        ]
                    }
                ]
            },
            "content": [
                {
                    "source": "ou-builder-build/packs/code_server/logo.svg",
                    "target": "/var/lib/code_server/logo.svg",
                    "overwrite": "always",
                },
            ],
            "web_apps": [
                {
                    "path": "code-server/",
                    "command": [
                        "code-server",
                        "--auth",
                        "none",
                        "--disable-update-check",
                        "--bind-addr",
                        "0.0.0.0",
                        "--port",
                        "{port}",
                    ],
                    "timeout": 60,
                    "default": True,
                    "new_browser_tab": False,
                    "launcher_entry": {"title": "VS Code", "icon_path": "/var/lib/code_server/logo.svg"},
                }
            ],
        },
    )
    if len(pack_settings["extensions"]) > 0:
        settings = merge_settings(
            settings,
            {
                "scripts": {
                    "build": [
                        {
                            "commands": [
                                f"code-server --install-extension {extension}"
                                for extension in pack_settings["extensions"]
                            ]
                        }
                    ]
                }
            },
        )
    return settings


def generate_files(context: str, env: Environment, settings: dict, pack_settings: dict) -> None:
    """Generate the build files for the code-server pack.

    This ensures that the the code-server is installed

    :param context: The context path within which the generation is running
    :type context: str
    :param env: The Jinja2 environment to use for loading and rendering templates
    :type env: :class:`~jinja2.environment.Environment`
    :param settings: The validated settings
    :type settings: dict
    :param pack_settings: The validated pack-specific settings
    :type settings: dict
    """
    source = resources.files("ou_container_builder") / "templates" / "packs" / "code_server" / "vscode.svg"
    target_path = os.path.join(context, "ou-builder-build", "packs", "code_server", "logo.svg")
    if not os.path.exists(os.path.dirname(target_path)):
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with resources.as_file(source) as in_path:
        with open(in_path, "rb") as in_f:
            with open(target_path, "wb") as out_f:
                out_f.write(in_f.read())
