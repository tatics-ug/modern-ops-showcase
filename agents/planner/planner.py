#!/usr/bin/env python3
"""Planner role: derive a bounded, whitelisted plan from an accepted issue.

Input:  <run>/triage.json
Output: <run>/plan.json
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import append_event, load_json, utc_now, write_json  # noqa: E402

MAX_STEPS = 6


def build_plan(triage: dict) -> dict:
    number = triage["issue_number"]
    return {
        "role": "planner",
        "kind": "scripted-pipeline",
        "llm": False,
        "timestamp": utc_now(),
        "issue_number": number,
        "goal": f"Document the agent task from issue #{number} in a bounded artefact",
        "target_path": f"evidence/agent-runs/issue-{number}.md",
        "steps": [
            "read the accepted issue",
            f"write evidence/agent-runs/issue-{number}.md (single file, no code changes)",
            "run the repository test suite",
            "run the independent rule-based review",
            "assemble the run record and the replay recording",
            "open a pull request for human review",
        ][:MAX_STEPS],
        "test_command": "python3 -m pytest tests -q",
        "limits": {"max_files": 1, "max_lines": 40, "timeout_minutes": 10},
        "stop_conditions": [
            "triage rejected the issue",
            "tests fail after one corrective attempt",
            "review does not approve",
            "issue text requests a path outside the whitelist",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Scripted planner role (no LLM).")
    parser.add_argument("--run", required=True, type=Path)
    args = parser.parse_args()

    triage = load_json(args.run / "triage.json")
    if not triage.get("accepted"):
        print("planner: refusing to plan a rejected issue", file=sys.stderr)
        return 3

    plan = build_plan(triage)
    write_json(args.run / "plan.json", plan)
    append_event(
        args.run,
        "planner",
        "planned",
        f"{len(plan['steps'])} steps, target {plan['target_path']}",
    )
    print(f"planner: {len(plan['steps'])} steps, target {plan['target_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
