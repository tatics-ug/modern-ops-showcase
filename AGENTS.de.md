# AGENTS.md -- Regeln für Beitragende und KI-Agenten

**Deutsch** | [English](AGENTS.md)

Diese Datei gilt für jede Änderung in `tatics-ug/modern-ops-showcase`, ob von
Menschen oder automatisiert. Widerspricht eine Regel hier einer
Aufgabenstellung, stoppen und nachfragen.

## 1. Projekt in einem Absatz

ModernOps Showcase ist ein reproduzierbares Referenzprojekt für moderne
Infrastruktur und Agentic Engineering. Zwei Labs (Terraform-Lebenszyklus,
Kubernetes-Plattform) sind heute ausführbar; Website, Validierungs-Workflow und
die geskriptete Agentic-Referenz-Pipeline existieren ebenfalls. Alles andere ist
`planned` und muss als solches gekennzeichnet werden.

## 2. Architektur und Aufbau

| Pfad | Zweck |
| --- | --- |
| `labs/01-terraform-lifecycle/` | Terraform-Modul, State-Handling, Lifecycle-Skript |
| `labs/03-kubernetes-platform/` | kind-Cluster + von Terraform verwalteter Workload |
| `agents/` | geskriptete Agentenrollen (Triage, Planner, Implementer, Tester, Reviewer) |
| `.github/workflows/` | Validierungs-, Pages-, Demo- und Agentic-Workflows |
| `replay/` | Replay-Schema, Szenario, Aufzeichnungen echter Läufe |
| `evidence/` | Ergebnis-Schema und echte Beispielergebnisse |
| `docs/` | Architektur, Betrieb, Technologiematrix, ADRs |
| `website/` | MkDocs-Material-Seite (Build-Eingabe für GitHub Pages) |

Ausführlicher Kontext: [ARCHITECTURE.de.md](ARCHITECTURE.de.md),
[docs/decisions/](docs/decisions/).

## 3. Build- und Testbefehle

```bash
make demo-list                     # verfügbare Szenarien
make demo-run SCENARIO=01          # Terraform-Lab, vollständiger Lebenszyklus
make demo-run SCENARIO=03          # Kubernetes-Lab, vollständiger Lebenszyklus
make website                       # Seite lokal bauen (benötigt mkdocs-material)
make validate                      # Repository-Prüfungen (Python-Tests, Nachweise, YAML)
make clean-demo SCENARIO=01        # Lab-Artefakte entfernen
```

Befehle auf Lab-Ebene:

```bash
cd labs/01-terraform-lifecycle && make lifecycle
cd labs/03-kubernetes-platform && make lifecycle
```

## 4. Konventionen

- Dokumentation, Kommentare, Commit-Messages, PR-Text und Code: **Englisch**.
  Englisch ist die maßgebliche Sprache; jede Dokumentationsdatei existiert
  zusätzlich als deutsche Übersetzung (`*.de.md`), die mit gleicher Struktur
  gepflegt und in beide Richtungen verlinkt wird.
- Statusvokabular exakt: `planned`, `experimental`, `implemented`, `validated`.
- Formatierung: `terraform fmt` (Terraform), `python3 -m compileall` und
  `pytest`, `bash -n` für Shell-Skripte, `yamllint` für YAML.
- Ein Anliegen pro Commit; imperative, beschreibende Commit-Betreffzeile
  (`feat(lab03): ...`, `docs: ...`, `fix(ci): ...`).
- Keine hart kodierten absoluten Pfade, keine Benutzernamen, keine lokalen
  Maschinenspezifika.
- Neue Abhängigkeiten brauchen eine Begründung, eine gepinnte Version und eine
  freie/Open-Source-Lizenz.

## 5. Tests und Dokumentation

- Jedes hinzugefügte Verhalten braucht mindestens einen automatisierten Test
  oder eine dokumentierte Begründung, warum Testen unmöglich ist (dann muss es
  als `planned` gekennzeichnet werden).
- Jedes Lab erhält eine README mit: Zweck, Voraussetzungen, Architektur,
  Ausführungsanleitung, erwartetem Ergebnis, Tests, Fehlerfall, Aufräumen,
  Einschränkungen (plus die deutsche Fassung `README.de.md`).
- Dokumentations- und Website-Statustabellen müssen die Realität abbilden. Ein
  Lab darf nur dann `validated` sein, wenn ein echter Lauf einen Nachweis
  erzeugt hat.
- Test-Ergebnisse, Benchmarks, Kunden, Agenten-Läufe oder Cloud-Ressourcen nie
  erfinden.

## 6. Sicherheitsregeln (verbindlich)

- Niemals Secrets, Tokens, kubeconfigs, State-Dateien, private Schlüssel oder
  `.env`-Dateien committen. Nur `.env.example` mit Dummy-Werten verwenden.
- Workflows: explizite `permissions:` nach dem Prinzip der geringsten Rechte.
  Keine Secrets für unvertrauenswürdige Kontexte (`pull_request_target`, Fork-PRs,
  mit Rechten ausgeführter Issue-Text).
- Unvertrauenswürdigen Issue-/PR-Text niemals als Shell-Befehle ausführen oder
  ungeprüft an privilegierte Actions übergeben.
- Kein automatischer Merge, kein `gh pr merge`, kein Force-Push auf `main`.
- Cloud-Ressourcen: im Standardablauf nicht erlaubt. Jede bezahlte oder externe
  Ressource braucht eine ausdrückliche menschliche Freigabe, eine Kostenschätzung,
  eine Region, eine TTL und einen Aufräumplan.
- Destruktive Skripte müssen auf dedizierte Demo-Ressourcen beschränkt sein und
  vor dem Löschen den aufgelösten Pfad/das Ziel prüfen.

## 7. Verbotene Aktionen

- Secrets oder generierten State veröffentlichen.
- Cloud-Ressourcen (AWS oder andere) ohne ausdrückliche schriftliche Freigabe
  anlegen.
- Den LLM-API-Schlüssel des Repository-Eigentümers in einen öffentlichen
  Workflow aufnehmen.
- Agenten-Läufe, Replay-Daten, Test-Ergebnisse oder Reifegrad vortäuschen.
- Arbeit löschen oder überschreiben, ohne sie vorher gelesen zu haben.
- Git-Historie auf `main` umschreiben oder direkt in einen geschützten Branch
  pushen.

## 8. Wenn Anforderungen unklar sind

1. Die relevanten Dokumente und ADRs lesen.
2. Die kleinste umkehrbare Änderung bevorzugen.
3. Betrifft die Unklarheit Kosten, Sicherheit, Datenverlust oder irreversible
   Änderungen: stoppen und den Repository-Eigentümer fragen.
4. Die Entscheidung in `docs/decisions/` festhalten, wenn sie architektonisch ist.

## 9. Definition of Done

Eine Änderung ist fertig, wenn:

1. Ziel und Design dokumentiert sind (README/ADR, wie passend).
2. Die Voraussetzungen vollständig und reproduzierbar sind.
3. Ein automatisierter Test existiert und besteht.
4. Aufräumen dokumentiert und getestet ist.
5. Keine Secrets offengelegt sind und die CI grün bleibt.
6. Statustabellen/Website den echten Zustand zeigen.
7. Bekannte Einschränkungen dokumentiert sind.

---

*Deutsche Fassung; maßgeblich ist die englische Originalfassung. Die Übersetzung kann hinter der englischen Version zurückliegen.*
