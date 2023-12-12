"""Exporter module."""

import json
import logging
import lsb_release
import platform
import socket
import subprocess
from pathlib import Path
from typing import Dict, List

import yaml
from fastapi import HTTPException

logger = logging.getLogger(__name__)

SNAPD_STATE = "/var/lib/snapd/state.json"


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


def generate_release_output() -> Dict:
    """Generate kernel version output."""
    return {"release": lsb_release.get_distro_information()['CODENAME']}


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

    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, ValueError) as error:
        logger.error("Error generating dpkg output %s", error)
        raise HTTPException(status_code=500, detail="Server error") from error


def generate_snap_output() -> Dict:
    """Generate snap output by reading the snapd state."""
    try:
        snaps = json.loads(Path(SNAPD_STATE).read_text(encoding="UTF-8"))["data"]["snaps"]
        for snap in snaps.keys():
            snap_meta = yaml.safe_load(
                Path(f"/snap/{snap}/current/meta/snap.yaml").read_text(encoding="UTF-8")
            )
            snaps[snap]["version"] = snap_meta["version"]
        return snaps
    except (FileNotFoundError, ValueError, KeyError, yaml.YAMLError) as error:
        logger.error("Error generating snap output: %s", error)
        raise HTTPException(status_code=500, detail="Server error") from error
