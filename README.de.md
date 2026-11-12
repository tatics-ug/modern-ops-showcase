# ModernOps Showcase

**Deutsch** | [English](README.md)

**Moderne Infrastruktur & Agentic Engineering** -- ein reproduzierbares,
praxisnahes Showcase für moderne Infrastruktur und Agentic Engineering. Erkunde
Linux-Automatisierung, Terraform, Kubernetes, GitOps, CI/CD, Observability,
Sicherheit und KI-gestützte Softwareentwicklung -- integriert in einem
transparenten Referenzprojekt.

Website: <https://modern-ops-showcase.tatics.de> (eigene Domain geplant) --
Repository: <https://github.com/tatics-ug/modern-ops-showcase>

Jede Fähigkeit in diesem Repository ist entweder **tatsächlich ausführbar** oder
ehrlich als geplant gekennzeichnet. Nichts hier ist ein Screenshot von etwas,
das nicht existiert.

---

## Was enthalten ist

| Bereich | Inhalt | Status |
| --- | --- | --- |
| Lab 01 | Terraform-Lebenszyklus der Infrastruktur (Module, State, Idempotenz, Destroy) | `validated` (lokal) |
| Lab 03 | Kubernetes-Anwendungsplattform (kind, Terraform, Probes, Fehlerfall) | `validated` (CI) |
| Lab 02, 04--09 | Ansible, Argo CD, Observability, DevSecOps, AWS-Emulation, Agentic-Lab, KI-Infrastruktur | `planned` |
| CI/CD | Validierungs-Workflow, Pages-Deployment, Demo-Workflows | `implemented` |
| Website | MkDocs-Material-Seite, veröffentlicht über GitHub Pages | `implemented` |
| Agentic Engineering | Geskriptete Referenz-Pipeline (ohne LLM) + Replay-Schema + BYOK-Design | `validated` (erster echter Lauf: PR #2, menschlicher Merge steht aus) |

Statusvokabular: `planned` -- nur beschrieben, `experimental` -- vorhanden, aber
noch nicht reproduzierbar, `implemented` -- Code und Tests vorhanden,
`validated` -- erfolgreich ausgeführt und Nachweise verlinkt.

## Schnellstart

```bash
make demo-list                 # verfügbare Demo-Szenarien auflisten
make demo-up SCENARIO=01       # ein Szenario vorbereiten
make demo-run SCENARIO=01      # ausführen (schreibt Nachweise)
make demo-down SCENARIO=01     # alles wieder entfernen
```

Voraussetzungen für die Labs: Terraform >= 1.6 (oder OpenTofu >= 1.6), Python
3.12 mit `pytest`, Docker, `kind`, `kubectl`, `make`. Kein Cloud-Konto, kein
API-Schlüssel, keine GPU.

## Repository-Struktur

```text
.github/            Workflows (Validierung, Pages, Demos, Agentic-Pipeline), Issue-Formulare
agents/             geskriptete Agentenrollen (Triage, Planner, Implementer, Tester, Reviewer)
docs/               Architektur, Sicherheit, Betrieb, Technologiematrix, ADRs
evidence/           Ergebnis-Schema + echte Beispielergebnisse
labs/01-terraform-lifecycle/   Terraform-Lebenszyklus-Lab
labs/03-kubernetes-platform/   Kubernetes-Plattform-Lab (kind + Terraform)
replay/             Replay-Schema, Szenarien und Aufzeichnungen echter Läufe
scripts/            Repository-Tooling (Nachweis-Validierung)
tests/              repository-weite Tests
website/            MkDocs-Material-Seite (veröffentlicht auf GitHub Pages)
```

## Wie es ausgeführt wird

| Baustein | Läuft auf |
| --- | --- |
| Website | GitHub Pages (nur statisch, kein Backend) |
| Code, Dokumentation, Issues, PRs | GitHub |
| Validierungs- und Demo-Workflows | GitHub Actions (kostenlose Runner für öffentliche Repositories) |
| Labs | lokale Maschine (Docker, kind, Terraform) und GitHub Actions |
| Cloud-Ressourcen | keine im Standardlauf; AWS ist nur eine optionale künftige Demo |

## Kosten und Abhängigkeiten

Alles hier Verwendete ist kostenlos: GitHub-Free-Organisation mit öffentlichen
Repositories, standardmäßige GitHub-gehostete Runner (kostenlos für öffentliche
Repositories), GitHub Pages und lokal installierte Open-Source-Werkzeuge
(Terraform/OpenTofu, kind, kubectl, Docker, Python, MkDocs Material,
Terraform-Provider).

Es ist kein AWS-Konto, keine bezahlte API und keine Kreditkarte erforderlich.
Ideen, die Geld kosten würden (echte AWS-Ressourcen, Live-LLM-Läufe), sind als
*optional* dokumentiert und standardmäßig deaktiviert; siehe
[docs/decisions](docs/decisions).

## Dokumentation

- [docs/GETTING_STARTED.de.md](docs/GETTING_STARTED.de.md) -- Voraussetzungen, lokaler Lauf, Sicherheitshinweise
- [docs/RUNBOOK.de.md](docs/RUNBOOK.de.md) -- Demos betreiben und Fehler beheben
- [docs/TECHNOLOGY_MATRIX.de.md](docs/TECHNOLOGY_MATRIX.de.md) -- jede Technologie mit ehrlichem Status
- [docs/AGENT_WORKFLOW.de.md](docs/AGENT_WORKFLOW.de.md) -- Triage/Plan/Implement/Tests/Review-Pipeline
- [ARCHITECTURE.de.md](ARCHITECTURE.de.md) -- Systemüberblick und Ausführungsmodell
- [SECURITY.de.md](SECURITY.de.md) -- Sicherheitsmodell, Meldung, Umgang mit Secrets
- [AGENTS.de.md](AGENTS.de.md) -- Regeln für menschliche und KI-Beitragende
- [evidence/](evidence/README.de.md) -- Ergebnisformat und echte Beispielergebnisse

## Agentic Engineering in einem Absatz

GitHub-Issues sind die Aufgabenquelle. Eine GitHub-Actions-Pipeline prüft das
Issue (Triage), leitet einen begrenzten Plan ab, wendet eine freigegebene
Änderung an, führt die Tests aus, macht ein unabhängiges regelbasiertes Review
und öffnet einen Pull Request. Die Pipeline enthält **kein LLM**: Sie ist eine
deterministische Referenzimplementierung der Orchestrierungsform und wird
überall als solche gekennzeichnet. Ein vollständiges Replay eines echten Laufs
liegt unter [replay/](replay/README.de.md). Live-KI-Läufe sind ein separater,
optionaler BYOK-Modus, der in diesem Repository **nicht** aktiviert ist; ein
Betreiber-Schlüssel wird nie offengelegt.

## Nachweise

| Quelle | Link |
| --- | --- |
| Validierungs-Workflow | https://github.com/tatics-ug/modern-ops-showcase/actions/runs/43256482921 |
| Lab-01-Lebenszyklus in CI | https://github.com/tatics-ug/modern-ops-showcase/actions/runs/43254091400 |
| Lab-03-Lebenszyklus in CI | https://github.com/tatics-ug/modern-ops-showcase/actions/runs/43256482922 |
| Website-Deployment | https://github.com/tatics-ug/modern-ops-showcase/actions/runs/43256483294 |
| Erster echter Agentic-Pipeline-Lauf | https://github.com/tatics-ug/modern-ops-showcase/actions/runs/43255005540 (Pull Request #2) |

## Lizenz

[MIT](LICENSE)

---

*Deutsche Fassung; maßgeblich ist die englische Originalfassung. Die Übersetzung kann hinter der englischen Version zurückliegen.*
