# Nachweise / Ergebnisse

Dieses Projekt belegt, was es ausgeführt hat. Demo-Läufe schreiben ein
strukturiertes JSON-Dokument mit Szenario-ID, Ausführungsmodus, Zeitstempeln,
Commit, Status je Prüfung und bekannten Einschränkungen.

## Echte Ergebnisse im Repository

| Dokument | Szenario | Modus | Status |
| --- | --- | --- | --- |
| `evidence/examples/terraform-lifecycle.local.json` | Lab 01 | `local` | `passed` |
| Workflow-Artefakte (`lab01-evidence`, `lab03-evidence`) | Labs 01/03 | `live-ci` | pro Lauf |

!!! note "Artefakte laufen ab, Beispiele sind committet"
    GitHub-Actions-Artefakte werden 14 Tage aufbewahrt. Das committete Beispiel
    ist ein echter Lauf; sein Feld `commit` zeigt, welche Revision ihn erzeugt
    hat.

## Ergebnisformat

```json
{
  "scenario_id": "terraform-lifecycle-001",
  "scenario_name": "Terraform Infrastructure Lifecycle",
  "execution_mode": "local",
  "status": "passed",
  "started_at": "2026-11-12T15:03:20Z",
  "completed_at": "2026-11-12T15:03:38Z",
  "commit": "53c37fe...",
  "workflow_run": null,
  "checks": [{ "name": "terraform-plan", "status": "passed" }],
  "artifacts": [{ "name": "evidence/local-lifecycle.json", "kind": "json" }],
  "limitations": ["Local run only; no GitHub Actions execution is recorded here."]
}
```

## Ausgeführte Workflows

| Workflow | Ergebnis |
| --- | --- |
| `validate` (python, shell, yaml, actionlint, terraform, links, site, trivy) | bestanden |
| `demo-terraform-lifecycle` | bestanden |
| `demo-kubernetes` (kind-Cluster, Apply, Tests, Fehler, Reparatur, Aufräumen) | bestanden ([Lauf](https://github.com/tatics-ug/modern-ops-showcase/actions/runs/43256482922)) |
| `deploy-pages` | bestanden |
| `agentic-issue` (geskriptet, kein LLM) | bestanden ([Lauf](https://github.com/tatics-ug/modern-ops-showcase/actions/runs/43255005540)) |

## Validierung

```bash
python3 scripts/validate_evidence.py
```

Jedes Dokument wird gegen `evidence/schema/scenario-result.schema.json`
validiert; Replay-Aufzeichnungen gegen `replay/schema/recording.schema.json`.
Ein Dokument, das nicht validiert, lässt die CI scheitern.

## Live vs. Replay

- `execution_mode: local` -- Lauf auf einer Entwicklermaschine.
- `execution_mode: live-ci` -- Lauf in GitHub Actions.
- `execution_mode: replay` -- ein aufgezeichneter Lauf, der wiedergegeben wird;
  klar gekennzeichnet.

Kein Dokument wird je als Live-KI-Lauf bezeichnet, wenn nicht tatsächlich ein
Modell gelaufen ist -- was in diesem Projekt heute nicht der Fall ist.

---

*Deutsche Fassung; maßgeblich ist die englische Originalfassung. Die Übersetzung kann hinter der englischen Version zurückliegen.*
