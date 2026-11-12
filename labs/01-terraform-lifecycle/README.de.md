# Lab 01 -- Terraform-Infrastruktur-Lebenszyklus

**Deutsch** | [English](README.md)

Praxis-Lab, das den vollständigen Infrastructure-as-Code-Lebenszyklus mit
Terraform in einer kontrollierten Umgebung zeigt: **Format, Validate, Plan,
Apply, Verify, Drift erkennen, Destroy, Aufräumen**. Es verwendet den Provider
`hashicorp/local`, erzeugt also keine Cloud-Ressourcen und kostet nichts.
`terraform init` braucht einmalig Netzzugang, um den Provider herunterzuladen;
alles danach läuft offline.

Dateien werden nach `./workspace/` geschrieben. Nichts außerhalb dieses
Lab-Verzeichnisses wird berührt. Der State bleibt lokal und ist git-ignoriert.

Status: **lokal validiert** -- alle Akzeptanzkriterien sind durch automatisierte
Tests abgedeckt. Der GitHub-Actions-Workflow führt dasselbe Skript aus; den
Workflow-Lauf unter *Actions* findest du als CI-Nachweis.

---

## 1. Zweck

Das Lab beantwortet die Frage „Was macht Terraform eigentlich?“ mit
beobachtbarem Nachweis statt mit einer Konfigurationsdatei:

| Lebenszyklus-Schritt | Demonstriert durch | Nachweis |
| --- | --- | --- |
| Formatierung | `terraform fmt -check -recursive` | Exit-Code 0 |
| Validierung | `terraform validate` | Exit-Code 0 |
| Planung | `terraform plan -out=lab.tfplan` | gespeicherte Plan-Datei |
| Anwenden | `terraform apply lab.tfplan` | Dateien auf der Platte |
| Outputs | `terraform output -json` | Pfade, SHA-256, geschwärztes Secret |
| State | lokaler `terraform.tfstate` | git-ignoriert, durch Test geprüft |
| Idempotenz | zweiter `plan -detailed-exitcode` | Exit-Code 0 (keine Änderungen) |
| Fehlerfall | ungültiger Variablenwert | Validierungsfehler, Exit-Code != 0 |
| Abbau | `terraform destroy` | Workspace entfernt, State leer |

## 2. Voraussetzungen

- Terraform >= 1.6 (validiert mit 1.17.2) oder OpenTofu >= 1.6
- Python 3.9+ mit `pytest`
- `make` (nur Komfort-Targets, alle Befehle funktionieren auch ohne)
- Netzzugang für `terraform init` (Provider-Download), ~30 MB Speicherplatz

Die Installation von Terraform ist **nicht** Teil dieses Labs. Auf der
Referenzmaschine wurde es aus dem apt-Repository von HashiCorp installiert
(`noble`-Suite, da Linux Mint 22.2 auf Ubuntu 24.04 basiert); jede
Terraform-1.6+- oder OpenTofu-1.6+-Binärdatei funktioniert.

## 3. Architektur

```text
labs/01-terraform-lifecycle/
├── versions.tf              Terraform-/Provider-Versionsvorgaben, lokales Backend
├── providers.tf             Provider hashicorp/local
├── variables.tf             Eingaben + Validierungsregeln
├── main.tf                  Locals, Tag-Set, Modulaufruf
├── outputs.tf               Lifecycle-Outputs
├── terraform.tfvars.example Beispiel-Variablendatei
├── modules/demo_workspace/  wiederverwendbares Modul: Dateien + Template + sensible Datei
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── versions.tf
│   └── templates/runtime.conf.tftpl
├── tests/
│   ├── test_lab.py          pytest-Prüfung gegen den angewendeten Workspace
│   └── run_lifecycle.sh     vollständiger Lebenszyklus inkl. Aufräumen + Nachweis-JSON
└── Makefile                 dünner Wrapper um die obigen Befehle
```

Zur Laufzeit erzeugt: `workspace/`, `.terraform/`, `terraform.tfstate`,
`lab.tfplan`, `evidence/` -- alle git-ignoriert. `.terraform.lock.hcl` wird
ebenfalls erzeugt, **ist aber committet**, damit Provider-Versionen und -Hashes
reproduzierbar bleiben.

Das Verzeichnis `workspace/` enthält vier Artefakte:

| Datei | Modus | Zweck |
| --- | --- | --- |
| `metadata.json` | 0644 | maschinenlesbare Zusammenfassung, Tags, Provider |
| `runtime.conf` | 0644 | gerendert aus einem `templatefile()` |
| `demo-credential.txt` | 0600 | Dummy-„Secret“ über `local_sensitive_file` |
| `checksums.txt` | 0644 | SHA-256-Manifest der anderen Dateien |

