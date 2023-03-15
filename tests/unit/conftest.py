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
def snapd_snaps():
    return {
        "type": "sync",
        "status-code": 200,
        "status": "OK",
        "result": [
            {
                "id": "pHxyR7qwIBt0ZMMxMLbhal5V6b0cI3jE",
                "title": "CVEScan",
                "summary": "Security/CVE vulnerability monitoring for Ubuntu",
                "description": "Check whether all available security patches have been installed.",
                "installed-size": 43163648,
                "name": "cvescan",
                "publisher": {
                    "id": "canonical",
                    "username": "canonical",
                    "display-name": "Canonical",
                    "validation": "verified",
                },
                "developer": "canonical",
                "status": "active",
                "type": "app",
                "base": "core18",
                "version": "2.5.0",
                "channel": "stable",
                "tracking-channel": "latest/stable",
                "ignore-validation": False,
                "revision": "281",
                "confinement": "strict",
                "private": False,
                "devmode": False,
                "jailmode": False,
                "apps": [
                    {"snap": "cvescan", "name": "cvescan"},
                    {"snap": "cvescan", "name": "sh"},
                ],
                "license": "GPL-3.0",
                "mounted-from": "/var/lib/snapd/snaps/cvescan_281.snap",
                "links": {
                    "contact": ["https://github.com/canonical/sec-cvescan/issues"],
                    "website": ["https://github.com/canonical/sec-cvescan"],
                },
                "contact": "https://github.com/canonical/sec-cvescan/issues",
                "website": "https://github.com/canonical/sec-cvescan",
                "media": [
                    {
                        "type": "screenshot",
                        "url": "https://dashboard.snapcraft.io/appmedia/cvescan_demo.gif",
                        "width": 784,
                        "height": 688,
                    }
                ],
                "install-date": "2023-03-14T10:45:53.357333475-03:00",
            },
        ],
    }
