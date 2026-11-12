# Lab 03 -- Kubernetes Application Platform

Runs a small, real application in a real (temporary) Kubernetes cluster, provisions
the workload declaratively with Terraform, proves it is healthy with automated
tests, breaks it on purpose, detects the failure, repairs it, and removes
everything again.

Cluster tooling: **Docker + kind**. Provisioning: **Terraform `hashicorp/kubernetes`
provider**. No cloud account, no managed Kubernetes, no cost.

Status: **validated locally** -- full lifecycle is automated in
`tests/run_lab.sh`; the same script runs in the `demo-kubernetes` workflow.

---

## 1. Purpose

| Question | Answer in this lab |
| --- | --- |
| Does a Deployment reach Ready? | `kubectl wait --for=condition=available` in tests |
| Is the Service reachable? | port-forward + real HTTP requests (`/healthz`, `/api/info`) |
| Are probes, limits and security context correct? | tests assert the live Deployment spec |
| Is a broken image detected? | image tag `missing` + `imagePullPolicy: Never` -> `ErrImageNeverPull` |
| Can the failure be repaired? | re-apply the desired state, all tests green again |
| Is cleanup complete? | Terraform destroy + kind cluster delete, verified by the script |

## 2. Prerequisites

- Docker running and usable by the current user
- `kind` >= 0.2x, `kubectl`, Terraform >= 1.6 (or OpenTofu >= 1.6), Python 3.9+ with `pytest`
- ~2 GB free disk for the kind node image, network access on first cluster creation
- No cloud credentials, no Kubernetes cluster needed in advance

## 3. Architecture

```text
host machine
├── docker
│   └── kind cluster "modernops-lab03" (temporary, deleted afterwards)
│       └── namespace demo                   <- managed by Terraform
│           ├── ConfigMap demo-app-config
│           ├── Deployment demo-app (2 replicas)
│           │   ├── image: modernops-showcase/demo-app:local (built locally, loaded into kind)
│           │   ├── liveness  /healthz
│           │   ├── readiness /readyz
│           │   ├── requests 25m/32Mi, limits 200m/128Mi
│           │   └── runAsNonRoot, read-only root fs, no capabilities
│           └── Service demo-app (ClusterIP, 80 -> 8080)
└── terraform/  (state local, git-ignored)
```

Cluster creation and resource provisioning are deliberately separate: `kind`
creates the cluster, Terraform only manages objects inside an existing cluster
(see [ADR 0005](../../docs/decisions/0005-cluster-creation-separate-from-terraform.md)).
This keeps `terraform destroy` from ever deleting a cluster.

## 4. Run it

```bash
cd labs/03-kubernetes-platform
make lifecycle            # complete run incl. fault scenario, cleanup, evidence
```

Step by step:

```bash
make cluster-up           # kind create cluster (local only)
make build                # docker build app image
make load                 # kind load docker-image
make apply                # terraform apply (creates namespace, deployment, service)
make test                 # integration tests against the live cluster
make fault                # deliberate fault + detection test
make apply                # repair
make test                 # green again
make destroy              # remove Kubernetes resources
make cluster-down         # delete the kind cluster
```

Without `make`:

```bash
kind create cluster --name modernops-lab03 --config kind/kind-config.yaml --kubeconfig kind/kubeconfig --wait 120s
docker build -t modernops-showcase/demo-app:local app
kind load docker-image modernops-showcase/demo-app:local --name modernops-lab03
terraform -chdir=terraform init && terraform -chdir=terraform apply -auto-approve
KUBECONFIG=kind/kubeconfig python3 -m pytest tests -q
kind delete cluster --name modernops-lab03
```

Expected results: 2/2 replicas Ready, all healthy-state tests pass (7 tests),
the fault test confirms the Deployment does *not* become available and the pods
report an image error, then everything is destroyed.

## 5. The deliberate fault

`app_image_tag=missing` combined with `image_pull_policy=Never` makes the kubelet
fail immediately (`ErrImageNeverPull`) without any network access:

```bash
terraform -chdir=terraform apply -var app_image_tag=missing -var image_pull_policy=Never
kubectl get pods -n demo            # ImagePullBackOff / ErrImageNeverPull
EXPECT_FAULT=1 python3 -m pytest tests -q -k test_fault_is_detected
terraform -chdir=terraform apply    # repair with the real tag
```

The fault test asserts *both* that the Deployment does not become available
within 40 s *and* that the container state carries an image error reason. A
deployment that is simply still starting would fail the test.

## 6. Tests

| Test | Checks |
| --- | --- |
| `test_deployment_becomes_available` | rollout reaches `Available` |
| `test_replicas_are_ready` | readyReplicas == desired, no unavailable replicas |
| `test_service_has_endpoints` | Service has ready Endpoint addresses |
| `test_resources_and_probes_are_configured` | requests/limits and probe paths in the live object |
| `test_pod_security_context_is_restrictive` | runAsNonRoot, seccomp, no caps, read-only fs |
| `test_http_endpoints_respond` | real HTTP through port-forward (`/healthz`, `/api/info`) |
| `test_fault_is_detected` | fault scenario is recognised as failure |

App unit tests (`app/tests/test_app.py`, no cluster needed): 5 tests.

## 7. State handling and security

- Local Terraform state, git-ignored; no remote backend (that is a later lab).
- The kubeconfig is written into `kind/kubeconfig` (git-ignored) and deleted with the cluster.
- The app container runs as UID 10001, non-root, read-only root filesystem,
  `RuntimeDefault` seccomp, all capabilities dropped, service links disabled,
  service account token not mounted. No image pull secrets are needed.
- The image is local (`:local`) and never pushed to a public registry.

## 8. Cleanup

```bash
make destroy       # Terraform resources
make cluster-down  # kind cluster + kubeconfig
make clean         # state, evidence, caches
```

`tests/run_lab.sh` performs destroy and cluster delete on success *and* on
failure (best effort). It only ever deletes the cluster named
`modernops-lab03` and the lab's own kubeconfig.

## 9. Evidence

`tests/run_lab.sh` writes `evidence/local-kubernetes.json` (git-ignored) with
scenario id, execution mode, timestamps, commit, per-check statuses and known
limitations. The `demo-kubernetes` workflow uploads it as an artifact.

## 10. Known limitations

- Single-node kind cluster: no multi-node scheduling, no autoscaler.
- No ingress controller, no TLS, no GitOps -- those are later labs (04/05).
- The image is loaded from the local Docker daemon, not from a registry.
- CI runs the same script, but evidence is only as good as the last run.
