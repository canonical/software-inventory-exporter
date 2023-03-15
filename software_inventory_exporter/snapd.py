"""Snapd Adapter module."""
import socket
from typing import Dict, Optional

from requests.adapters import HTTPAdapter
from urllib3.connection import HTTPConnection
from urllib3.connectionpool import HTTPConnectionPool


class SnapdConnection(HTTPConnection):  # pragma: no cover
    """Create snapd connection thru socket at localhost."""

    def __init__(self) -> None:
        """Create SnapdConnection on localhost."""
        super().__init__("localhost")

    def connect(self) -> None:
        """Make connection socket for snapd."""
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)  # pylint: disable=W0201
        self.sock.connect("/run/snapd.socket")


class SnapdConnectionPool(HTTPConnectionPool):  # pragma: no cover
    """Snapd connection pool."""

    def __init__(self) -> None:
        """Create SnapdConnectionPool on localhost."""
        super().__init__("localhost")

    def _new_conn(self) -> SnapdConnection:
        """Create new connection using the SnapdConnection."""
        return SnapdConnection()


class SnapdAdapter(HTTPAdapter):  # pragma: no cover
    """Snapd adapter to use the snapd-api."""

    def get_connection(self, url: str, proxies: Optional[Dict] = None) -> SnapdConnectionPool:
        """Get connection with the snapd-api."""
        return SnapdConnectionPool()
