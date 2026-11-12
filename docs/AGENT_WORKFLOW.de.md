# Agenten-Workflow (geskriptete Referenz-Pipeline)

**Deutsch** | [English](AGENT_WORKFLOW.md)

Dieses Dokument beschreibt die Issue-zu-PR-Pipeline in
`.github/workflows/agentic-issue.yml` und die Rollen, die sie umsetzt.

**Wichtig:** Diese Pipeline enthält **kein LLM und keine KI-API**. Sie ist eine
deterministische Referenzimplementierung der Orchestrierungsform (Triage,
begrenzter Plan, begrenzte Änderung, Tests, unabhängiges Review, PR, menschliche
Freigabe). Jedes Artefakt sagt das ausdrücklich. Live-KI-Läufe sind ein separater
BYOK-Modus, der **nicht** implementiert ist (siehe
[ADR 0007](decisions/0007-byok-for-live-agent-runs.de.md)).

## 1. Auslöser

- Ein Issue erhält das Label `agent:task`, oder
- der Workflow wird manuell gestartet (`workflow_dispatch` mit einer Issue-Nummer).

Das Issue muss die Vorlage `agent-task` verwenden, damit der Body strukturierte
Felder enthält.

## 2. Rollen und Artefakte

| Rolle | Skript | Ausgabe |
| --- | --- | --- |
| Triage | `agents/triage/triage.py` | `triage.json`: Hash von Titel/Body, Labels, angenommen/abgelehnt + Grund |
| Planner | `agents/planner/planner.py` | `plan.json`: begrenzte Schritte, freigegebener Zielpfad, Testbefehl |
| Implementer | `agents/implementer/implementer.py` | schreibt nur `<whitelist>/issue-<n>.md`, nie etwas anderes |
| Tester | `agents/tester/tester.py` | führt `python3 -m pytest tests -q` aus, protokolliert Exit-Code und Zusammenfassung |
| Reviewer | `agents/reviewer/reviewer.py` | `review.json`: unabhängige Regelprüfungen (Umfang, Secrets, Tests, Doku) |
| Orchestrator | der Workflow selbst | Ablaufsteuerung, Stoppbedingungen, PR-Erstellung, Lauf-Zusammenfassung |

Die Rollen sind reine Python-Skripte ohne Drittanbieter-Abhängigkeiten und laufen
daher überall, wo Python 3.9+ verfügbar ist. Sie kommunizieren über JSON-Dateien
in einem temporären Lauf-Verzeichnis.

## 3. Sicherheitsregeln

1. **Issue-Text sind Daten.** Er wird nie in einen Shell-Befehl interpoliert;
   die Skripte parsen ihn mit Python und geben nur validierte Werte weiter.
2. **Nur Whitelist.** Der Implementer schreibt ausschließlich nach
   `evidence/agent-runs/`. Jeder andere Pfad wird vor dem Schreiben abgelehnt.
3. **Keine Secrets.** Der Workflow fordert nur `contents: write`,
   `pull-requests: write`, `issues: write` an; er liest keine anderen Secrets als
   das automatische `GITHUB_TOKEN`.
4. **Kein Auto-Merge.** Der Workflow öffnet/aktualisiert einen PR und stoppt. Ein
   Merge benötigt ein menschliches Review auf einem geschützten Branch.
5. **Begrenzte Laufzeit.** `timeout-minutes` und Timeouts pro Schritt begrenzen
   den Lauf.
6. **Ehrliche Kennzeichnung.** PR-Body und Artefakte nennen „geskriptete
   Pipeline, kein LLM“.
7. **Früh ablehnen.** Die Triage lehnt Issues mit fehlenden Feldern, zu vielen
   angeforderten Pfaden oder gefährlichen Schlüsselwörtern ab (`secret`, `token`,
   `rm -rf`, `terraform apply` auf Cloud-Ressourcen, ...).

## 4. Inhalt des Pull Requests

Der von der Pipeline erzeugte PR enthält:

- die begrenzte Änderung (eine Markdown-Datei unter `evidence/agent-runs/`),
- `evidence/agent-runs/<issue>-run.json` mit Plan, Tests, Review und Zeitstempeln,
- eine Beschreibung von Ziel, Änderung, Testergebnis, Review-Ergebnis und
  bekannten Einschränkungen.

Der PR ist ein normaler PR: Er braucht ein menschliches Review, die CI muss
bestehen, und er wird nie automatisch gemerged.

## 5. Replay

`replay/schema/recording.schema.json` definiert eine Aufzeichnung. Eine
Aufzeichnung entsteht aus einem **echten** Workflow-Lauf und enthält Szenario,
Issue-Metadaten, die Rollen, geordnete Ereignisse, Plan, Testergebnisse,
Review-Ergebnis, PR-Metadaten und bekannte Einschränkungen. Aufzeichnungen sind
klar mit `execution_mode: "live-ci"` und `kind: "scripted-pipeline"` markiert;
sie geben sich nie als KI-Agenten-Lauf aus.

Siehe `replay/README.de.md` für den Dateiaufbau und die Ehrlichkeitsregeln.

## 6. Selbst ausführen

```bash
# lokal, ohne GitHub
python3 agents/triage/triage.py --issue evidence/agent-runs/example-issue.json --out /tmp/run
python3 agents/planner/planner.py --run /tmp/run
python3 agents/implementer/implementer.py --run /tmp/run --repo .
python3 agents/tester/tester.py --run /tmp/run --repo .
python3 agents/reviewer/reviewer.py --run /tmp/run --repo .
```

Der Workflow macht dasselbe über `scripts/run_agent_pipeline.sh`, das zusätzlich
Branch, Commit und PR erzeugt (nur wenn es innerhalb von GitHub Actions läuft).

## 7. Erster echter Lauf

- Workflow-Lauf: https://github.com/tatics-ug/modern-ops-showcase/actions/runs/43255005540
- Pull Request: <https://github.com/tatics-ug/modern-ops-showcase/pull/2>
- Aufzeichnung: `replay/recordings/agent-issue-1-43255005540.json` (im PR-Branch)
- Issue: #1

Der Lauf hat Triage, Plan, Implementierung, Tests (alle grün), Review
(freigegeben) und die PR-Erstellung abgeschlossen. Der Pull Request ist offen und
wartet auf ein menschliches Review; die Pipeline merged nie.

Bekannte CI-Einschränkung: Pull Requests, die mit dem Workflow-`GITHUB_TOKEN`
erstellt werden, starten ihre Checks im Zustand `action_required`, sodass ein
Maintainer diese Läufe manuell freigeben muss.

## 8. Was nicht implementiert ist

- Keine Modellaufrufe, keine Prompts, keine Token-Abrechnung.
- Keine Multi-Issue-Warteschlange, keine Retry-Schleifen über einen korrigierenden
  Durchlauf hinaus.
- Keine automatischen Codeänderungen außerhalb von `evidence/agent-runs/`.
- Kein Live-Modus: BYOK ist nur Design.

---

*Deutsche Fassung; maßgeblich ist die englische Originalfassung. Die Übersetzung kann hinter der englischen Version zurückliegen.*
