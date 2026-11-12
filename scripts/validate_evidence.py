#!/usr/bin/env python3
"""Validate every evidence document and replay recording against its schema.

Usage:
    python3 scripts/validate_evidence.py [--strict]

Requires `jsonschema` (see requirements-dev.txt); CI installs it. Exit code 1 on
any validation error, so this is usable as a CI gate.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_SCHEMA = REPO_ROOT / "evidence" / "schema" / "scenario-result.schema.json"
RECORDING_SCHEMA = REPO_ROOT / "replay" / "schema" / "recording.schema.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate evidence and replay documents.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="fail if jsonschema is missing instead of skipping validation",
    )
    args = parser.parse_args()

    try:
        import jsonschema
    except ModuleNotFoundError:
        message = "jsonschema is not installed (pip install -r requirements-dev.txt)"
        if args.strict:
            print(f"error: {message}", file=sys.stderr)
            return 2
        print(f"warning: {message}; validation skipped")
        return 0

    targets = [
        (EVIDENCE_SCHEMA, sorted((REPO_ROOT / "evidence").rglob("*.json"))),
        (RECORDING_SCHEMA, sorted((REPO_ROOT / "replay" / "recordings").rglob("*.json"))),
    ]

    failures = 0
    checked = 0
    for schema_path, documents in targets:
        schema = load(schema_path)
        for document in documents:
            if document == schema_path:
                continue
            checked += 1
            try:
                jsonschema.validate(instance=load(document), schema=schema)
            except jsonschema.ValidationError as error:
                failures += 1
                location = ".".join(str(part) for part in error.absolute_path) or "<root>"
                print(f"FAIL {document.relative_to(REPO_ROOT)}: {location}: {error.message}", file=sys.stderr)
            else:
                print(f"ok   {document.relative_to(REPO_ROOT)}")

    print(f"\n{checked - failures}/{checked} document(s) valid")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
