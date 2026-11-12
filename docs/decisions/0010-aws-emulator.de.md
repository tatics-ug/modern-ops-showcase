# ADR 0010 -- AWS-Emulation (Entscheidung vertagt)

**Deutsch** | [English](0010-aws-emulator.md)

- Status: proposed (kein Emulator gewählt, nichts implementiert)
- Datum: 2026-11-12
- Entscheider: Repository-Eigentümer

## Kontext

Eine AWS-Demo soll Cloud-Konzepte ohne AWS-Kosten zeigen. Ein Kandidat namens
„Floci“ wurde in der Spezifikation genannt, aber nicht verifiziert. LocalStack
ist der bekannteste Emulator; seine kostenlose Community-Edition hat begrenzte
API-Abdeckung und Lizenzbedingungen, die für die konkrete Version geprüft werden
müssen.

## Entscheidung

Noch keinen Emulator auswählen. Vor der Implementierung von Lab 07: das konkrete
Projekt, seinen Pflegestatus, seine API-Abdeckung, Lizenz und CI-Kompatibilität
prüfen. Echte AWS-Ressourcen bleiben deaktiviert und erfordern eine ausdrückliche
Freigabe mit Kostenschätzung, Region, TTL und Aufräumplan.

## Verworfene Alternativen

- LocalStack Community Edition: Abdeckung/Lizenz für die gewählte Ressource
  prüfen.
- Moto (Python-Mock): gut für Tests auf Unit-Ebene, kein vollständiger
  Endpoint-Emulator.
- Echtes AWS mit Budget-Alarm: kostet Geld, erfordert Freigabe.

## Konsequenzen

- Keine AWS-bezogene Aussage erscheint in der Dokumentation.
- Lab 07 bleibt `planned`, bis die Bewertung dokumentiert ist.

---

*Deutsche Fassung; maßgeblich ist die englische Originalfassung. Die Übersetzung kann hinter der englischen Version zurückliegen.*
