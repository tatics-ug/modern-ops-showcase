#!/usr/bin/env python3
"""Reviewer role: independent, rule-based review of the pipeline change.

The reviewer only sees files, plans and test results -- not the implementer's
intentions. It refuses changes outside the whitelist, secrets in the diff,
missing tests, and missing documentation.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import (  # noqa: E402
    append_event,
    is_writable,
    load_json,
    utc_now,
    write_json,
)

SECRET_PATTERNS = (
    r"AKIA[0-9A-Z]{16}",
    r"ghp_[A-Za-z0-9]{20,}",
    r"-----BEGIN [A-Z ]+PRIVATE KEY-----",
    r"(?i)(api[_-]?key|token|password)\s*[:=]\s*['\"][^'\"]{8,}['\"]",
)


def changed_files(repo: Path) -> list[str]:
    proc = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=repo,
        capture_output=True,
        text=True,
        check=True,
    )
    files = []
    for line in proc.stdout.splitlines():
        if not line.strip():
            continue
        files.append(line[3:].strip().strip('"'))
    return files


def scan_secrets(text: str) -> list[str]:
    return [pattern for pattern in SECRET_PATTERNS if re.search(pattern, text)]


def main() -> int:
    parser = argparse.ArgumentParser(description="Scripted reviewer role (no LLM).")
    parser.add_argument("--run", required=True, type=Path)
    parser.add_argument("--repo", required=True, type=Path)
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    plan = load_json(args.run / "plan.json")
    implement = load_json(args.run / "implement.json")
    tests = load_json(args.run / "tests.json")
    triage = load_json(args.run / "triage.json")

    checks: list[dict] = []

    files = changed_files(repo)
    outside = [path for path in files if not is_writable(path)]
    checks.append(
        {
            "name": "scope-whitelist",
            "status": "passed" if not outside else "failed",
            "detail": f"{len(files)} changed file(s); outside whitelist: {outside or 'none'}",
        }
    )

    declared = set(implement.get("files_changed", []))
    checks.append(
        {
            "name": "declared-changes-match",
            "status": "passed" if declared.issubset(set(files)) else "failed",
            "detail": f"declared: {sorted(declared)}; changed: {sorted(files)}",
        }
    )

    checks.append(
        {
            "name": "file-count-within-limits",
            "status": "passed" if len(files) <= plan["limits"]["max_files"] else "failed",
            "detail": f"{len(files)} <= {plan['limits']['max_files']}",
        }
    )

    secret_hits = []
    for path in files:
        candidate = repo / path
        if candidate.is_file():
            secret_hits += [(path, pattern) for pattern in scan_secrets(candidate.read_text(encoding="utf-8", errors="ignore"))]
    checks.append(
        {
            "name": "no-secrets-in-diff",
            "status": "passed" if not secret_hits else "failed",
            "detail": f"{len(secret_hits)} hit(s)",
        }
    )

    checks.append(
        {
            "name": "tests-passed",
            "status": "passed" if tests.get("status") == "passed" else "failed",
            "detail": tests.get("summary", ""),
        }
    )

    artefact = repo / plan["target_path"]
    has_disclaimer = artefact.is_file() and "scripted reference pipeline" in artefact.read_text(encoding="utf-8")
    checks.append(
        {
            "name": "artefact-has-honest-label",
            "status": "passed" if has_disclaimer else "failed",
            "detail": "artefact mentions the scripted pipeline" if has_disclaimer else "label missing",
        }
    )

    checks.append(
        {
            "name": "issue-was-accepted",
            "status": "passed" if triage.get("accepted") else "failed",
            "detail": triage.get("reason", ""),
        }
    )

    approved = all(check["status"] == "passed" for check in checks)
    review = {
        "role": "reviewer",
        "kind": "scripted-pipeline",
        "llm": False,
        "timestamp": utc_now(),
        "approved": approved,
        "checks": checks,
        "reviewer": "rule-based-independent-review",
        "limitations": [
            "Rule-based review only: no semantic judgement, no security expertise beyond the rules above.",
        ],
    }
    write_json(args.run / "review.json", review)
    append_event(args.run, "reviewer", "approved" if approved else "changes-requested", f"{len(checks)} checks")
    print(f"reviewer: {'approved' if approved else 'changes requested'} ({len(checks)} checks)")
    return 0 if approved else 6


if __name__ == "__main__":
    raise SystemExit(main())
