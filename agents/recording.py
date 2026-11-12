#!/usr/bin/env python3
"""Assemble the run record and the replay recording from one pipeline run.

Everything written here is derived from real files produced by the roles in this
run. Missing role output is recorded as missing, never invented.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import (  # noqa: E402
    append_event,
    assert_writable,
    load_json,
    read_events,
    utc_now,
    write_json,
)

KNOWN_LIMITATIONS = [
    "Scripted pipeline: no language model, no reasoning beyond deterministic rules.",
    "Review is rule-based and cannot judge design quality.",
    "Pull requests created with the workflow GITHUB_TOKEN do not trigger further workflows.",
    "The pipeline writes only to evidence/agent-runs/ and replay/recordings/; it cannot change code.",
]


def optional(path: Path) -> dict | None:
    try:
        return load_json(path)
    except (OSError, ValueError):
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Assemble run record and replay recording (no LLM).")
    parser.add_argument("--run", required=True, type=Path)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--scenario", default="agent-task-001")
    parser.add_argument("--pr-number", default=None)
    parser.add_argument("--pr-url", default=None)
    parser.add_argument("--status", default="passed")
    parser.add_argument(
        "--execution-mode",
        default="live-ci" if os.environ.get("GITHUB_ACTIONS") else "local",
        choices=["live-ci", "local"],
    )
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    triage = load_json(args.run / "triage.json")
    plan = load_json(args.run / "plan.json")
    implement = load_json(args.run / "implement.json")
    tests = load_json(args.run / "tests.json")
    review = load_json(args.run / "review.json")
    events = read_events(args.run)

    number = triage["issue_number"]
    run_id = os.environ.get("GITHUB_RUN_ID") or utc_now().replace(":", "").replace("-", "")
    recording_id = f"agent-issue-{number}-{run_id}"

    run_record = {
        "schema_version": "1",
        "scenario_id": args.scenario,
        "scenario_name": f"Agent task #{number}",
        "kind": "scripted-pipeline",
        "llm": False,
        "recording_id": recording_id,
        "execution_mode": args.execution_mode,
        "status": args.status,
        "issue": {"number": number, "title": triage["title"], "url": triage.get("issue_url")},
        "roles": [event["actor"] for event in events if event["actor"] not in {"orchestrator"}],
        "events": events,
        "plan": plan,
        "changes": implement.get("files_changed", []),
        "tests": tests,
        "review": review,
        "pull_request": {"number": args.pr_number, "url": args.pr_url},
        "known_limitations": KNOWN_LIMITATIONS,
        "generated_at": utc_now(),
    }

    run_record_path = assert_writable(repo, f"evidence/agent-runs/issue-{number}-run.json")
    write_json(run_record_path, run_record)

    recording = {
        "recording_id": recording_id,
        "kind": "scripted-pipeline",
        "llm": False,
        "scenario_id": args.scenario,
        "title": f"Agent task #{number}: {triage['title']}",
        "description": (
            "Replay of a real GitHub Actions run of the scripted reference pipeline. "
            "No language model was involved; every step is a deterministic script."
        ),
        "execution_mode": args.execution_mode,
        "issue": {"number": number, "title": triage["title"], "url": triage.get("issue_url")},
        "roles": run_record["roles"],
        "started_at": triage.get("timestamp"),
        "completed_at": utc_now(),
        "events": events,
        "plan": plan,
        "changes": run_record["changes"],
        "tests": {"status": tests.get("status"), "summary": tests.get("summary")},
        "review": {"approved": review.get("approved"), "checks": review.get("checks", [])},
        "pull_request": run_record["pull_request"],
        "known_limitations": KNOWN_LIMITATIONS,
    }
    recording_path = assert_writable(repo, f"replay/recordings/{recording_id}.json")
    write_json(recording_path, recording)

    append_event(args.run, "orchestrator", "recording-assembled", recording_path.name)
    print(f"recording: {recording_path.relative_to(repo)}")
    print(f"run record: {run_record_path.relative_to(repo)}")
    print(json.dumps({"recording_id": recording_id}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
