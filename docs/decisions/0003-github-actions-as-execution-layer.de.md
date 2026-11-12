# ADR 0003 -- GitHub Actions als Ausführungsschicht

**Deutsch** | [English](0003-github-actions-as-execution-layer.md)

- Status: accepted
- Datum: 2026-11-12
- Entscheider: Repository-Eigentümer

## Kontext

Demos, Validierung und die Agentic-Pipeline brauchen einen Scheduler und Runner.
Das Projekt darf kein Geld kosten.

## Entscheidung

GitHub Actions mit standardmäßigen GitHub-gehosteten Runnern verwenden. Für
öffentliche Repositories sind diese Runner kostenlos, und die Nutzung reduziert
kein enthaltenes Kontingent.

## Verworfene Alternativen

- Selbst gehostete Runner: keine Kosten pro Minute, aber dauerhaft zu pflegende
  und abzusichernde Infrastruktur.
- Ausschließlich lokale Ausführung: kein reproduzierbarer Nachweis für Besucher.

## Konsequenzen

- Kostenlose Ausführung; der Nachweis ist eine Workflow-Lauf-URL.
- Unvertrauenswürdige Eingabe muss sorgfältig behandelt werden: keine Secrets in
  Fork-/PR-Kontexten, explizite `permissions:`, kein `pull_request_target`.
- Die Bindung an GitHub wird akzeptiert; Skripte bleiben lokal ausführbar.

---

*Deutsche Fassung; maßgeblich ist die englische Originalfassung. Die Übersetzung kann hinter der englischen Version zurückliegen.*
