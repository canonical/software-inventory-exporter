"""API unit tests."""
import subprocess

import pytest
import requests
from fastapi.testclient import TestClient

from software_inventory_exporter import api, exporter

client = TestClient(api.app)


def test_hostname(mocker):
    """Test the hostname endpoint."""
    hostname = "juju-70b49f-3"
    mocker.patch.object(exporter.socket, "gethostname", return_value=hostname)
    response = client.get("/hostname")
    assert response.status_code == 200
    assert response.text == hostname


def test_hostname_error(mocker):
    """Test possible errors in the hostname endpoint."""
    mocker.patch.object(exporter.socket, "gethostname", side_effect=ValueError("some error"))
    response = client.get("/hostname")
    assert response.status_code == 500


def test_kernel(mocker):
    """Test the kernel endpoint."""
    mocker.patch.object(exporter.platform, "release", return_value="5.19.0-32-test")
    response = client.get("/kernel")
    assert response.status_code == 200
    assert response.json() == {"kernel": "5.19.0-32-test"}


def test_dpkg(mocker, list_dpkg):
    """Test the dpkg endpoint."""
    mocker.patch.object(exporter.subprocess, "check_output", return_value=list_dpkg)
    response = client.get("/dpkg")
    assert response.status_code == 200
    assert response.json() == [
        {"package": "accountsservice", "version": "22.07.5-2ubuntu1.3"},
        {"package": "acl", "version": "2.3.1-1"},
    ]


@pytest.mark.parametrize(
    "raise_error",
    [
        subprocess.TimeoutExpired(cmd=None, timeout=1),
        subprocess.CalledProcessError(cmd=None, returncode=1),
        ValueError,
    ],
)
def test_dpkg_error(mocker, raise_error):
    """Test possible errors in the dpkg endpoint."""
    mocker.patch.object(exporter.subprocess, "check_output", side_effect=raise_error)
    response = client.get("/dpkg")
    assert response.status_code == 500


def test_snap(mocker, snapd_snaps):
    """Test the snap endpoint."""
    mock_response = mocker.MagicMock()
    mock_response.json = mocker.MagicMock(return_value=snapd_snaps)
    mocker.patch.object(exporter.requests.Session, "get", return_value=mock_response)
    response = client.get("/snap")
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.parametrize(
    "raise_error",
    [
        requests.exceptions.RequestException,
        KeyError,
    ],
)
def test_snap_error(mocker, raise_error):
    """Test possible errors in the snap endpoint."""
    mocker.patch.object(exporter.requests.Session, "get", side_effect=raise_error)
    response = client.get("/snap")
    assert response.status_code == 500
