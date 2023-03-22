"""Conftest module for unit tests."""
import json

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
def snapd_snaps():
    """Equivalent of the content of the file at /var/lib/snapd/state.json ."""
    snaps = {
        "data": {
            "snaps": {
                "core20": {
                    "type": "base",
                    "sequence": [
                        {
                            "name": "core20",
                            "snap-id": "DLqre5XGLbDqg9jPtiAhRRjDuPVa5X1q",
                            "revision": "1822",
                            "channel": "latest/stable",
                            "links": {"contact": ["https://github.com/snapcore/core20/issues"]},
                            "contact": "https://github.com/snapcore/core20/issues",
                            "title": "core20",
                            "summary": "Runtime environment based on Ubuntu 20.04",
                            "description": "The base snap based on the Ubuntu 20.04 release.",
                        },
                        {
                            "name": "core20",
                            "snap-id": "DLqre5XGLbDqg9jPtiAhRRjDuPVa5X1q",
                            "revision": "1828",
                            "channel": "latest/stable",
                            "links": {"contact": ["https://github.com/snapcore/core20/issues"]},
                            "contact": "https://github.com/snapcore/core20/issues",
                            "title": "core20",
                            "summary": "Runtime environment based on Ubuntu 20.04",
                            "description": "The base snap based on the Ubuntu 20.04 release.",
                        },
                    ],
                    "active": True,
                    "current": "1828",
                    "channel": "latest/stable",
                    "last-refresh-time": "2023-03-08T09:06:07.732371956-03:00",
                    "version": "20230207",
                },
            }
        }
    }
    return json.dumps(snaps)
