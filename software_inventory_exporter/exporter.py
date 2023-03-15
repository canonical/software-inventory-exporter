"""Exporter module."""

import logging
import platform
import socket
import subprocess
from typing import Dict, List

import requests
from fastapi import HTTPException

from software_inventory_exporter.snapd import SnapdAdapter

logger = logging.getLogger(__name__)


def generate_hostname_output() -> str:
    """Generate hostname output."""
    try:
        return socket.gethostname()
    except Exception as error:
        logger.error("Failed to get hostname %s", error)
        raise HTTPException(status_code=500, detail="Server error") from error


def generate_kernel_output() -> Dict:
    """Generate kernel version output."""
    return {"kernel": platform.release()}


def generate_dpkg_output() -> List[Dict]:
    """Generate Debian package output.

    The first 5 lines of the output are headers. The expected format
    can be found at `resources` in the unit tests.
    """
    cmd = "dpkg -l --admindir=/var/lib/snapd/hostfs/var/lib/dpkg"
    try:
        dpkg = str(subprocess.check_output(cmd.split(), timeout=10))
        lines = dpkg.split("\\n")
        lines = lines[5:-1]
        output = []
        for line in lines:
            _, package, version, *_ = line.split()
            output.append(
                {
                    "package": package,
                    "version": version,
                }
            )
        return output

    except subprocess.TimeoutExpired as error:
        logger.error("Timeout to list dpkg %s", error)
        raise HTTPException(status_code=500, detail="Server error") from error

    except subprocess.CalledProcessError as error:
        logger.error("CalledProcessError to list dpkg: %s", error)
        raise HTTPException(status_code=500, detail="Server error") from error

    except ValueError as error:
        logger.error("ValueError to list dpkg: %s", error)
        raise HTTPException(status_code=500, detail="Server error") from error


def generate_snap_output() -> List[Dict]:
    """Generate snap output.

    Use the snapd-api to list all installed snaps in the machine.
    See more information at https://snapcraft.io/docs/snapd-api
    """
    try:
        session = requests.Session()
        session.mount("http://snapd/", SnapdAdapter())
        response = session.get("http://snapd/v2/snaps", timeout=10)
        response.raise_for_status()
        return response.json()["result"]
    except requests.exceptions.RequestException as error:
        logger.error("Error to list snap %s", error)
        raise HTTPException(status_code=500, detail="Server error") from error
    except KeyError as error:
        logger.error("Error to list snap %s", error)
        raise HTTPException(status_code=500, detail="Server error") from error
