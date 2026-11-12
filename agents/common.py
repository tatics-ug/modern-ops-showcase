"""Shared helpers for the scripted agent pipeline.

No third-party dependencies, no network, no model calls. The pipeline is a
deterministic reference implementation of the orchestration shape described in
docs/AGENT_WORKFLOW.md.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Only these locations may be written by the implementer.
WRITABLE_PREFIXES = ("evidence/agent-runs/", "replay/recordings/")

# Untrusted issue text is rejected when it tries to steer the pipeline into
# privileged or destructive behaviour.
DANGEROUS_PATTERNS = (
    r"\brm\s+-rf\b",
    r"\bsudo\b",
    r"\bchmod\s+777\b",
    r"\bcurl\b[^\n]*\|\s*(ba)?sh\b",
    r"\bwget\b[^\n]*\|\s*(ba)?sh\b",
    r"\bterraform\s+apply\b",
    r"\baws\s+[a-z]",
    r"\bkubectl\s+delete\b",
    r"\bsecret\b",
    r"\btoken\b",
    r"\bapi[_-]?key\b",
    r"\bpassword\b",
    r"\bprivate\s*key\b",
    r"\bgit\s+push\s+--force\b",
    r"\.github/workflows",
    r"pull_request_target",
)

MAX_BODY_BYTES = 8000
MAX_TITLE_CHARS = 120


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_of(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def append_event(run_dir: Path, actor: str, action: str, detail: str = "") -> dict:
    """Append one event to the ordered event log of a run."""
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    log = run_dir / "events.jsonl"
    order = 0
    if log.exists():
        order = sum(1 for _ in log.open(encoding="utf-8"))
    event = {
        "order": order,
        "timestamp": utc_now(),
        "actor": actor,
        "action": action,
        "detail": detail,
    }
    with log.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")
    return event


def read_events(run_dir: Path) -> list[dict]:
    log = Path(run_dir) / "events.jsonl"
    if not log.exists():
        return []
    return [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines() if line.strip()]


def is_writable(relative_path: str) -> bool:
    normalised = relative_path.replace("\\", "/").lstrip("./")
    return any(normalised.startswith(prefix) for prefix in WRITABLE_PREFIXES)


def assert_writable(repo: Path, relative_path: str) -> Path:
    """Resolve a whitelisted repository path and refuse anything else."""
    if not is_writable(relative_path):
        raise PermissionError(f"path '{relative_path}' is outside the pipeline whitelist")
    target = (Path(repo) / relative_path).resolve()
    repo_root = Path(repo).resolve()
    if target != repo_root and repo_root not in target.parents:
        raise PermissionError(f"path '{relative_path}' escapes the repository")
    return target


def scan_dangerous(text: str) -> list[str]:
    found = []
    lowered = text.lower()
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, lowered):
            found.append(pattern)
    return found


def normalise_title(title: str) -> str:
    return re.sub(r"\s+", " ", title).strip()[:MAX_TITLE_CHARS]
