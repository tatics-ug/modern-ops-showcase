#!/usr/bin/env bash
# Orchestrator for the scripted reference pipeline (no LLM).
#
# Runs triage -> plan -> implement -> test -> review -> recording against a real
# issue JSON document. Exits with the failing role's code:
#   3 triage rejected, 4 implementer blocked, 5 tests failed, 6 review rejected.
#
# Usage:
#   RUN_DIR=/tmp/run ISSUE_JSON=agents/examples/example-issue.json \
#     bash scripts/run_agent_pipeline.sh
set -Eeuo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

PYTHON="${PYTHON:-python3}"
ISSUE_JSON="${ISSUE_JSON:-}"
RUN_DIR="${RUN_DIR:-$(mktemp -d "${TMPDIR:-/tmp}/modernops-agent.XXXXXX")}"

interactive() { [[ -t 1 ]]; }

if [[ -z "$ISSUE_JSON" || ! -f "$ISSUE_JSON" ]]; then
  echo "run_agent_pipeline: ISSUE_JSON must point to an existing issue JSON file" >&2
  exit 2
fi

# The reviewer inspects `git status`, so the pipeline needs a clean baseline --
# exactly like the CI checkout. Refuse early instead of producing a confusing review.
if [[ -n "$(git -C "$REPO_ROOT" status --porcelain)" ]]; then
  echo "run_agent_pipeline: working tree is not clean; commit or stash first" >&2
  exit 2
fi

echo "== pipeline run in $RUN_DIR (scripted, no LLM) =="

set +e
"$PYTHON" agents/triage/triage.py --issue "$ISSUE_JSON" --run "$RUN_DIR"
rc=$?
set -e
if [[ $rc -ne 0 ]]; then
  echo "pipeline: triage did not accept the issue (exit $rc)"
  echo "RUN_DIR=$RUN_DIR"
  exit "$rc"
fi

"$PYTHON" agents/planner/planner.py --run "$RUN_DIR"
"$PYTHON" agents/implementer/implementer.py --run "$RUN_DIR" --repo "$REPO_ROOT"

set +e
"$PYTHON" agents/tester/tester.py --run "$RUN_DIR" --repo "$REPO_ROOT"
rc=$?
set -e
if [[ $rc -ne 0 ]]; then
  echo "pipeline: tests failed (exit $rc); writing a failed run record"
  "$PYTHON" agents/recording.py --run "$RUN_DIR" --repo "$REPO_ROOT" --status failed || true
  echo "RUN_DIR=$RUN_DIR"
  exit "$rc"
fi

"$PYTHON" agents/reviewer/reviewer.py --run "$RUN_DIR" --repo "$REPO_ROOT"
"$PYTHON" agents/recording.py --run "$RUN_DIR" --repo "$REPO_ROOT" \
  --pr-number "${PR_NUMBER:-}" --pr-url "${PR_URL:-}"

echo "RUN_DIR=$RUN_DIR"
if interactive; then
  echo "pipeline finished successfully"
fi
