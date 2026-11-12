"""Fast unit tests for the demo app (no cluster required)."""

from __future__ import annotations

import json
import os
import sys
import threading
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import app  # noqa: E402


@pytest.fixture()
def base_url():
    server = ThreadingHTTPServer(("127.0.0.1", 0), app.Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}"
    finally:
        server.shutdown()
        server.server_close()


def get(url: str):
    with urllib.request.urlopen(url, timeout=5) as response:
        return response.status, response.read().decode()


def test_healthz(base_url: str) -> None:
    status, body = get(f"{base_url}/healthz")
    assert status == 200
    assert json.loads(body)["status"] == "ok"


def test_readyz(base_url: str) -> None:
    status, body = get(f"{base_url}/readyz")
    assert status == 200
    assert json.loads(body)["status"] == "ready"


def test_api_info(base_url: str) -> None:
    status, body = get(f"{base_url}/api/info")
    assert status == 200
    payload = json.loads(body)
    assert payload["app"] == os.environ.get("APP_NAME", "modernops-demo-app")
    assert payload["version"]
    assert payload["hostname"]


def test_index_page(base_url: str) -> None:
    status, body = get(f"{base_url}/")
    assert status == 200
    assert "modernops-demo-app" in body


def test_unknown_path_returns_404(base_url: str) -> None:
    with pytest.raises(urllib.error.HTTPError) as excinfo:
        get(f"{base_url}/does-not-exist")
    assert excinfo.value.code == 404
