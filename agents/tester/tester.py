#!/usr/bin/env python3
"""Tester role: run the repository tests and record the real result.

This role never invents results: the exit code and the last output line of the
test command are stored as they are.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import append_event, load_json, utc_now, write_json  # noqa: E402

TIMEOUT_SECONDS = 600


def main() -> int:
    parser = argparse.ArgumentParser(description="Scripted tester role (no LLM).")
    parser.add_argument("--run", required=True, type=Path)
    parser.add_argument("--repo", required=True, type=Path)
    args = parser.parse_args()

    plan = load_json(args.run / "plan.json")
    command = plan["test_command"].split()
    # Use the interpreter that runs this role, so a virtualenv with the test
    # dependencies behaves exactly like the CI environment.
    if command and command[0] in {"python3", "python"}:
        command[0] = sys.executable
    repo = Path(args.repo).resolve()

    started = utc_now()
    try:
        proc = subprocess.run(
            command,
            cwd=repo,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
        exit_code = proc.returncode
        output = (proc.stdout + proc.stderr).strip().splitlines()
    except subprocess.TimeoutExpired:
        exit_code = 124
        output = [f"test command timed out after {TIMEOUT_SECONDS}s"]
    except FileNotFoundError as error:
        exit_code = 127
        output = [f"test command not found: {error}"]

    tail = output[-1] if output else ""
    summary = next((line for line in reversed(output) if "passed" in line or "failed" in line or "error" in line), tail)
    passed = exit_code == 0

    write_json(
        args.run / "tests.json",
        {
            "role": "tester",
            "kind": "scripted-pipeline",
            "llm": False,
            "timestamp": utc_now(),
            "started_at": started,
            "command": plan["test_command"],
            "exit_code": exit_code,
            "status": "passed" if passed else "failed",
            "summary": summary[:400],
            "output_tail": output[-20:],
        },
    )
    append_event(args.run, "tester", "tests-passed" if passed else "tests-failed", summary[:200])
    print(f"tester: exit code {exit_code} -- {summary[:160]}")
    return 0 if passed else 5


if __name__ == "__main__":
    raise SystemExit(main())