## 4. Ausführen

```bash
cd labs/01-terraform-lifecycle
make lifecycle            # vollständiger Lauf, endet mit Destroy + Nachweis-JSON
```

oder Schritt für Schritt:

```bash
make init                 # Provider-Download, lokales Backend
make fmt-check            # Format-Gate
make validate
make plan                 # schreibt lab.tfplan
make apply
make output               # Pfade, Hash, geschwärzter sensibler Wert
make test                 # pytest-Prüfung
make destroy              # alle verwalteten Ressourcen entfernen
make clean                # lokale Arbeitsdaten und Artefakte entfernen
```

Ohne `make`:

```bash
terraform init -input=false
terraform fmt -check -recursive
terraform validate
terraform plan -input=false -out=lab.tfplan
terraform apply -input=false lab.tfplan
python3 -m pytest tests -q
terraform destroy -input=false -auto-approve
```

Engine-Auswahl: Jeder Befehl akzeptiert `TF=<binary>`, z. B.
`make TF=tofu lifecycle`. Die Testsuite übernimmt dieselbe Engine, sodass ein
OpenTofu-Lauf wirklich die OpenTofu-Binärdatei von Anfang bis Ende ausführt (das
HCL verwendet nur Konstrukte, die beide Werkzeuge unterstützen).

Einschränkung beim Wechsel der Engine: `tofu init` überschreibt die committete
`.terraform.lock.hcl` (Provider-Quelle `registry.opentofu.org`, andere Hashes).
Danach verweigert `terraform` den Start mit „Inconsistent dependency lock file“.
Entweder bei einer Engine bleiben oder die Lock-Datei vor dem Zurückwechseln mit
`git checkout -- .terraform.lock.hcl` wiederherstellen.

Erwartete Ergebnisse: `make plan` meldet **4 to add** in einem sauberen
Workspace; `make apply` schreibt die vier obigen Dateien; `make test` besteht
alle Tests; `make destroy` entfernt sie und lässt `terraform state list` leer
zurück.

## 5. Eingaben und Ausgaben

| Variable | Standard | Hinweise |
| --- | --- | --- |
| `workspace_dir` | `workspace` | relativ, muss im Lab bleiben, kein `..` |
| `workspace_name` | `lab01-demo` | `^[a-z][a-z0-9-]{2,30}$` |
| `environment` | `demo` | eines von `demo`, `dev`, `test` |
| `owner` | `modernops-showcase` | Tag-Wert |
| `file_permission` | `0644` | Oktalmodus für nicht sensible Dateien |
| `sensitive_demo_value` | Dummy-Platzhalter | als `sensitive` markiert, nie ein echtes Credential |

| Output | Bedeutung |
| --- | --- |
| `workspace_dir` | Pfad des Workspace, relativ zum Lab-Verzeichnis |
| `workspace_name` | zurückgegebene Eingabe |
| `metadata_path` | Pfad von `metadata.json`, relativ zum Lab-Verzeichnis |
| `metadata_sha256` | SHA-256, den Terraform als maßgeblich ansieht |
| `runtime_config_path` | Pfad von `runtime.conf`, relativ zum Lab-Verzeichnis |
| `file_count` | Anzahl der verwalteten Dateien (4) |
| `sensitive_demo_value` | in der CLI-Ausgabe geschwärzt (`sensitive = true`) |

## 6. Tests

`tests/test_lab.py` prüft das angewendete Ergebnis, nicht die Absicht:

- erzeugte Dateien existieren und passen zu `terraform output`
- Inhalt und SHA-256 von `metadata.json` passen zu Terraforms eigenem Hash
- `runtime.conf` wurde mit den erwarteten Werten aus dem Template erzeugt
- `checksums.txt` passt zu den Dateien auf der Platte
- Dateimodi sind `0644`/`0600` wie konfiguriert
- der sensible Output ist markiert und in der einfachen `terraform output`-Ausgabe
  geschwärzt
- die „Credential“-Datei enthält nur den Dummy-Platzhalter
- ein zweiter Plan hat keine Änderungen (Idempotenz)
- `workspace_name=Invalid_Name` und ein absoluter `workspace_dir` werden abgelehnt
- `terraform.tfstate` ist git-ignoriert (State wird nie veröffentlicht)

```bash
make apply   # Tests prüfen einen angewendeten Workspace
make test
```

## 7. Bewusster Fehlerfall

