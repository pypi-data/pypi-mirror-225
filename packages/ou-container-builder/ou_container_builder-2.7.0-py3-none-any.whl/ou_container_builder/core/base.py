"""Pack to handle setting up the base settings.

This provides a few minimal initial settings.
"""
from jinja2 import Environment

from ou_container_builder.utils import merge_settings


def process_settings(settings: dict) -> dict:
    """Process the content core settings.

    :param settings: The settings parsed from the configuration file
    :type settings: dict
    :return: The updated settings
    :rtype: dict
    """
    settings = merge_settings(
        {
            "packages": {
                "apt": ["libcurl3-gnutls", "libcurl3-gnutls-dev", "gnutls-dev", "gcc", "build-essential"],
                "pip": ["pycurl"],
            }
        },
        settings,
    )
    return settings


def generate_files(context: str, env: Environment, settings: dict) -> None:
    """Generate the build files for the base core.

    :param context: The context path within which the generation is running
    :type context: str
    :param env: The Jinja2 environment to use for loading and rendering templates
    :type env: :class:`~jinja2.environment.Environment`
    :param settings: The validated settings
    :type settings: dict
    """
    pass
