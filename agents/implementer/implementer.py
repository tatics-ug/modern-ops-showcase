#!/usr/bin/env python3
"""Implementer role: apply the bounded change described by the plan.

The implementer is deliberately boring: it writes exactly one Markdown artefact
under evidence/agent-runs/. It never touches code, workflows or configuration.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import (  # noqa: E402
    append_event,
    assert_writable,
    load_json,
    utc_now,
    write_json,
)


def render_artefact(triage: dict, plan: dict) -> str:
    number = triage["issue_number"]
    lines = [
        f"# Agent task #{number}: {triage['title']}",
        "",
        "> Recorded by the **scripted reference pipeline** (no LLM involved).",
        "> This file is produced automatically and reviewed by a human before merge.",
        "",
        f"- Issue: {triage.get('issue_url', 'n/a')}",
        f"- Plan target: `{plan['target_path']}`",
        f"- Test command: `{plan['test_command']}`",
        f"- Generated at: {utc_now()}",
        "",
        "## Bounded plan",
        "",
    ]
    lines += [f"{index}. {step}" for index, step in enumerate(plan["steps"], start=1)]
    lines += [
        "",
        "## Limits",
        "",
        f"- max files: {plan['limits']['max_files']}",
        f"- max lines: {plan['limits']['max_lines']}",
        f"- timeout: {plan['limits']['timeout_minutes']} minutes",
        "",
        "## Issue excerpt",
        "",
        "The issue text is untrusted input; it is quoted, never executed.",
        "",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Scripted implementer role (no LLM).")
    parser.add_argument("--run", required=True, type=Path)
    parser.add_argument("--repo", required=True, type=Path)
    args = parser.parse_args()

    triage = load_json(args.run / "triage.json")
    plan = load_json(args.run / "plan.json")
    repo = Path(args.repo).resolve()

    try:
        target = assert_writable(repo, plan["target_path"])
    except PermissionError as error:
        print(f"implementer: {error}", file=sys.stderr)
        append_event(args.run, "implementer", "blocked", str(error))
        return 4

    target.parent.mkdir(parents=True, exist_ok=True)
    content = render_artefact(triage, plan)
    line_count = content.count("\n")
    if line_count > plan["limits"]["max_lines"] + 20:
        message = f"planned change is larger than the plan allows ({line_count} lines)"
        append_event(args.run, "implementer", "blocked", message)
        print(f"implementer: {message}", file=sys.stderr)
        return 4

    target.write_text(content, encoding="utf-8")
    append_event(args.run, "implementer", "wrote", str(target.relative_to(repo)))
    write_json(
        args.run / "implement.json",
        {
            "role": "implementer",
            "kind": "scripted-pipeline",
            "llm": False,
            "timestamp": utc_now(),
            "files_changed": [str(target.relative_to(repo))],
            "lines_written": line_count,
        },
    )
    print(f"implementer: wrote {target.relative_to(repo)} ({line_count} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