Zwei reproduzierbare Negativfälle existieren als Tests; beide scheitern *bevor*
etwas erzeugt wird:

```bash
terraform plan -var workspace_name=Invalid_Name
# Error: Invalid value for variable -> workspace_name must match ^[a-z][a-z0-9-]{2,30}$

terraform plan -var workspace_dir=/tmp/lab01-escape
# Error: Invalid value for variable -> workspace_dir must be a non-empty relative path
```

Der zweite Fall ist der wichtige: Er macht die Eigenschaft „dieses Lab kann nicht
außerhalb seines eigenen Verzeichnisses schreiben“ testbar statt angenommen.

## 8. State-Handling und Sicherheit

- Lokales Backend (`backend "local"`), es gibt also keinen Remote-State, keinen
  Bucket und kein Cloud-Konto.
- `terraform.tfstate` enthält den Dummy-Wert mit sensiblen Daten im Klartext. Das
  ist der Punkt der Demo: **sensible Outputs werden in der CLI geschwärzt, aber im
  State gespeichert**. Der State ist daher git-ignoriert und wird nie committet.
- `.terraform.lock.hcl` **ist** committet, damit Provider-Versionen und -Hashes
  reproduzierbar sind.
- Es sind keine Credentials nötig: Der Provider `local` braucht keine, und das
  einzige „Secret“ ist der dokumentierte Platzhalter.
- `.gitignore` (Repository-Wurzel) schließt `*.tfstate*`, `.terraform/`,
  `*.tfplan`, `workspace/` und `evidence/` aus; ein Test prüft, dass der State
  ignoriert wird.
- `tests/run_lifecycle.sh` löscht nur Pfade innerhalb dieses Lab-Verzeichnisses,
  abgesichert durch eine Pfad-Containment-Prüfung. Hinweis: Die Prüfung nutzt das
  logische `pwd` von bash, daher wird ein durch externe Manipulation erzeugtes
  symbolisch verlinktes `workspace/` als Link entfernt (das Linkziel selbst wird
  von `rm -rf` nie gelöscht).

Für den Produktiveinsatz würde der State in einem verschlüsselten Remote-Backend
mit Locking und eingeschränktem Zugriff liegen. Das ist hier als Lücke
dokumentiert, nicht simuliert.

## 9. Aufräumen

```bash
make destroy     # verwaltete Ressourcen zerstören (idempotent, mehrfach sicher)
make clean       # .terraform/, lab.tfplan, workspace/, evidence/, State entfernen
```

`tests/run_lifecycle.sh` zerstört auch bei Fehlern (best effort) und prüft, dass
das Workspace-Verzeichnis und der State danach leer sind.

## 10. CI

`.github/workflows/demo-terraform.yml` führt denselben Lebenszyklus auf
`ubuntu-latest` aus, mit `permissions: contents: read`, einem Limit über
`timeout-minutes` und `terraform destroy` in einem `always()`-Schritt. Es lädt
`evidence/` als Artefakt hoch. Der Workflow ist implementiert, aber **noch nicht
ausgeführt** (in dieser Umgebung gibt es kein Remote mit Actions); daher ist er
nicht als `validated` markiert.

## 11. Bekannte Einschränkungen

- Einzelmaschinen-Demo: kein Remote-Backend, kein State-Locking, kein
  Mehrbenutzer-Workflow.
- Der Provider-Download benötigt beim ersten `init` Netzwerk.
- Das „Secret“ ist ein dokumentierter Dummy; das Lab zeigt kein echtes
  Secret-Management (das ist ein späteres Lab).
- CI-Parität ist vorbereitet, nicht bewiesen.

## 12. Kompetenznachweis

| Aussage | Nachweis in diesem Lab |
| --- | --- |
| Terraform-Moduldesign | `modules/demo_workspace` mit typisierten, validierten Eingaben |
| Variablenvalidierung | drei Validierungsblöcke plus zwei Negativtests |
| Templates | `templatefile()` erzeugt `runtime.conf` |
| Outputs | sieben Outputs, einer sensibel |
| State-Bewusstsein | git-ignore-Test, dokumentiertes Klartext-State-Risiko |
| Idempotenz | `plan -detailed-exitcode`-Gate in Tests und Lifecycle-Skript |
| Lebenszyklus | `tests/run_lifecycle.sh` von init bis destroy mit Nachweis-JSON |
| Geringste Rechte | `permissions: contents: read`, keine Credentials verwendet |

---

*Deutsche Fassung; maßgeblich ist die englische Originalfassung. Die Übersetzung kann hinter der englischen Version zurückliegen.*
