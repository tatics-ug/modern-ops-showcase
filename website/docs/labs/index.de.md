# Labs

Jedes Lab ist ein eigenständiges, reproduzierbares Szenario mit eigener README,
Makefile, automatisierten Tests, bewusstem Fehlerfall, Aufräumen und
Nachweis-Ausgabe.

| Lab | Fokus | Tooling | Status |
| --- | --- | --- | --- |
| [Lab 01 -- Terraform-Lebenszyklus](terraform-lifecycle.md) | Infrastructure-as-Code-Lebenszyklus | Terraform / OpenTofu, `hashicorp/local` | `validated` (lokal) |
| [Lab 03 -- Kubernetes-Plattform](kubernetes-platform.md) | Anwendungsplattform, Probes, Fehlerbehandlung | Docker, kind, Terraform-Kubernetes-Provider | `validated` (CI) |
| Lab 02 -- Ansible Linux | Linux-Konfiguration, Idempotenz | Ansible | `planned` |
| Lab 04 -- GitOps | Deklarativer Cluster-Zustand | Argo CD | `planned` |
| Lab 05 -- Observability | Metriken, Dashboards, Alerts | Prometheus, Grafana | `planned` |
| Lab 06 -- DevSecOps | Scanning, Policy, Reports | Trivy, Kyverno/OPA | `planned` |
| Lab 07 -- AWS-Emulation | Cloud-APIs ohne Kosten | Emulator (offen, ADR 0010) | `planned` |
| Lab 08 -- Agentic Engineering | Issue zu PR | geskriptete Pipeline | `validated` (geskriptet, [PR #2](https://github.com/tatics-ug/modern-ops-showcase/pull/2)) |
| Lab 09 -- KI-Infrastruktur | Lokales Modell-Serving | Ollama, Qdrant | `planned` |

## Ein Lab ausführen

```bash
make demo-list
make demo-up   SCENARIO=01
make demo-run  SCENARIO=01
make demo-down SCENARIO=01
```

Voraussetzungen und Fehlerbehebung: [Erste Schritte](../getting-started.md).

---

*Deutsche Fassung; maßgeblich ist die englische Originalfassung. Die Übersetzung kann hinter der englischen Version zurückliegen.*
