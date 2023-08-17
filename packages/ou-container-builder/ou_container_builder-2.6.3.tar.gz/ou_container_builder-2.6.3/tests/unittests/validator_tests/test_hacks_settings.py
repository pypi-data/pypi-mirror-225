"""Test the image settings validation."""
from pydantic import ValidationError
from pytest import raises

from ou_container_builder.settings import Settings

from .util import error_locations


def test_fail_invalid_hack():
    """Test that an invalid hack fails."""
    with raises(ValidationError) as e_info:
        Settings(hacks=["fail"])
    assert ("hacks", 0) in error_locations(e_info.value)
