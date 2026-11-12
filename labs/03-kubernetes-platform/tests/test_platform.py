"""Integration tests for the Kubernetes platform lab.

Run against a real cluster (kind) after `terraform apply`:

    KUBECONFIG=kind/kubeconfig python3 -m pytest tests -q

Set EXPECT_FAULT=1 to verify the deliberate failure scenario instead: the
deployment must *not* become available and the pods must report an image error.
"""

from __future__ import annotations

import json
import os
import socket
import subprocess
import time
import urllib.request
from pathlib import Path

import pytest

LAB_DIR = Path(__file__).resolve().parents[1]
KUBECONFIG = os.environ.get("KUBECONFIG", str(LAB_DIR / "kind" / "kubeconfig"))
NAMESPACE = os.environ.get("NS", "demo")
DEPLOYMENT = os.environ.get("DEPLOYMENT", "demo-app")
EXPECT_FAULT = os.environ.get("EXPECT_FAULT") == "1"
WAIT_SECONDS = int(os.environ.get("WAIT_SECONDS", "120"))

ENV = {**os.environ, "KUBECONFIG": KUBECONFIG}


def kubectl(*args: str, check: bool = True, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(
        ["kubectl", *args, "--kubeconfig", KUBECONFIG],
        capture_output=True,
        text=True,
        timeout=timeout,
        env=ENV,
    )
    if check and proc.returncode != 0:
        raise AssertionError(
            f"kubectl {' '.join(args)} failed ({proc.returncode})\n"
            f"--- stdout ---\n{proc.stdout}\n--- stderr ---\n{proc.stderr}"
        )
    return proc


def get_json(*args: str) -> dict:
    return json.loads(kubectl(*args, "-o", "json").stdout)


@pytest.fixture(scope="session", autouse=True)
def _cluster_reachable() -> None:
    proc = subprocess.run(
        ["kubectl", "cluster-info", "--kubeconfig", KUBECONFIG],
        capture_output=True,
        text=True,
        timeout=30,
        env=ENV,
    )
    if proc.returncode != 0:
        pytest.skip(f"cluster not reachable with kubeconfig {KUBECONFIG}: {proc.stderr.strip()[:200]}")


@pytest.mark.skipif(EXPECT_FAULT, reason="healthy-state tests are skipped in the fault scenario")
def test_deployment_becomes_available() -> None:
    kubectl(
        "wait",
        f"--for=condition=available",
        f"deployment/{DEPLOYMENT}",
        f"-n{NAMESPACE}",
        f"--timeout={WAIT_SECONDS}s",
        timeout=WAIT_SECONDS + 30,
    )


@pytest.mark.skipif(EXPECT_FAULT, reason="healthy-state tests are skipped in the fault scenario")
def test_replicas_are_ready() -> None:
    deployment = get_json("get", "deployment", DEPLOYMENT, "-n", NAMESPACE)
    status = deployment["status"]
    assert status.get("replicas") == deployment["spec"]["replicas"], status
    assert status.get("readyReplicas") == deployment["spec"]["replicas"], status
    assert status.get("unavailableReplicas", 0) == 0, status


@pytest.mark.skipif(EXPECT_FAULT, reason="healthy-state tests are skipped in the fault scenario")
def test_service_has_endpoints() -> None:
    endpoints = get_json("get", "endpoints", DEPLOYMENT, "-n", NAMESPACE)
    addresses = [
        address for subset in endpoints.get("subsets", []) for address in subset.get("addresses", [])
    ]
    assert addresses, f"service {DEPLOYMENT} has no ready endpoints: {endpoints}"


@pytest.mark.skipif(EXPECT_FAULT, reason="healthy-state tests are skipped in the fault scenario")
def test_resources_and_probes_are_configured() -> None:
    deployment = get_json("get", "deployment", DEPLOYMENT, "-n", NAMESPACE)
    container = deployment["spec"]["template"]["spec"]["containers"][0]

    assert container["resources"]["requests"]["cpu"] == "25m"
    assert container["resources"]["requests"]["memory"] == "32Mi"
    assert container["resources"]["limits"]["cpu"] == "200m"
    assert container["resources"]["limits"]["memory"] == "128Mi"
    assert container["livenessProbe"]["httpGet"]["path"] == "/healthz"
    assert container["readinessProbe"]["httpGet"]["path"] == "/readyz"


@pytest.mark.skipif(EXPECT_FAULT, reason="healthy-state tests are skipped in the fault scenario")
def test_pod_security_context_is_restrictive() -> None:
    deployment = get_json("get", "deployment", DEPLOYMENT, "-n", NAMESPACE)
    pod_spec = deployment["spec"]["template"]["spec"]
    container = pod_spec["containers"][0]

    assert pod_spec["securityContext"]["runAsNonRoot"] is True
    assert pod_spec["securityContext"]["seccompProfile"]["type"] == "RuntimeDefault"
    assert container["securityContext"]["allowPrivilegeEscalation"] is False
    assert container["securityContext"]["readOnlyRootFilesystem"] is True
    assert container["securityContext"]["capabilities"]["drop"] == ["ALL"]


@pytest.mark.skipif(EXPECT_FAULT, reason="healthy-state tests are skipped in the fault scenario")
def test_http_endpoints_respond() -> None:
    port = socket.socket()
    port.bind(("127.0.0.1", 0))
    local_port = port.getsockname()[1]
    port.close()

    process = subprocess.Popen(
        [
            "kubectl",
            "port-forward",
            f"svc/{DEPLOYMENT}",
            f"{local_port}:80",
            "--kubeconfig",
            KUBECONFIG,
            "-n",
            NAMESPACE,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=ENV,
    )
    try:
        base = f"http://127.0.0.1:{local_port}"
        deadline = time.time() + 60
        last_error: Exception | None = None
        while time.time() < deadline:
            try:
                with urllib.request.urlopen(f"{base}/healthz", timeout=3) as response:
                    assert response.status == 200
                    assert json.loads(response.read())["status"] == "ok"
                break
            except Exception as error:  # noqa: BLE001 - retry until the tunnel is up
                last_error = error
                time.sleep(1)
        else:
            raise AssertionError(f"port-forward/healthz never succeeded: {last_error}")

        with urllib.request.urlopen(f"{base}/api/info", timeout=5) as response:
            info = json.loads(response.read())
        assert info["app"] == "demo-app"
        assert info["version"] == "local"
        assert info["hostname"]
    finally:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()


@pytest.mark.skipif(not EXPECT_FAULT, reason="only runs in the deliberate fault scenario")
def test_fault_is_detected() -> None:
    # Rolling updates keep the old, ready pods around while the new ReplicaSet is
    # broken -- so `condition=available` would still be true. The correct signal
    # is that the rollout does not make progress: the pull policy is Never and
    # the image tag does not exist, so no new pod can become ready.
    proc = kubectl(
        "rollout",
        "status",
        f"deployment/{DEPLOYMENT}",
        f"-n{NAMESPACE}",
        "--timeout=40s",
        check=False,
        timeout=60,
    )
    assert proc.returncode != 0, "fault scenario unexpectedly completed its rollout"

    pods = kubectl("get", "pods", "-n", NAMESPACE, "-o", "json").stdout
    payload = json.loads(pods)
    reasons = []
    for item in payload["items"]:
        for status in item.get("status", {}).get("containerStatuses", []) or []:
            reason = status.get("state", {}).get("waiting", {}).get("reason")
            if reason:
                reasons.append(reason)
    assert any(reason in {"ErrImageNeverPull", "ImagePullBackOff", "InvalidImageName"} for reason in reasons), (
        f"expected an image error, got container states: {reasons}"
    )
