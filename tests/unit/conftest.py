"""Conftest module for unit tests."""
import pytest


def read_file(path: str):
    """Read the content of a file."""
    with open(path, encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def list_dpkg():
    """Equivalent of the output of 'dpkg -l' command."""
    return read_file("tests/unit/resources/dpkg.txt")


@pytest.fixture
def list_snap():
    """Equivalent of the output of 'snap list' command."""
    return read_file("tests/unit/resources/snap.txt")
