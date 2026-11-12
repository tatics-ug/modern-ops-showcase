# ADR 0006 -- Replay als Standard-Demonstrationsmodus

**Deutsch** | [English](0006-replay-as-default-mode.md)

- Status: accepted
- Datum: 2026-11-12
- Entscheider: Repository-Eigentümer

## Kontext

Besucher müssen dem Agentic-Ablauf ohne API-Schlüssel folgen können. Live-Agenten-
Läufe kosten Geld und dürfen nie einen Betreiber-Schlüssel offenlegen.

## Entscheidung

Aufgezeichnete Läufe sind der Standard: strukturierte JSON-Aufzeichnungen werden
als Aufzeichnungen präsentiert und als solche gekennzeichnet. Live-Ausführung ist
optional und erfordert den eigenen Schlüssel des Besuchers (BYOK).

## Verworfene Alternativen

- Vom Betreiber finanzierte Live-Demo: Kosten- und Missbrauchsrisiko.
- Screenshots: nicht verifizierbar.

## Konsequenzen

- Keine Kosten, reproduzierbare Präsentation.
- Replay-Daten müssen aus echten Läufen stammen; erfundene Aufzeichnungen sind
  verboten.
- Replay ist ausdrücklich mit `execution_mode: live-ci` plus
  `kind: scripted-pipeline` gekennzeichnet, bis ein echter KI-Lauf existiert.

---

*Deutsche Fassung; maßgeblich ist die englische Originalfassung. Die Übersetzung kann hinter der englischen Version zurückliegen.*
