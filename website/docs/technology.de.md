# Technologiestack

Jede Technologie mit ihrem echten Status: `planned`, `experimental`,
`implemented` oder `validated`.

## Grundlagen

| Technologie | Status | Wo |
| --- | --- | --- |
| Terraform | `validated` | Lab 01, Lab 03 |
| OpenTofu | `validated` | `make TF=tofu lifecycle` |
| Kubernetes | `implemented` | Lab 03 (kind) |
| Docker | `validated` | Image für Lab 03 |
| Python | `validated` | Tests, Demo-App, Pipeline |
| Bash | `validated` | Lifecycle-Skripte der Labs |
| Git / GitHub / Actions | `validated` | Repository, CI |
| HTTP, DNS, TLS | `implemented` | Endpunkte der Demo-App, Domain-Doku für Pages |

## Plattform-Engineering

| Technologie | Status |
| --- | --- |
| Helm | `planned` |
| Argo CD | `planned` |
| Kustomize | `planned` |
| cert-manager, Ingress | `planned` |
| Health Probes, Requests/Limits | `validated` (Lab 03) |
| RBAC / gehärtete Pod-Sicherheit | `implemented` (Lab 03) |
| HPA, Network Policies | `planned` |

## Observability

| Technologie | Status |
| --- | --- |
| Prometheus, Grafana, Alertmanager | `planned` (Lab 05) |
| Loki, OpenTelemetry, Tempo | `planned` |

Hier wird kein Dashboard gezeigt, weil noch keines existiert.

## Sicherheit

| Technologie | Status |
| --- | --- |
| Trivy-Dateisystem-Scan | `implemented` (CI) |
| Workflows mit geringsten Rechten | `validated` |
| Container-Härtung | `validated` (Lab 03) |
| Kyverno / OPA | `planned` (Entscheidung vertagt, ADR 0012) |
| Keycloak, OpenBao | `planned` |
| SBOM, Image-Signierung | `planned` |

## KI-Infrastruktur

| Technologie | Status |
| --- | --- |
| Geskriptete Agentic-Pipeline | `implemented` (kein LLM) |
| Ollama, vLLM, Qdrant | `planned` |
| BYOK-Live-Modus | `planned` (nur Design) |

Die maßgebliche, immer aktuelle Matrix liegt in `docs/TECHNOLOGY_MATRIX.de.md`
im Repository: [docs/](https://github.com/tatics-ug/modern-ops-showcase/tree/main/docs).

---

*Deutsche Fassung; maßgeblich ist die englische Originalfassung. Die Übersetzung kann hinter der englischen Version zurückliegen.*
