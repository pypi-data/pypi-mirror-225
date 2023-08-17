"""Test the sources settings validation."""
from ou_container_builder.settings import Script, Scripts


def test_valid_script_settings():
    """Test that a valid scripts configuration passes."""
    Scripts(build=[{"commands": ["test"]}], startup=[], shutdown=[])


def test_default_sources_settings():
    """Test that the default sources settings are correct."""
    settings = Scripts()
    assert settings.build == []
    assert settings.startup == []
    assert settings.shutdown == []


def test_valid_script_settings():
    """Test that a valid script configuration passes."""
    Script(commands=["test"])


def test_script_string_conversion():
    """Test that the string to script conversion works."""
    settings = Script(commands="test")
    assert settings.commands == ["test"]


def test_script_multiline_string_conversion():
    """Test that the string to script conversion works."""
    settings = Script(
        commands='''test
echo "Hello World!"'''
    )
    assert settings.commands == ["test", 'echo "Hello World!"']
