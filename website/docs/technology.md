# Technology Stack

Every technology with its real status: `planned`, `experimental`, `implemented`
or `validated`.

## Foundations

| Technology | Status | Where |
| --- | --- | --- |
| Terraform | `validated` | Lab 01, Lab 03 |
| OpenTofu | `validated` | `make TF=tofu lifecycle` |
| Kubernetes | `implemented` | Lab 03 (kind) |
| Docker | `validated` | Lab 03 image |
| Python | `validated` | tests, demo app, pipeline |
| Bash | `validated` | lab lifecycle scripts |
| Git / GitHub / Actions | `validated` | repository, CI |
| HTTP, DNS, TLS | `implemented` | demo app endpoints, Pages domain docs |

## Platform engineering

| Technology | Status |
| --- | --- |
| Helm | `planned` |
| Argo CD | `planned` |
| Kustomize | `planned` |
| cert-manager, ingress | `planned` |
| Health probes, requests/limits | `validated` (Lab 03) |
| RBAC / hardened pod security | `implemented` (Lab 03) |
| HPA, network policies | `planned` |

## Observability

| Technology | Status |
| --- | --- |
| Prometheus, Grafana, Alertmanager | `planned` (Lab 05) |
| Loki, OpenTelemetry, Tempo | `planned` |

No dashboard is shown here because none exists yet.

## Security

| Technology | Status |
| --- | --- |
| Trivy filesystem scan | `implemented` (CI) |
| Least-privilege workflows | `validated` |
| Container hardening | `validated` (Lab 03) |
| Kyverno / OPA | `planned` (decision deferred, ADR 0012) |
| Keycloak, OpenBao | `planned` |
| SBOM, image signing | `planned` |

## AI infrastructure

| Technology | Status |
| --- | --- |
| Scripted agentic pipeline | `implemented` (no LLM) |
| Ollama, vLLM, Qdrant | `planned` |
| BYOK live mode | `planned` (design only) |

The authoritative, always-current matrix is
[`docs/TECHNOLOGY_MATRIX.md`](https://github.com/tatics-ug/modern-ops-showcase/blob/main/docs/TECHNOLOGY_MATRIX.md).
