# ADR 0001 -- Ein Repository zu Beginn

**Deutsch** | [English](0001-single-repository.md)

- Status: accepted
- Datum: 2026-11-12
- Entscheider: Repository-Eigentümer

## Kontext

Das Showcase enthält Labs (Terraform, Kubernetes, später Ansible, GitOps,
Observability, DevSecOps, AWS-Emulation, KI-Infrastruktur), eine Website, CI und
eine Agentic-Pipeline. Eine Aufteilung in mehrere Repositories würde ab dem
ersten Tag CI-Setups, Secret-Umfang und Cross-Repository-Versionierung
vervielfachen.

## Entscheidung

Genau ein Repository verwenden (`tatics-ug/modern-ops-showcase`) und Module in
Verzeichnissen organisieren. Erst aufteilen, wenn ein konkreter technischer oder
organisatorischer Grund vorliegt.

## Verworfene Alternativen

- Ein Repository pro Lab: bessere Isolation, aber doppelte CI, mehr Pflegeaufwand.
- Monorepo plus veröffentlichte Artefakte: für ein Showcase unnötig.

## Konsequenzen

- Einfaches Onboarding, ein Branch-Schutz, ein Pages-Setup.
- Lab-Verzeichnisse müssen unabhängig bleiben (jedes hat eigene Makefile und
  eigenen State).
- Eine spätere Aufteilung bleibt möglich; nichts hängt am Monorepo-Layout.

---

*Deutsche Fassung; maßgeblich ist die englische Originalfassung. Die Übersetzung kann hinter der englischen Version zurückliegen.*
