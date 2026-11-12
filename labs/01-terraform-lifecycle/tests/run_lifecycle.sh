#!/usr/bin/env bash
# Lab 01 -- Terraform Infrastructure Lifecycle: full, reproducible run.
#
# init -> fmt -check -> validate -> plan -> apply -> verify (pytest) ->
# idempotency check -> destroy -> cleanup verification -> evidence JSON.
#
# Safety:
#   * Only this lab directory is touched.
#   * On failure a trap destroys the lab state and removes the generated
#     workspace if (and only if) it lives inside this lab directory.
set -Eeuo pipefail

LAB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$LAB_DIR"

TF="${TF:-terraform}"
export TF
PYTHON="${PYTHON:-python3}"
SCENARIO_ID="terraform-lifecycle-001"
SCENARIO_NAME="Terraform Infrastructure Lifecycle"
WORKSPACE_DIR="$LAB_DIR/workspace"
EVIDENCE_DIR="$LAB_DIR/evidence"
EVIDENCE_FILE="$EVIDENCE_DIR/local-lifecycle.json"
PLAN_FILE="$LAB_DIR/lab.tfplan"
STARTED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
CHECKS_FILE="$(mktemp)"

log() { printf '[lab01] %s\n' "$*"; }
record() { printf '%s|%s\n' "$1" "$2" >>"$CHECKS_FILE"; }

# Remove only lab-owned artefacts; never any path outside $LAB_DIR.
cleanup_workspace() {
  if [[ -d "$WORKSPACE_DIR" ]]; then
    case "$(cd "$WORKSPACE_DIR" && pwd)" in
      "$LAB_DIR"/*) rm -rf "$WORKSPACE_DIR" ;;
      *) log "refusing to delete $WORKSPACE_DIR (outside $LAB_DIR)" ;;
    esac
  fi
  rm -f "$PLAN_FILE"
}

cleanup_destroy() {
  if [[ -f "$LAB_DIR/terraform.tfstate" ]]; then
    log "cleaning up: terraform destroy (best effort)"
    "$TF" destroy -input=false -auto-approve -no-color >/dev/null 2>&1 || true
    rmdir "$WORKSPACE_DIR" 2>/dev/null || true
  fi
}

write_evidence() {
  local status="$1"
  mkdir -p "$EVIDENCE_DIR"
  "$PYTHON" - "$EVIDENCE_FILE" "$status" "$SCENARIO_ID" "$SCENARIO_NAME" \
    "$STARTED_AT" "$CHECKS_FILE" <<'PY'
import json
import subprocess
import sys
from datetime import datetime, timezone

out, status, scenario_id, scenario_name, started, checks_file = sys.argv[1:7]

checks = []
with open(checks_file, encoding="utf-8") as handle:
    for line in handle:
        line = line.rstrip("\n")
        if not line:
            continue
        name, _, check_status = line.partition("|")
        checks.append({"name": name, "status": check_status})

try:
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
    ).stdout.strip()
except (subprocess.CalledProcessError, FileNotFoundError):
    commit = None

evidence = {
    "schema_version": "1",
    "scenario_id": scenario_id,
    "scenario_name": scenario_name,
    "execution_mode": "local",
    "status": status,
    "started_at": started,
    "completed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "commit": commit,
    "workflow_run": None,
    "checks": checks,
    "artifacts": [{"name": "evidence/local-lifecycle.json", "kind": "json"}],
    "limitations": [
        "Local run only; no GitHub Actions execution is recorded here.",
        "Uses the hashicorp/local provider; no cloud or cluster resources are created.",
    ],
}
with open(out, "w", encoding="utf-8") as handle:
    json.dump(evidence, handle, indent=2)
    handle.write("\n")
PY
}

on_exit() {
  local rc=$?
  trap - ERR EXIT
  if [[ $rc -ne 0 ]]; then
    record "lifecycle" "failed"
    cleanup_destroy
    cleanup_workspace
    write_evidence "failed" || true
  else
    write_evidence "passed" || rc=1
  fi
  rm -f "$CHECKS_FILE"
  log "evidence: ${EVIDENCE_FILE#"$LAB_DIR"/} (status: $([[ $rc -eq 0 ]] && echo passed || echo failed))"
  exit "$rc"
}
trap on_exit EXIT

# --- 0. preconditions -------------------------------------------------------
command -v "$TF" >/dev/null 2>&1 || { log "terraform binary '$TF' not found"; exit 127; }
log "using $("$TF" version | head -n 1)"
record "terraform-available" "passed"

# --- 1. format --------------------------------------------------------------
"$TF" fmt -check -recursive
record "terraform-fmt" "passed"

# --- 2. init ----------------------------------------------------------------
"$TF" init -input=false -no-color
record "terraform-init" "passed"

# --- 3. validate ------------------------------------------------------------
"$TF" validate -no-color
record "terraform-validate" "passed"

# --- 4. plan ----------------------------------------------------------------
"$TF" plan -input=false -no-color -out="$PLAN_FILE"
record "terraform-plan" "passed"

# --- 5. apply ---------------------------------------------------------------
"$TF" apply -input=false -no-color "$PLAN_FILE"
record "terraform-apply" "passed"

# --- 6. verification --------------------------------------------------------
"$PYTHON" -m pytest tests -q
record "pytest" "passed"

# --- 7. idempotency ---------------------------------------------------------
set +e
"$TF" plan -input=false -no-color -detailed-exitcode >/dev/null 2>&1
plan_rc=$?
set -e
if [[ $plan_rc -ne 0 ]]; then
  log "second plan still reports changes (exit code $plan_rc)"
  record "second-plan-no-changes" "failed"
  exit 1
fi
record "second-plan-no-changes" "passed"

# --- 8. destroy -------------------------------------------------------------
"$TF" destroy -input=false -no-color -auto-approve
record "terraform-destroy" "passed"

# --- 9. cleanup verification ------------------------------------------------
rmdir "$WORKSPACE_DIR" 2>/dev/null || true
if [[ -e "$WORKSPACE_DIR" ]]; then
  log "workspace directory still exists after destroy"
  record "workspace-removed" "failed"
  exit 1
fi
if [[ -n "$("$TF" state list 2>/dev/null)" ]]; then
  log "state still contains resources after destroy"
  record "state-empty" "failed"
  exit 1
fi
record "workspace-removed" "passed"
record "state-empty" "passed"
rm -f "$PLAN_FILE"

log "lifecycle finished successfully"
