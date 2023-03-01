#!/usr/bin/env python3
"""Exporter module."""

import logging
import platform
import socket
import subprocess
import sys
from typing import Dict, List

import uvicorn
import yaml
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse

app = FastAPI(
    title="software-inventory-exporter",
    description="Exporter for apt packages and snaps in json via web.",
    license_info={
        "name": "GNU GENERAL PUBLIC LICENSE",
        "url": "https://www.gnu.org/licenses/gpl-3.0.en.html",
    },
)

logger = logging.getLogger(__name__)


@app.get("/hostname", response_class=PlainTextResponse)
def get_hostname() -> str:
    """Get the hostname of the machine."""
    try:
        return socket.gethostname()
    except Exception as error:
        logger.error("Failed to get hostname %s", error)
        raise HTTPException(status_code=500, detail="server error to get hostname")


@app.get("/kernel")
def get_kernel() -> Dict:
    """Get the kernel version of the machine."""
    return {"kernel": platform.release()}


@app.get("/dpkg")
def get_dpkg() -> List:
    """List the debian packages installed in the machine."""
    return generate_dpkg_output()


@app.get("/snap")
def get_snap() -> List:
    """List the snap packages installed in the machine."""
    return generate_snap_output()


def generate_dpkg_output() -> List:
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
        raise HTTPException(status_code=500, detail="Timeout error")

    except subprocess.CalledProcessError as error:
        logger.error("CalledProcessError to list dpkg: %s", error)
        raise HTTPException(status_code=500, detail="CalledProcessError")

    except ValueError as error:
        logger.error("ValueError to list dpkg: %s", error)
        raise HTTPException(status_code=500, detail="Server error")


def generate_snap_output() -> List:
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
        raise HTTPException(status_code=500, detail="Timeout error")

    except subprocess.CalledProcessError as error:
        logger.error("CalledProcessError to list snap: %s", error)
        raise HTTPException(status_code=500, detail="CalledProcessError")

    except ValueError as error:
        logger.error("ValueError to list snap: %s", error)
        raise HTTPException(status_code=500, detail="Server error")


def main() -> None:
    """Program entry point."""
    args = sys.argv
    if args[1] == "-c":
        config_file_path = args[2]
    else:
        sys.exit(1)
    with open(config_file_path, "r", encoding="utf-8") as config_file:
        config = yaml.safe_load(config_file.read())["settings"]
    uvicorn.run(app, host=config["bind_address"], port=int(config["port"]))


if __name__ == "__main__":  # pragma: no cover
    main()
