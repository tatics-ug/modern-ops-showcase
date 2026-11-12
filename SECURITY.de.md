# Sicherheitsrichtlinie

**Deutsch** | [English](SECURITY.md)

## Sicherheitslücke melden

Bitte kein öffentliches Issue für Sicherheitsprobleme öffnen. Nutze die
**private Schwachstellenmeldung** von GitHub (Reiter „Security“ ->
„Report a vulnerability“) für dieses Repository. Eine Bestätigung erfolgt so
schnell wie möglich; dies ist ein Showcase-Projekt, das von einer einzelnen
Person gepflegt wird, daher bitte einige Tage Geduld.

## Geltungsbereich

Im Geltungsbereich: Workflow-Berechtigungen und Umgang mit Secrets, die
geskriptete Agentic-Pipeline und ihr Umgang mit unvertrauenswürdiger Eingabe,
die Kubernetes-Lab-Manifeste, die Terraform-Lab-Konfiguration und der
Website-Build.

Nicht im Geltungsbereich: Schwachstellen in Drittanbieter-Werkzeugen oder
-Actions selbst (bitte upstream melden) und die Sicherheit der lokalen Maschine
eines Besuchers.

## Sicherheitsmodell (wovon dieses Projekt ausgeht)

| Annahme | Umsetzung |
| --- | --- |
| Keine Secrets im Repository | `.gitignore` deckt State, kubeconfigs, `.env`, tfvars ab; zum Ausführen ist kein Secret nötig |
| CI nach dem Prinzip der geringsten Rechte | jeder Workflow setzt explizite `permissions:`; Standard ist `contents: read` |
| Keine Secrets für unvertrauenswürdige Eingabe | kein Workflow verwendet `pull_request_target`; Fork-PRs erhalten keine Secrets |
| Issue-Text ist Daten, kein Code | die Agentic-Pipeline parst Issue-Text, validiert ihn und berührt nur einen freigegebenen Pfad |
| Kein automatischer Merge | die Pipeline darf einen PR öffnen/aktualisieren, nie mergen; `main` ist geschützt |
| Keine Cloud- oder bezahlten Ressourcen | Labs laufen lokal und in kostenlosen CI-Runnern; AWS-Labs sind `planned` und deaktiviert |
| Reproduzierbare Provider | `.terraform.lock.hcl` ist committet; Provider-Versionen sind gepinnt |
| Container-Härtung (Lab) | Non-Root-UID, schreibgeschütztes Root-Dateisystem, alle Capabilities entfernt, seccomp `RuntimeDefault`, kein Service-Account-Token |

## Secrets

- Für keine Standard-Demo wird ein Credential benötigt. In diesem Repository
  und in seinen Workflows ist kein API-Schlüssel gespeichert.
- Live-KI-Läufe (BYOK) sind **nicht** implementiert. Falls dieser Modus später
  ergänzt wird, muss der Schlüssel ein Actions-Secret aus dem eigenen
  Fork/Environment des Besuchers sein, niemals ein Betreiber-Schlüssel und
  niemals für unvertrauenswürdige PRs verwendet. Siehe
  [docs/decisions/0007-byok-for-live-agent-runs.de.md](docs/decisions/0007-byok-for-live-agent-runs.de.md).
- Der Terraform-State kann sensible Werte im Klartext enthalten (in Lab 01
  demonstriert). Der State ist git-ignoriert und wird nie veröffentlicht.

## Branch-Schutz

`main` ist geschützt: Pull Requests erforderlich, mindestens ein
zustimmendes Review, Force-Pushes und Branch-Löschung deaktiviert. Änderungen an
Sicherheitsrichtlinien, Secrets, Berechtigungen oder kostenrelevanten Ressourcen
erfordern immer eine menschliche Freigabe (siehe AGENTS.md).

## Umgang mit Abhängigkeiten und Workflows

- GitHub Actions werden über Versions-Tag referenziert (`@v4`, `@v3`); das Pinnen
  auf Commit-SHAs ist ein empfohlener Härtungsschritt, der in
  [docs/RUNBOOK.de.md](docs/RUNBOOK.de.md) verfolgt wird.
- Sicherheitsfunktionen öffentlicher Repositories (Dependabot-Alerts,
  Push-Schutz für Secret-Scanning, wo kostenlos verfügbar) werden empfohlen,
  nicht stillschweigend aktiviert.
- Scanning: Trivy läuft im Validierungs-Workflow (Dateisystem-/Konfigurations-
  Scan); Ergebnisse werden als Workflow-Artefakte hochgeladen.

## Repository-Einstellungen, die dieses Modell erzwingen

| Einstellung | Wert | Warum |
| --- | --- | --- |
| Branch-Schutz auf `main` | PR erforderlich, 1 zustimmendes Review, kein Force-Push, keine Löschung | menschliches Gate für jede Änderung |
| Actions dürfen Pull Requests erstellen | auf Organisationsebene aktiviert | die geskriptete Pipeline öffnet PRs, kann sie aber nicht mergen oder freigeben |
| Standard-Workflow-Token | Nur-Lese-Rechte | Workflows müssen Schreibzugriff explizit anfordern |
| Pages-Quelle | GitHub Actions | nur statische Seite, kein Backend |
| Aufbewahrung von Artefakten | 14 Tage (Demos), 30 Tage (Agenten-Läufe) | veralteten, wachsenden Speicher vermeiden |

Das `gh`-Token des Eigentümers benötigt die Scopes `workflow` und `admin:org`
für die Repository-Administration; es wird nie in diesem Repository gespeichert
und nie innerhalb eines Workflows verwendet.

## Unterstützte Versionen

Nur der letzte Commit auf `main` wird unterstützt. Es gibt keine
veröffentlichten Versionen und kein Produktions-Deployment; die Website ist
statische Dokumentation.

---

*Deutsche Fassung; maßgeblich ist die englische Originalfassung. Die Übersetzung kann hinter der englischen Version zurückliegen.*
