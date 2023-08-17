"""Test the sources settings validation."""
from pydantic import ValidationError
from pytest import raises

from ou_container_builder.settings import WebApp, LauncherEntry

from .util import error_locations


def test_valid_web_app_settings():
    """Test that a valid sources configuration passes."""
    WebApp(
        path="/test", command="python -m http.server {port}", port=80, timeout=120, absolute_url=True, launcher_entry={}
    )


def test_default_web_app_settings():
    """Test that the default web_app settings are correct."""
    settings = WebApp(path="/test", command="python -m http.server {port}")
    assert settings.port == 0
    assert settings.timeout == 60
    assert settings.absolute_url is False
    assert settings.new_browser_tab is False
    assert settings.environment == {}
    assert settings.request_headers_override == {}
    assert settings.launcher_entry.enabled is True


def test_valid_launcher_entry_settings():
    """Test that a valid launcher entry configuration passes."""
    settings = LauncherEntry(enabled=False, icon_path="/var/lib/test.svg", title="Test")
    assert settings.enabled is False


def test_default_launcher_entry_settings():
    """Test that the default launcher entry settings are correct."""
    settings = LauncherEntry()
    assert settings.enabled is True
    assert settings.icon_path == ""
    assert settings.title == ""
