#!/usr/bin/env python3
"""Triage role: decide whether an issue may be processed by the pipeline.

Input:  an issue JSON document (number, title, body, labels, url)
Output: <run-dir>/triage.json and an event in <run-dir>/events.jsonl

Exit codes: 0 accepted, 3 rejected, 2 misuse.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import (  # noqa: E402
    MAX_BODY_BYTES,
    MAX_TITLE_CHARS,
    append_event,
    load_json,
    normalise_title,
    scan_dangerous,
    sha256_of,
    utc_now,
    write_json,
)

REQUIRED_BODY_SECTIONS = ("goal", "scope", "acceptance")
REQUIRED_LABEL = "agent:task"


def triage(issue: dict) -> tuple[bool, str]:
    raw_title = (issue.get("title") or "").strip()
    title = normalise_title(raw_title)
    body = issue.get("body") or ""
    labels = [label.get("name", "") if isinstance(label, dict) else str(label) for label in issue.get("labels", [])]

    if not title:
        return False, "issue has no title"
    if len(raw_title) > MAX_TITLE_CHARS:
        return False, f"title exceeds {MAX_TITLE_CHARS} characters"
    if len(body.encode("utf-8")) > MAX_BODY_BYTES:
        return False, f"body exceeds {MAX_BODY_BYTES} bytes"
    if REQUIRED_LABEL not in labels:
        return False, f"label '{REQUIRED_LABEL}' is required"

    lowered = body.lower()
    missing = [section for section in REQUIRED_BODY_SECTIONS if section not in lowered]
    if missing:
        return False, f"issue body is missing required sections: {', '.join(missing)}"

    dangerous = scan_dangerous(body)
    if dangerous:
        return False, "issue text contains disallowed instructions: " + ", ".join(sorted(set(dangerous)))

    if body.count("\n- ") > 10:
        return False, "issue asks for too many individual changes (more than 10 bullet points)"

    return True, "issue is bounded and safe to process"


def main() -> int:
    parser = argparse.ArgumentParser(description="Scripted triage role (no LLM).")
    parser.add_argument("--issue", required=True, type=Path, help="issue JSON file")
    parser.add_argument("--run", required=True, type=Path, help="run directory")
    args = parser.parse_args()

    try:
        issue = load_json(args.issue)
    except (OSError, ValueError) as error:
        print(f"triage: cannot read issue JSON: {error}", file=sys.stderr)
        return 2

    accepted, reason = triage(issue)
    result = {
        "role": "triage",
        "kind": "scripted-pipeline",
        "llm": False,
        "timestamp": utc_now(),
        "issue_number": issue.get("number"),
        "issue_url": issue.get("url"),
        "title": normalise_title(issue.get("title", "")),
        "body_sha256": sha256_of(issue.get("body") or ""),
        "labels": sorted(str(label.get("name") if isinstance(label, dict) else label) for label in issue.get("labels", [])),
        "accepted": accepted,
        "reason": reason,
    }
    write_json(args.run / "triage.json", result)
    append_event(args.run, "triage", "accepted" if accepted else "rejected", reason)
    print(f"triage: {'accepted' if accepted else 'rejected'} -- {reason}")
    return 0 if accepted else 3


if __name__ == "__main__":
    raise SystemExit(main())
