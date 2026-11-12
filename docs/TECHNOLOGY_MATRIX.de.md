# Technologiematrix

**Deutsch** | [English](TECHNOLOGY_MATRIX.md)

Jede Technologie ist mit ihrem **tatsächlichen** Reifegrad in diesem Repository
aufgeführt. Reifegrade: `planned` (nur beschrieben), `experimental` (vorhanden,
nicht reproduzierbar), `implemented` (Code und Tests vorhanden), `validated`
(erfolgreich ausgeführt, Nachweis verfügbar).

## Grundlagen

| Technologie | Status | Wo | Nachweis |
| --- | --- | --- | --- |
| Git / GitHub | `validated` | Repository, Issues, PRs | Commit-Historie, PRs |
| GitHub Actions | `validated` | `.github/workflows/` | Workflow-Läufe (validate, Demos, Pages) |
| YAML | `validated` | Workflows, kind-Konfiguration | yamllint in der CI |
| Bash | `validated` | `labs/*/tests/*.sh` | shellcheck in der CI |
| Python | `validated` | Tests, Skripte, Demo-App | pytest in der CI |
| HTTP / DNS / TLS | `implemented` | Lab-App-Endpunkte, Pages-Domain-Doku | Lab-Tests, Doku |
| Linux | `validated` | alle Labs laufen auf Linux | Lab-Läufe |
| Docker | `validated` | Image-Build für Lab 03, kind | Lab-Lauf |
| Terraform | `validated` | Lab 01, Lab 03 | Lifecycle-Läufe + Nachweise |
| OpenTofu | `validated` | `make TF=tofu lifecycle` | lokaler Lauf (Einschränkung mit Lock-Datei dokumentiert) |
| Kubernetes | `validated` | Lab 03 | `demo-kubernetes`-Lauf in der CI |
| kind | `validated` | Cluster für Lab 03 | `demo-kubernetes`-Lauf in der CI |
| CI/CD | `implemented` | validate-/Demo-/Pages-Workflows | Workflow-Läufe |
| AWS-Grundlagen | `planned` | nicht implementiert, keine AWS-Ressourcen angelegt | -- |

## Kubernetes-/GitOps-Ökosystem

| Technologie | Status | Hinweise |
| --- | --- | --- |
| Helm | `planned` | Phase 4; für Lab 03 nicht nötig |
| Argo CD | `planned` | Lab 04, nach einem stabilen Kubernetes-Lab |
| Kustomize | `planned` | in kubectl enthalten, nicht verwendet |
| cert-manager | `planned` | zusammen mit Ingress |
| NGINX Ingress | `planned` | Ingress-Lab |
| Kubernetes RBAC | `implemented` | eingeschränkter Security Context, kein Token-Mount (Lab 03) |
| Network Policies | `planned` | Erweiterung von Lab 03 |
| Persistent Volumes | `planned` | von der Demo-App nicht benötigt |
| Health Probes | `validated` | Liveness/Readiness in Lab 03 |
| Requests/Limits | `validated` | 25m/32Mi Requests, 200m/128Mi Limits |
| HPA | `planned` | nur mit Metrics-Server sinnvoll |
| Flux CD | `planned` | Alternative zu Argo CD, nicht parallel |

## Observability

| Technologie | Status | Hinweise |
| --- | --- | --- |
| Prometheus | `planned` | nächste Phase (Lab 05) |
| Grafana | `planned` | nächste Phase |
| Alertmanager | `planned` | nächste Phase |
| Loki | `planned` | spätere Erweiterung |
| OpenTelemetry / Tempo | `planned` | spätere Erweiterung |

Die Demo-App stellt einfache HTTP-Health-Endpunkte bereit; einen Metrics-Endpunkt
gibt es noch nicht. Nichts in diesem Repository zeigt ein Dashboard, das nicht
existiert.

## Sicherheit / Identität

| Technologie | Status | Hinweise |
| --- | --- | --- |
| Trivy | `implemented` | Dateisystem-/Konfigurations-Scan in der CI |
| Secret-Hygiene | `validated` | keine Secrets nötig, `.gitignore`, Doku |
| Container-Härtung | `validated` | non-root, schreibgeschütztes Dateisystem, entfernte Capabilities (Lab 03) |
| Workflows mit geringsten Rechten | `validated` | explizite `permissions:` in allen Workflows |
| Kyverno / OPA | `planned` | Kandidat für Lab 06, Entscheidung vertagt (ADR 0012) |
| Keycloak | `planned` | optionales späteres Lab |
| OpenBao / Vault | `planned` | optionales späteres Lab |
| SBOM (Syft) | `planned` | spätere Erweiterung |
| Image-Signierung | `planned` | spätere Erweiterung |

## Build, Registry, Provisionierung

| Technologie | Status | Hinweise |
| --- | --- | --- |
| Harbor | `planned` | lokale Registry ist ein späteres Lab |
| Packer | `planned` | Maschinen-Images |
| Velero | `planned` | Backup/Restore |
| NGINX/Traefik-Proxy | `planned` | Ingress-Lab |
| OpenTofu | `validated` | als Terraform-Alternative, Einschränkung mit Lock-Datei |

## Datenspeicher

| Technologie | Status | Hinweise |
| --- | --- | --- |
| PostgreSQL | `planned` | realistische App-Erweiterung |
| Redis | `planned` | Cache-Erweiterung |
| Kafka / RabbitMQ | `planned` | separate Eventing-Labs |

## KI-Infrastruktur

| Technologie | Status | Hinweise |
| --- | --- | --- |
| Ollama | `planned` | Lab 09, lokal, keine GPU-Anforderung für Besucher |
| vLLM | `planned` | später |
| Qdrant | `planned` | RAG-Beispiel später |
| OpenAI-kompatible APIs | `planned` | nur BYOK, nie Betreiber-Schlüssel |
| Agentic Workflows | `validated` | geskriptete Pipeline, **kein LLM** (siehe ADR 0008) |

## Agentic Engineering

| Fähigkeit | Status | Hinweise |
| --- | --- | --- |
| Issue-getriebene Pipeline | `validated` | Triage -> Plan -> Implement -> Test -> Review -> PR (Lauf 43255005540) |
| Umgang mit unvertrauenswürdiger Eingabe | `implemented` | Issue-Text wird geparst, nie ausgeführt |
| Menschliches Freigabe-Gate | `implemented` | Branch-Schutz + kein Auto-Merge |
| Replay eines echten Laufs | `implemented` | die Aufzeichnung von Lauf 43255005540 liegt im Pipeline-PR #2, bis ein Mensch sie merged |
| Live-KI-Modus (BYOK) | `planned` | nur dokumentiertes Design, deaktiviert |

---

*Deutsche Fassung; maßgeblich ist die englische Originalfassung. Die Übersetzung kann hinter der englischen Version zurückliegen.*
