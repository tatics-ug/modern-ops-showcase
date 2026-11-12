# Replay

**Deutsch** | [English](README.md)

Replay macht einen Lauf nachvollziehbar, ohne ihn erneut auszuführen -- und ohne
API-Schlüssel. Es ist die Aufzeichnung eines **echten** Laufs, nie eine
Simulation.

## Aufbau

```text
replay/
├── schema/recording.schema.json      Struktur einer Aufzeichnung
├── scenarios/agent-task-001.json     was die Pipeline tun soll
└── recordings/                       eine Datei pro echtem Lauf
```

## Ehrlichkeitsregeln

1. Eine Aufzeichnung wird aus den eigenen Artefakten des Laufs abgeleitet
   (Triage, Plan, Ereignisse, Tests, Review, Pull Request). Fehlende Schritte
   werden als fehlend erfasst.
2. Jede Aufzeichnung nennt `kind` und `llm`. Die aktuelle Pipeline ist
   `kind: "scripted-pipeline"`, `llm: false`; sie ist **kein** KI-Agenten-Lauf und
   gibt sich auch nicht als solcher aus.
3. `execution_mode: "live-ci"` bedeutet, dass der Lauf in GitHub Actions
   stattgefunden hat; `replay` wäre die erneute Darstellung einer solchen
   Aufzeichnung. Nichts hier behauptet einen Live-Modellaufruf.
4. Pull Requests werden nie automatisch gemerged; das menschliche Gate ist Teil
   des aufgezeichneten Ablaufs.

## Eine Aufzeichnung lesen

```bash
jq '.title, .events[] | {order, actor, action}' replay/recordings/<file>.json
```

Das Array `events` ist geordnet (`order`), jeder Eintrag hat einen Zeitstempel,
die ausführende Rolle und ein kurzes Detail. `changes`, `tests`, `review` und
`pull_request` zeigen, was tatsächlich passiert ist.

## Aufzeichnungen validieren

```bash
python3 scripts/validate_evidence.py
```

## Aktueller Stand

Die erste echte Aufzeichnung entstand aus dem `agentic-issue`-Lauf
[43255005540](https://github.com/tatics-ug/modern-ops-showcase/actions/runs/43255005540):
`replay/recordings/agent-issue-1-43255005540.json`. Sie enthält sechs geordnete
Ereignisse (Triage, Plan, Implementierung, Tests, Review, Aufzeichnung), den Plan,
das Testergebnis, die Review-Prüfungen und die PR-Metadaten (PR #2).

Diese Datei liegt derzeit im Pipeline-Branch `agent/issue-1-43255005540` und ist
Teil von [Pull Request #2](https://github.com/tatics-ug/modern-ops-showcase/pull/2).
Sie wird Teil von `main`, sobald ein Mensch den Pull Request merged -- die
Pipeline merged nie, genau das ist der Sinn des menschlichen Gates.

---

*Deutsche Fassung; maßgeblich ist die englische Originalfassung. Die Übersetzung kann hinter der englischen Version zurückliegen.*
