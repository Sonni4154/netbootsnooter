"""Boot server agent providing HTTP and TFTP services."""
from __future__ import annotations

import logging
from functools import partial
from pathlib import Path
from threading import Thread
from typing import Optional
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

try:
    from tftpy import TftpServer
except Exception:  # pragma: no cover - tftpy may be missing
    TftpServer = None  # type: ignore[assignment]


class BootServerAgent:
    """Start minimal HTTP and TFTP services and keep them running."""

    def __init__(
        self,
        root: Path | str = Path("boot"),
        http_port: int = 8000,
        tftp_port: int = 6969,
    ) -> None:
        self.root = Path(root)
        self.root.mkdir(exist_ok=True)
        self.http_port = http_port
        self.tftp_port = tftp_port
        self.logger = logging.getLogger(self.__class__.__name__)
        self.http_server: Optional[ThreadingHTTPServer] = None
        self.http_thread: Optional[Thread] = None
        self.tftp_server: Optional[TftpServer] = None
        self.tftp_thread: Optional[Thread] = None

    # ------------------------------------------------------------------
    # HTTP handling
    def start_http(self, port: Optional[int] = None) -> int:
        """Start an HTTP server serving files from ``root``.

        Returns the port the server is bound to.
        """
        if port is not None:
            self.http_port = port
        handler = partial(SimpleHTTPRequestHandler, directory=str(self.root))
        self.http_server = ThreadingHTTPServer(("0.0.0.0", self.http_port), handler)
        # If port 0 was given, update to actual port
        self.http_port = self.http_server.server_address[1]
        self.http_thread = Thread(target=self.http_server.serve_forever, daemon=True)
        self.http_thread.start()
        self.logger.info("HTTP server started on port %s", self.http_port)
        return self.http_port

    def stop_http(self) -> None:
        if self.http_server:
            self.http_server.shutdown()
            self.http_server.server_close()
            if self.http_thread:
                self.http_thread.join()
            self.http_server = None
            self.http_thread = None

    # ------------------------------------------------------------------
    # TFTP handling
    def start_tftp(self, port: Optional[int] = None) -> Optional[int]:
        """Start a TFTP server if :mod:`tftpy` is available."""
        if TftpServer is None:
            self.logger.warning("tftpy not installed; skipping TFTP server")
            return None
        if port is not None:
            self.tftp_port = port
        self.tftp_server = TftpServer(str(self.root))
        self.tftp_thread = Thread(
            target=self.tftp_server.listen,
            kwargs={"listenip": "0.0.0.0", "listenport": self.tftp_port},
            daemon=True,
        )
        self.tftp_thread.start()
        self.logger.info("TFTP server started on port %s", self.tftp_port)
        return self.tftp_port

    def stop_tftp(self) -> None:
        if self.tftp_server:
            self.tftp_server.stop(now=True)
            if self.tftp_thread:
                self.tftp_thread.join()
            self.tftp_server = None
            self.tftp_thread = None

    # ------------------------------------------------------------------
    def ensure_running(self) -> None:
        """Restart any service that has stopped."""
        if self.http_server is None or self.http_thread is None or not self.http_thread.is_alive():
            self.logger.warning("HTTP server not running; restarting")
            self.start_http(self.http_port)
        if TftpServer is not None and (
            self.tftp_server is None or self.tftp_thread is None or not self.tftp_thread.is_alive()
        ):
            self.logger.warning("TFTP server not running; restarting")
            self.start_tftp(self.tftp_port)

    def run(self) -> None:
        """Start all services."""
        self.start_http(self.http_port)
        self.start_tftp(self.tftp_port)

    def stop(self) -> None:
        """Stop all running services."""
        self.stop_http()
        self.stop_tftp()


__all__ = ["BootServerAgent"]
