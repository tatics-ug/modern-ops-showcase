"""Verification tests for Lab 01 -- Terraform Infrastructure Lifecycle.

The tests run against an *applied* workspace (see `make apply` or
`make lifecycle`). They verify what Terraform actually created instead of
trusting the configuration alone.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
from pathlib import Path

import pytest

LAB_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = LAB_DIR.parents[1]
TF = os.environ.get("TF_BIN") or os.environ.get("TF") or shutil.which("terraform") or "terraform"
STATE_FILE = LAB_DIR / "terraform.tfstate"

EXPECTED_FILES = (
    "metadata.json",
    "runtime.conf",
    "demo-credential.txt",
    "checksums.txt",
)


def run_tf(*args: str, check: bool = True, timeout: int = 180) -> subprocess.CompletedProcess[str]:
    """Run terraform inside the lab directory."""
    proc = subprocess.run(
        [TF, *args],
        cwd=LAB_DIR,
        capture_output=True,
        text=True,
        timeout=timeout,
        env={**os.environ, "TF_IN_AUTOMATION": "1"},
    )
    if check and proc.returncode != 0:
        raise AssertionError(
            f"{TF} {' '.join(args)} failed with exit code {proc.returncode}\n"
            f"--- stdout ---\n{proc.stdout}\n--- stderr ---\n{proc.stderr}"
        )
    return proc


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.fixture(scope="session", autouse=True)
def _require_applied_state() -> None:
    if not STATE_FILE.exists():
        pytest.skip("no terraform.tfstate -- run `make apply` or `make lifecycle` first")


@pytest.fixture(scope="session")
def outputs() -> dict:
    return json.loads(run_tf("output", "-json").stdout)


def as_path(value: str) -> Path:
    """Outputs are relative to the lab directory; resolve them against it."""
    path = Path(value)
    return path if path.is_absolute() else (LAB_DIR / path).resolve()


@pytest.fixture(scope="session")
def workspace(outputs: dict) -> Path:
    path = as_path(outputs["workspace_dir"]["value"])
    assert path.is_dir(), f"workspace directory {path} does not exist"
    return path


def test_workspace_contains_expected_files(workspace: Path) -> None:
    missing = [name for name in EXPECTED_FILES if not (workspace / name).is_file()]
    assert not missing, f"missing generated files: {missing}"


def test_outputs_describe_existing_files(outputs: dict, workspace: Path) -> None:
    assert as_path(outputs["metadata_path"]["value"]) == workspace / "metadata.json"
    assert as_path(outputs["runtime_config_path"]["value"]) == workspace / "runtime.conf"
    assert outputs["file_count"]["value"] == 4
    assert outputs["workspace_name"]["value"] == "lab01-demo"


def test_metadata_matches_configuration(outputs: dict, workspace: Path) -> None:
    metadata = json.loads((workspace / "metadata.json").read_text())
    assert metadata["workspace_name"] == "lab01-demo"
    assert metadata["environment"] == "demo"
    assert metadata["provider"] == "hashicorp/local"
    assert metadata["managed_by"] == "terraform"
    assert metadata["tags"]["lab"] == "01-terraform-lifecycle"
    assert metadata["tags"]["project"] == "modern-ops-showcase"
    # Terraform's own hash must match the file on disk.
    assert outputs["metadata_sha256"]["value"] == sha256_of(workspace / "metadata.json")


def test_runtime_config_is_rendered(workspace: Path) -> None:
    content = (workspace / "runtime.conf").read_text()
    assert re.search(r"^workspace_name = lab01-demo$", content, re.MULTILINE)
    assert re.search(r"^environment    = demo$", content, re.MULTILINE)
    assert "provider       = hashicorp/local" in content


def test_checksums_match_files(workspace: Path) -> None:
    checksums = {}
    for line in (workspace / "checksums.txt").read_text().splitlines():
        if not line.strip():
            continue
        name, digest = line.split()
        checksums[name] = digest
    assert checksums["metadata.json"] == sha256_of(workspace / "metadata.json")
    assert checksums["runtime.conf"] == sha256_of(workspace / "runtime.conf")


def test_file_permissions_are_applied(workspace: Path) -> None:
    metadata_mode = stat.S_IMODE((workspace / "metadata.json").stat().st_mode)
    credential_mode = stat.S_IMODE((workspace / "demo-credential.txt").stat().st_mode)
    assert metadata_mode == 0o644, f"expected 0644, got {metadata_mode:04o}"
    assert credential_mode == 0o600, f"expected 0600, got {credential_mode:04o}"


def test_sensitive_output_is_flagged(outputs: dict) -> None:
    assert outputs["sensitive_demo_value"]["sensitive"] is True


def test_sensitive_value_is_redacted_in_plain_output() -> None:
    plain = run_tf("output").stdout
    assert "demo-only-placeholder" not in plain
    assert "sensitive" in plain.lower()


def test_demo_credential_contains_only_dummy_value(workspace: Path) -> None:
    value = (workspace / "demo-credential.txt").read_text().strip()
    assert value.startswith("demo-only-placeholder"), "the lab must never hold a real credential"


def test_plan_is_idempotent() -> None:
    proc = run_tf("plan", "-input=false", "-detailed-exitcode", "-no-color", check=False)
    assert proc.returncode == 0, (
        "second plan still reports changes; the configuration is not idempotent\n"
        f"{proc.stdout[-2000:]}"
    )


def test_invalid_workspace_name_is_rejected() -> None:
    proc = run_tf("plan", "-input=false", "-no-color", "-var", "workspace_name=Invalid_Name", check=False)
    assert proc.returncode != 0, "an invalid workspace_name must fail validation"
    assert "workspace_name must match" in proc.stderr + proc.stdout


def test_path_escape_is_rejected() -> None:
    proc = run_tf("plan", "-input=false", "-no-color", "-var", "workspace_dir=/tmp/lab01-escape", check=False)
    assert proc.returncode != 0, "an absolute workspace_dir must fail validation"
    assert "must be a non-empty relative path" in proc.stderr + proc.stdout


def test_state_is_not_tracked_by_git() -> None:
    if not (REPO_ROOT / ".git").exists():
        pytest.skip("not a git repository")
    proc = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "check-ignore", "-v", "labs/01-terraform-lifecycle/terraform.tfstate"],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, "terraform.tfstate must be git-ignored"
