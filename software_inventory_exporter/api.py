"""API module."""

import logging
from typing import Dict, List

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from software_inventory_exporter import exporter

logger = logging.getLogger(__name__)

app = FastAPI(
    title="software-inventory-exporter",
    description="Exporter for apt packages and snaps in json via web.",
    license_info={
        "name": "GNU GENERAL PUBLIC LICENSE",
        "url": "https://www.gnu.org/licenses/gpl-3.0.en.html",
    },
)


@app.get("/hostname", response_class=PlainTextResponse)
def get_hostname() -> str:
    """Get the hostname of the machine."""
    return exporter.generate_hostname_output()


@app.get("/kernel")
def get_kernel() -> Dict:
    """Get the kernel version of the machine."""
    return exporter.generate_kernel_output()


@app.get("/dpkg")
def get_dpkg() -> List[Dict]:
    """List the debian packages installed in the machine."""
    return exporter.generate_dpkg_output()


@app.get("/snap")
def get_snap() -> Dict:
    """List the snap packages installed in the machine."""
    return exporter.generate_snap_output()
