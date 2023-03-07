"""Exporter module."""

import logging
import platform
import socket
import subprocess
from typing import Dict, List

from fastapi import HTTPException

logger = logging.getLogger(__name__)


def generate_hostname_output() -> str:
    """Generate hostname output."""
    try:
        return socket.gethostname()
    except Exception as error:
        logger.error("Failed to get hostname %s", error)
        raise HTTPException(status_code=500, detail="Server error")


def generate_kernel_output() -> Dict:
    """Generate kernel version output."""
    return {"kernel": platform.release()}


def generate_dpkg_output() -> List[Dict]:
    """Generate Debian package output."""
    cmd = "dpkg -l"
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
        raise HTTPException(status_code=500, detail="Server error")

    except subprocess.CalledProcessError as error:
        logger.error("CalledProcessError to list dpkg: %s", error)
        raise HTTPException(status_code=500, detail="Server error")

    except ValueError as error:
        logger.error("ValueError to list dpkg: %s", error)
        raise HTTPException(status_code=500, detail="Server error")


def generate_snap_output() -> List[Dict]:
    """Generate snap output."""
    cmd = "snap list"
    try:
        snaps = str(subprocess.check_output(cmd.split(), timeout=10))
        lines = snaps.split("\\n")
        lines = lines[1:-1]
        output = []
        for line in lines:
            snap, version, revision, tracking, *_ = line.split()
            output.append(
                {
                    "snap": snap,
                    "version": version,
                    "revision": revision,
                    "tracking": tracking,
                }
            )
        return output
    except subprocess.TimeoutExpired as error:
        logger.error("Timeout to list snap %s", error)
        raise HTTPException(status_code=500, detail="Server error")

    except subprocess.CalledProcessError as error:
        logger.error("CalledProcessError to list snap: %s", error)
        raise HTTPException(status_code=500, detail="Server error")

    except ValueError as error:
        logger.error("ValueError to list snap: %s", error)
        raise HTTPException(status_code=500, detail="Server error")
