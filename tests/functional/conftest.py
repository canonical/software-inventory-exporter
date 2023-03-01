"""Conftest module for functional tests."""
import logging
import os
import subprocess

import pytest
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


@pytest.fixture(scope="session", autouse=True)
def install_package():
    """Install the package to the system and cleanup afterwards.

    Depending on the environment variable TEST_SNAP,
    it will install the snap or the python package.
    """
    software_inventory_exporter_snap = os.environ.get("TEST_SNAP", None)
    if software_inventory_exporter_snap:
        # change directory to not import from local modules and force using the snap package
        cwd = os.getcwd()
        install_cmd = (
            f"sudo snap install --dangerous --classic {software_inventory_exporter_snap}".split()
        )
        os.chdir("/tmp")
        logging.info(f"Installing {software_inventory_exporter_snap}")
        assert os.path.isfile(software_inventory_exporter_snap)
        assert subprocess.check_call(install_cmd) == 0  # noqa
    else:
        logging.warning("Installing python package")
        assert subprocess.check_call("python3 -m pip install .".split()) == 0

    yield software_inventory_exporter_snap

    if software_inventory_exporter_snap:
        # return to the previous working directory
        os.chdir(cwd)
        logging.info("Removing snap package software-inventory-exporter")
        subprocess.check_call("sudo snap remove software-inventory-exporter".split())

    else:
        logging.info("Uninstalling python package software-inventory-exporter")
        subprocess.check_call("python3 -m pip uninstall --yes software-inventory-exporter".split())


@pytest.fixture(scope="session")
def session():
    """Create a session for requests."""
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session
