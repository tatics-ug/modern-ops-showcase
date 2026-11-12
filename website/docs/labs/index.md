# Labs

Each lab is a self-contained, reproducible scenario with its own README,
Makefile, automated tests, deliberate failure case, cleanup and evidence output.

| Lab | Focus | Tooling | Status |
| --- | --- | --- | --- |
| [Lab 01 -- Terraform lifecycle](terraform-lifecycle.md) | Infrastructure as Code lifecycle | Terraform / OpenTofu, `hashicorp/local` | `validated` (local) |
| [Lab 03 -- Kubernetes platform](kubernetes-platform.md) | Application platform, probes, fault handling | Docker, kind, Terraform Kubernetes provider | `validated` (CI) |
| Lab 02 -- Ansible Linux | Linux configuration, idempotency | Ansible | `planned` |
| Lab 04 -- GitOps | Declarative cluster state | Argo CD | `planned` |
| Lab 05 -- Observability | Metrics, dashboards, alerts | Prometheus, Grafana | `planned` |
| Lab 06 -- DevSecOps | Scanning, policy, reports | Trivy, Kyverno/OPA | `planned` |
| Lab 07 -- AWS emulation | Cloud APIs without cost | emulator (TBD, ADR 0010) | `planned` |
| Lab 08 -- Agentic engineering | Issue to PR | scripted pipeline | `validated` (scripted, [PR #2](https://github.com/tatics-ug/modern-ops-showcase/pull/2)) |
| Lab 09 -- AI infrastructure | Local model serving | Ollama, Qdrant | `planned` |

## Running a lab

```bash
make demo-list
make demo-up   SCENARIO=01
make demo-run  SCENARIO=01
make demo-down SCENARIO=01
```

Requirements and troubleshooting: [Getting Started](../getting-started.md).
