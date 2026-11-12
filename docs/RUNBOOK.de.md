# Runbook

**Deutsch** | [English](RUNBOOK.md)

Betriebsabläufe für das Showcase. Nichts hier benötigt bezahlte Dienste.

## 1. Ausführbare Szenarien

| Szenario | Befehl | Dauer | Erzeugt | Entfernt |
| --- | --- | --- | --- | --- |
| 01 Terraform-Lebenszyklus | `make demo-run SCENARIO=01` | ~20 s | Dateien in `labs/01-terraform-lifecycle/workspace/` | `make demo-down SCENARIO=01` |
| 03 Kubernetes-Plattform | `make demo-run SCENARIO=03` | 4-8 min | kind-Cluster `modernops-lab03`, Namespace `demo` | `make demo-down SCENARIO=03` |

Beide schreiben ein Nachweis-JSON (`labs/*/evidence/`), das git-ignoriert ist;
die CI lädt es als Artefakt hoch.

## 2. Routineprüfungen

```bash
make validate                 # Repo-Tests + Nachweis-Schema + terraform fmt
make website                  # strikter MkDocs-Build
```

Die CI führt dieselben Prüfungen aus, zusätzlich YAML-, Shell- und
Workflow-Linting sowie einen Trivy-Dateisystem-Scan
(`.github/workflows/validate.yml`).

## 3. Fehlerbehandlung

### Lab 01

| Symptom | Ursache | Lösung |
| --- | --- | --- |
| `Inconsistent dependency lock file` | Engine gewechselt (tofu <-> terraform) und Lock-Datei überschrieben | bei einer Engine bleiben oder `git checkout -- labs/01-terraform-lifecycle/.terraform.lock.hcl` |
| `terraform init` erreicht die Registry nicht | offline/Proxy | `HTTPS_PROXY` konfigurieren oder `.terraform/` vorab befüllen |
| Nachweis fehlt nach einem Fehler | der Nachweis-Schreiber selbst ist fehlgeschlagen (z. B. defektes `PYTHON`) | mit funktionierendem `python3` erneut ausführen; eine veraltete Nachweis-Datei wird nie von einem defekten Schreiber überschrieben |
| zweiter Plan meldet Änderungen | manuelle Änderung in `workspace/` | erwartete Drift; `terraform apply` stellt den Zustand wieder her |

### Lab 03

| Symptom | Ursache | Lösung |
| --- | --- | --- |
| `docker: permission denied` | Benutzer nicht in der Gruppe `docker` | Benutzer zu `docker` hinzufügen, neu anmelden |
| kind-Cluster-Erzeugung läuft in ein Timeout | Node-Image-Download langsam | zuerst `docker pull kindest/node:v1.33.12`, dann erneut versuchen |
| Pods in `ErrImageNeverPull` während der Gesund-Tests | Image nicht in kind geladen | `make load` nach `make build` |
| `terraform destroy` schlägt fehl | Cluster wurde bereits manuell gelöscht | lokalen State löschen: `labs/03-kubernetes-platform/terraform/terraform.tfstate` |
| Port 30080 bereits belegt | anderer Dienst nutzt den gemappten Port | `extraPortMappings` in `kind/kind-config.yaml` ändern |

## 4. Aufräumen und Zurücksetzen

```bash
make demo-reset SCENARIO=01    # Terraform-Ressourcen zerstören, Workspace-Dateien entfernen
make demo-down  SCENARIO=01    # Reset + lokale Terraform-Arbeitsdaten entfernen
make demo-down  SCENARIO=03    # Ressourcen zerstören + kind-Cluster löschen
docker ps                      # prüfen, dass keine modernops-Container übrig sind
kind get clusters              # prüfen, dass modernops-lab03 weg ist
```

## 5. GitHub-Workflows

| Workflow | Auslöser | Zweck |
| --- | --- | --- |
| `validate` | Push, PR | Repository-Prüfungen, Website-Build, Trivy |
| `deploy-pages` | Push auf `main` | Seite bauen und auf GitHub Pages veröffentlichen |
| `demo-terraform` | Push/PR mit Änderungen an Lab 01, manuell | Lab-01-Lebenszyklus in der CI |
| `demo-kubernetes` | Push/PR mit Änderungen an Lab 03, manuell | Lab-03-Lebenszyklus mit kind |
| `agentic-issue` | Issue mit Label `agent:task`, manuell | geskriptete Triage/Plan/Implement/Test/Review, öffnet einen PR |

Alle Workflows verwenden `permissions:` mit dem minimal nötigen Umfang, und
kein Workflow hat Zugriff auf ein bezahltes Secret.

## 6. GitHub Pages und eigene Domain

Pages ist mit **GitHub Actions** als Quelle konfiguriert. Für die eigene Domain
`modern-ops-showcase.tatics.de` muss ein DNS-Eintrag von der Stelle angelegt
werden, die die Zone `tatics.de` kontrolliert (dieses Projekt ändert kein DNS):

1. `CNAME` `modern-ops-showcase.tatics.de` -> `tatics-ug.github.io` anlegen.
2. Im Repository: Settings -> Pages -> Custom domain ->
   `modern-ops-showcase.tatics.de`, speichern.
3. „Enforce HTTPS“ aktivieren, sobald GitHub das Zertifikat ausgestellt hat.
4. Prüfen: `dig +short modern-ops-showcase.tatics.de CNAME` und die Seite öffnen.

Typische Probleme: Der CNAME zeigt noch auf den alten Host, die Domain ist von
einem anderen Repository belegt, oder HTTPS wird aktiviert, bevor das Zertifikat
existiert.

## 7. Repository-Pflege

- Actions sind über Tag gepinnt; das Pinnen auf Commit-SHAs ist ein empfohlener
  Härtungsschritt (erfordert einen PR, da `main` geschützt ist).
- Dependabot-Alerts können in den Repository-Einstellungen aktiviert werden
  (kostenlos für öffentliche Repositories); automatische PRs sind bewusst nicht
  konfiguriert.
- Nachweis-Artefakte werden 14 Tage aufbewahrt (Demo-Workflows), um den Speicher
  klein zu halten.

## 8. Für dieses Projekt gesetzte Repository-Einstellungen (kostenlose Tarife)

| Einstellung | Wert |
| --- | --- |
| Sichtbarkeit | öffentlich |
| Pages | Quelle GitHub Actions, HTTPS erzwungen |
| Organisationsrichtlinie | „Actions may create pull requests“ aktiviert (Merge bleibt weiterhin nur für Menschen möglich) |
| Standard-Workflow-Berechtigungen | Nur-Lese-Rechte |
| Labels | `agent:task`, `docs` |
| Branch-Schutz | siehe SECURITY.de.md |

Die Richtlinie „Actions may create pull requests“ ist eine Einstellung auf
Organisationsebene und benötigt den Scope `admin:org`. Sie ist nötig, weil die
geskriptete Pipeline den PR mit `GITHUB_TOKEN` öffnet; das Token kann weiterhin
nicht mergen oder freigeben.

## 9. Eskalation

Nur der Repository-Eigentümer kann Sicherheitsrichtlinien, Branch-Schutz,
Secrets oder kostenrelevante Einstellungen ändern. Alles, was bezahlte
Ressourcen erzeugen würde, muss ausdrücklich freigegeben und vorher mit
Kostenschätzung, Region, TTL und Aufräumplan dokumentiert werden.

---

*Deutsche Fassung; maßgeblich ist die englische Originalfassung. Die Übersetzung kann hinter der englischen Version zurückliegen.*
