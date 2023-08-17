"""Test the packages settings validation."""
from ou_container_builder.settings import Packages


def test_valid_packages_settings():
    """Test that a valid packages configuration passes."""
    Packages(apt=["curl"], pip=["jupyterlab"])


def test_default_sources_settings():
    """Test that the default sources settings are correct."""
    settings = Packages()
    assert settings.apt == []
    assert settings.pip == []
