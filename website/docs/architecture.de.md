# Architektur

ModernOps Showcase ist eine Referenzplattform, kein Produkt: kleine
reproduzierbare Szenarien plus die Automatisierung darum herum.

## Ausführungsmodell

| Komponente | Läuft auf | Kosten |
| --- | --- | --- |
| Website | GitHub Pages (nur statisch) | kostenlos |
| Code, Issues, PRs | GitHub | kostenlos |
| Validierung und Demos | GitHub Actions, Standard-Runner | kostenlos für öffentliche Repos |
| Terraform-Lab | lokale Maschine oder Actions | kostenlos (lokaler Provider) |
| Kubernetes-Lab | Docker + kind, lokal oder Actions | kostenlos |
| Agentic-Pipeline | GitHub Actions, kein LLM | kostenlos |

GitHub Pages **führt nie etwas aus**. Demos laufen in Actions oder lokal.

## Repository-Aufbau

```text
labs/        ausführbare Szenarien (Terraform, Kubernetes)
agents/      Rollen der geskripteten Pipeline
replay/      Schema, Szenario, Aufzeichnungen echter Läufe
evidence/    Ergebnis-Schema + echte Beispielergebnisse
website/     diese Seite (MkDocs Material -> GitHub Pages)
docs/        Erste Schritte, Runbook, Technologiematrix, ADRs
.github/     Workflows und Issue-Formulare
```

## Vertrauensgrenzen

- Issue-Text ist unvertrauenswürdige Eingabe: geparst, nie ausgeführt, nie in
  Shell-Befehle interpoliert.
- Fork-Pull-Requests erhalten keine Secrets und Nur-Lese-Token.
- Das Kubernetes-Lab zieht nie aus einer Registry: Das Image ist lokal.
- Die Agentic-Pipeline schreibt nur nach `evidence/agent-runs/` und
  `replay/recordings/` und merged nie.

## Entscheidungen

Zwölf Architecture Decision Records dokumentieren die Entscheidungen: ein
Repository, GitHub Pages, Actions als Ausführungsschicht, kind-Cluster, Trennung
von Cluster und Ressourcen, Replay als Standardmodus, BYOK für künftige
Live-Läufe, geskriptete Orchestrierung, MkDocs Material, AWS-Emulator (vertagt),
Observability-Stack (geplant), Policy-Engine (vertagt).

[:octicons-arrow-right-24: Alle ADRs](https://github.com/tatics-ug/modern-ops-showcase/tree/main/docs/decisions)

## Bekannte Lücken

Labs 02, 04--09 sind nicht implementiert; die Agentic-Pipeline ist geskriptet,
nicht KI; der Terraform-State ist lokal ohne Locking; einen Observability-Stack
gibt es noch nicht.

---

*Deutsche Fassung; maßgeblich ist die englische Originalfassung. Die Übersetzung kann hinter der englischen Version zurückliegen.*
