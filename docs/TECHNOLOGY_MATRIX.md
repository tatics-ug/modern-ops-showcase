# Technology Matrix

**English** | [Deutsch](TECHNOLOGY_MATRIX.de.md)

Every technology is listed with its **actual** maturity in this repository.
Maturity values: `planned` (described only), `experimental` (exists, not
reproducible), `implemented` (code and tests exist), `validated` (executed
successfully, evidence available).

## Foundations

| Technology | Status | Where | Evidence |
| --- | --- | --- | --- |
| Git / GitHub | `validated` | repository, issues, PRs | commit history, PRs |
| GitHub Actions | `validated` | `.github/workflows/` | workflow runs (validate, demos, pages) |
| YAML | `validated` | workflows, kind config | yamllint in CI |
| Bash | `validated` | `labs/*/tests/*.sh` | shellcheck in CI |
| Python | `validated` | tests, scripts, demo app | pytest in CI |
| HTTP / DNS / TLS | `implemented` | lab app endpoints, Pages domain docs | lab tests, docs |
| Linux | `validated` | all labs run on Linux | lab runs |
| Docker | `validated` | Lab 03 image build, kind | lab run |
| Terraform | `validated` | Lab 01, Lab 03 | lifecycle runs + evidence |
| OpenTofu | `validated` | `make TF=tofu lifecycle` | local run (lock-file caveat documented) |
| Kubernetes | `validated` | Lab 03 | `demo-kubernetes` run in CI |
| kind | `validated` | Lab 03 cluster | `demo-kubernetes` run in CI |
| CI/CD | `implemented` | validate/demo/pages workflows | workflow runs |
| AWS fundamentals | `planned` | not implemented, no AWS resources created | -- |

## Kubernetes / GitOps ecosystem

| Technology | Status | Notes |
| --- | --- | --- |
| Helm | `planned` | Phase 4; not needed for Lab 03 |
| Argo CD | `planned` | Lab 04, after a stable Kubernetes lab |
| Kustomize | `planned` | bundled with kubectl, not used |
| cert-manager | `planned` | alongside ingress |
| NGINX Ingress | `planned` | ingress lab |
| Kubernetes RBAC | `implemented` | restricted security context, no token mount (Lab 03) |
| Network Policies | `planned` | Lab 03 extension |
| Persistent Volumes | `planned` | not required by the demo app |
| Health Probes | `validated` | liveness/readiness in Lab 03 |
| Requests/Limits | `validated` | 25m/32Mi requests, 200m/128Mi limits |
| HPA | `planned` | only meaningful with metrics server |
| Flux CD | `planned` | alternative to Argo CD, not parallel |

## Observability

| Technology | Status | Notes |
| --- | --- | --- |
| Prometheus | `planned` | next phase (Lab 05) |
| Grafana | `planned` | next phase |
| Alertmanager | `planned` | next phase |
| Loki | `planned` | later extension |
| OpenTelemetry / Tempo | `planned` | later extension |

The demo app exposes plain HTTP health endpoints; no metrics endpoint is claimed
yet. Nothing in this repository shows a dashboard that does not exist.

## Security / identity

| Technology | Status | Notes |
| --- | --- | --- |
| Trivy | `implemented` | filesystem/config scan in CI |
| Secret hygiene | `validated` | no secrets required, `.gitignore`, docs |
| Container hardening | `validated` | non-root, read-only fs, dropped caps (Lab 03) |
| Least-privilege workflows | `validated` | explicit `permissions:` in all workflows |
| Kyverno / OPA | `planned` | Lab 06 candidate, decision deferred (ADR 0012) |
| Keycloak | `planned` | optional later lab |
| OpenBao / Vault | `planned` | optional later lab |
| SBOM (Syft) | `planned` | later extension |
| Image signing | `planned` | later extension |

## Build, registry, provisioning

| Technology | Status | Notes |
| --- | --- | --- |
| Harbor | `planned` | local registry is a later lab |
| Packer | `planned` | machine images |
| Velero | `planned` | backup/restore |
| NGINX/Traefik proxy | `planned` | ingress lab |
| OpenTofu | `validated` | as Terraform alternative, lock-file caveat |

## Data stores

| Technology | Status | Notes |
| --- | --- | --- |
| PostgreSQL | `planned` | realistic app extension |
| Redis | `planned` | cache extension |
| Kafka / RabbitMQ | `planned` | separate eventing labs |

## AI infrastructure

| Technology | Status | Notes |
| --- | --- | --- |
| Ollama | `planned` | Lab 09, local, no GPU requirement for visitors |
| vLLM | `planned` | later |
| Qdrant | `planned` | RAG example later |
| OpenAI-compatible APIs | `planned` | BYOK only, never operator keys |
| Agentic workflows | `validated` | scripted pipeline, **no LLM** (see ADR 0008) |

## Agentic engineering

| Capability | Status | Notes |
| --- | --- | --- |
| Issue-driven pipeline | `validated` | triage -> plan -> implement -> test -> review -> PR (run 43255005540) |
| Untrusted-input handling | `implemented` | issue text is parsed, never executed |
| Human approval gate | `implemented` | branch protection + no auto-merge |
| Replay of a real run | `implemented` | recording of run 43255005540 lives on the pipeline PR #2 until a human merges it |
| Live AI mode (BYOK) | `planned` | documented design only, disabled |
