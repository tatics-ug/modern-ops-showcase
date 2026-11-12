#!/usr/bin/env bash
# Lab 03 -- Kubernetes Application Platform: full, reproducible run.
#
# kind cluster -> app image -> Terraform apply -> tests -> deliberate fault ->
# detection -> fix -> tests -> destroy -> cluster delete -> evidence JSON.
#
# Safety:
#   * Only this lab's kind cluster ("modernops-lab03") and its kubeconfig are
#     created or deleted.
#   * Cleanup runs on failure as well (destroy + cluster delete).
set -Eeuo pipefail

LAB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$LAB_DIR"

TF="${TF:-terraform}"
PYTHON="${PYTHON:-python3}"
CLUSTER_NAME="modernops-lab03"
KUBECONFIG_PATH="$LAB_DIR/kind/kubeconfig"
SCENARIO_ID="kubernetes-platform-001"
SCENARIO_NAME="Kubernetes Application Platform"
IMAGE_REPO="modernops-showcase/demo-app"
IMAGE_TAG="local"
EVIDENCE_DIR="$LAB_DIR/evidence"
EVIDENCE_FILE="$EVIDENCE_DIR/local-kubernetes.json"
STARTED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
CHECKS_FILE="$(mktemp)"
export KUBECONFIG="$KUBECONFIG_PATH"

log() { printf '[lab03] %s\n' "$*"; }
record() { printf '%s|%s\n' "$1" "$2" >>"$CHECKS_FILE"; }

cluster_exists() {
  kind get clusters 2>/dev/null | grep -qx "$CLUSTER_NAME"
}

delete_cluster() {
  if cluster_exists; then
    log "deleting kind cluster $CLUSTER_NAME"
    kind delete cluster --name "$CLUSTER_NAME" >/dev/null 2>&1 || true
  fi
  rm -f "$KUBECONFIG_PATH"
}

cleanup_destroy() {
  if [[ -f "$LAB_DIR/terraform/terraform.tfstate" ]]; then
    log "cleaning up: terraform destroy (best effort)"
    ( cd "$LAB_DIR/terraform" && "$TF" destroy -input=false -auto-approve -no-color ) >/dev/null 2>&1 || true
  fi
  delete_cluster
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
    "artifacts": [{"name": "evidence/local-kubernetes.json", "kind": "json"}],
    "limitations": [
        "Temporary local kind cluster; no managed or cloud Kubernetes service involved.",
        "The application image is built locally and loaded into kind, not published to a registry.",
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
for tool in kind kubectl docker "$TF"; do
  command -v "$tool" >/dev/null 2>&1 || { log "required tool '$tool' not found"; exit 127; }
done
record "tools-available" "passed"

# --- 1. cluster + image -----------------------------------------------------
if ! cluster_exists; then
  log "creating kind cluster $CLUSTER_NAME"
  kind create cluster --name "$CLUSTER_NAME" --config kind/kind-config.yaml \
    --kubeconfig "$KUBECONFIG_PATH" --wait 120s
  record "cluster-created" "passed"
else
  log "reusing existing kind cluster $CLUSTER_NAME"
  record "cluster-created" "skipped"
fi

docker build -t "${IMAGE_REPO}:${IMAGE_TAG}" app >/dev/null
record "image-built" "passed"

kind load docker-image "${IMAGE_REPO}:${IMAGE_TAG}" --name "$CLUSTER_NAME" >/dev/null
record "image-loaded" "passed"

# --- 2. terraform -----------------------------------------------------------
cd "$LAB_DIR/terraform"
"$TF" init -input=false -no-color >/dev/null
record "terraform-init" "passed"
"$TF" validate -no-color >/dev/null
record "terraform-validate" "passed"
"$TF" apply -input=false -auto-approve -no-color
record "terraform-apply" "passed"
cd "$LAB_DIR"

# --- 3. healthy state -------------------------------------------------------
"$PYTHON" -m pytest tests -q
record "healthy-tests" "passed"

# --- 4. deliberate fault ----------------------------------------------------
log "applying the fault scenario (missing image tag, pull policy Never)"
( cd "$LAB_DIR/terraform" && "$TF" apply -input=false -auto-approve -no-color \
    -var "app_image_tag=missing" -var "image_pull_policy=Never" >/dev/null )
EXPECT_FAULT=1 "$PYTHON" -m pytest tests -q -k test_fault_is_detected
record "fault-detected" "passed"

# --- 5. fix -----------------------------------------------------------------
log "restoring the desired state"
( cd "$LAB_DIR/terraform" && "$TF" apply -input=false -auto-approve -no-color >/dev/null )
"$PYTHON" -m pytest tests -q
record "fixed-tests" "passed"

# --- 6. cleanup -------------------------------------------------------------
( cd "$LAB_DIR/terraform" && "$TF" destroy -input=false -auto-approve -no-color >/dev/null )
record "terraform-destroy" "passed"

delete_cluster
if cluster_exists; then
  record "cluster-removed" "failed"
  exit 1
fi
record "cluster-removed" "passed"

log "lab finished successfully"
