# ADR 0007 -- BYOK für Live-Agenten-Läufe (nicht implementiert)

**Deutsch** | [English](0007-byok-for-live-agent-runs.md)

- Status: proposed (nur Design, bewusst deaktiviert)
- Datum: 2026-11-12
- Entscheider: Repository-Eigentümer

## Kontext

Ein Live-KI-Modus ist attraktiv, darf aber niemals den API-Schlüssel des
Repository-Eigentümers für beliebige Besucher verwenden und niemals Secrets an
Fork-Workflows preisgeben.

## Entscheidung (Design)

Falls der Live-Modus implementiert wird: Der Besucher stellt seinen eigenen
Schlüssel über ein Environment-Secret oder ein von ihm kontrolliertes
Repository/Environment bereit, der Workflow läuft nur über
`workflow_dispatch` (nie automatisch bei Issues/PRs), Kosten und Limits werden
angezeigt, und der Schlüssel wird nie protokolliert. Bis dahin bleibt der
Live-Modus deaktiviert.

## Verworfene Alternativen

- Betreiber-Schlüssel: verboten (öffentliches Kosten-/Missbrauchsrisiko).
- Gemeinsames Demo-Konto: weiterhin vom Betreiber finanziert.

## Konsequenzen

- Heute keine Kosten und kein Secret-Risiko.
- Die Agentic-Demo bleibt geskriptet; das wird auf der Website und in der
  Pipeline-Ausgabe genannt.

---

*Deutsche Fassung; maßgeblich ist die englische Originalfassung. Die Übersetzung kann hinter der englischen Version zurückliegen.*
