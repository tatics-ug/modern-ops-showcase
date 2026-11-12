# ADR 0008 -- Geskriptete Agenten-Orchestrierung für das MVP

**Deutsch** | [English](0008-agentic-orchestration-path.md)

- Status: accepted
- Datum: 2026-11-12
- Entscheider: Repository-Eigentümer

## Kontext

Das MVP braucht eine echte Issue-zu-PR-Pipeline mit Triage, Plan, begrenzter
Änderung, Tests, unabhängigem Review und einem menschlichen Merge-Gate. Kandidaten
für die Orchestrierung sind GitHub Agentic Workflows (`gh-aw`) und Issue-/PR-
Agenten, die alle einen LLM-API-Schlüssel und damit Geld für beliebige Besucher
benötigen.

## Entscheidung

Die Orchestrierungsform als deterministische, regelbasierte Pipeline in GitHub
Actions implementieren (`agents/` + `agentic-issue`-Workflow), ausdrücklich als
„geskriptet, kein LLM“ gekennzeichnet. Im MVP weder `gh-aw` noch ein anderes
Agenten-Framework einführen.

## Verworfene Alternativen

- `gh-aw`: vielversprechend, erfordert Prüfung von Berechtigungen/Kosten und
  einen LLM-Schlüssel.
- Eigener Agent mit kostenloser API: Unsicherheit bei Kontingent/Nutzungs-
  bedingungen, nicht verlässlich.
- Nur manuelle Demonstration: verfehlt das MVP-Akzeptanzkriterium.

## Konsequenzen

- Kostenlos, reproduzierbar, prüfbar, kein Secret-Handling.
- Kein LLM-Reasoning: Die „Intelligenz“ ist der Workflow, kein Modell. Das wird
  überall genannt.
- Der Live-KI-Modus kann später hinter dem BYOK-Design ergänzt werden (ADR 0007).

---

*Deutsche Fassung; maßgeblich ist die englische Originalfassung. Die Übersetzung kann hinter der englischen Version zurückliegen.*
