#!/usr/bin/env python3
"""Minimal demo application for the Kubernetes platform lab.

Standard library only: no dependencies to install, no build step, a small image
that starts in well under a second. Endpoints:

    GET /healthz   -> 200 {"status": "ok"}       (liveness probe)
    GET /readyz    -> 200 {"status": "ready"}    (readiness probe)
    GET /api/info  -> 200 JSON metadata
    GET /          -> small HTML page
"""

from __future__ import annotations

import json
import os
import socket
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

APP_NAME = os.environ.get("APP_NAME", "modernops-demo-app")
APP_VERSION = os.environ.get("APP_VERSION", "dev")


class Handler(BaseHTTPRequestHandler):
    server_version = "modernops-demo-app"
    sys_version = ""

    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status: int, payload: dict) -> None:
        self._send(status, json.dumps(payload).encode(), "application/json")

    def do_GET(self) -> None:  # noqa: N802 (http.server API)
        path = self.path.split("?", 1)[0]
        if path == "/healthz":
            self._json(200, {"status": "ok"})
        elif path == "/readyz":
            self._json(200, {"status": "ready"})
        elif path == "/api/info":
            self._json(
                200,
                {
                    "app": APP_NAME,
                    "version": APP_VERSION,
                    "hostname": socket.gethostname(),
                },
            )
        elif path == "/":
            body = (
                "<!doctype html><html><head><title>ModernOps demo app</title></head>"
                f"<body><h1>{APP_NAME}</h1><p>version: {APP_VERSION}</p>"
                '<p><a href="/api/info">/api/info</a> &middot; '
                '<a href="/healthz">/healthz</a> &middot; '
                '<a href="/readyz">/readyz</a></p>'
                "</body></html>"
            ).encode()
            self._send(200, body, "text/html; charset=utf-8")
        else:
            self._json(404, {"error": "not found", "path": path})

    def log_message(self, *args) -> None:  # keep container logs quiet and clean
        return


def main() -> None:
    port = int(os.environ.get("PORT", "8080"))
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()


if __name__ == "__main__":
    main()
