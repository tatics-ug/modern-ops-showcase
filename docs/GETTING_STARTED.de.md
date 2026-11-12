# Erste Schritte

**Deutsch** | [English](GETTING_STARTED.md)

Diese Anleitung führt in wenigen Minuten von einem frischen Clone zu einem
erfolgreichen Demo-Lauf. Kein Cloud-Konto, kein API-Schlüssel, keine GPU, keine
Kosten.

## 1. Voraussetzungen

| Werkzeug | Version | Benötigt für |
| --- | --- | --- |
| Terraform *oder* OpenTofu | >= 1.6 | Lab 01, Lab 03 |
| Python | >= 3.9 (3.12 empfohlen) mit `pytest` | alle Tests, Website |
| Docker | >= 24 | Lab 03 (kind) |
| kind | >= 0.2x | Lab 03 |
| kubectl | >= 1.28 | Lab 03 |
| make | beliebiges GNU make | Komfortbefehle |

Optional: `mkdocs-material` (Website-Build), `shellcheck`, `yamllint` (lokale
Lint-Parität mit der CI).

### Terraform installieren (Ubuntu/Mint, kostenlos)

Das apt-Repository von HashiCorp ist der bequeme Weg. Unter Linux Mint ist der
Distributions-Codename (`zara`, `xia`, ...) **kein** HashiCorp-Suite-Name;
stattdessen den Ubuntu-Basis-Codename verwenden (`noble` für Mint 22.x):

```bash
sudo install -m 0755 -d /usr/share/keyrings
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com noble main" \
  | sudo tee /etc/apt/sources.list.d/hashicorp-terraform.list
sudo apt-get update && sudo apt-get install -y terraform
terraform version
```

OpenTofu funktioniert genauso über `make TF=tofu ...`.

### kind installieren (kostenlos, einzelne Binärdatei)

```bash
curl -fsSL -o kind https://github.com/kubernetes-sigs/kind/releases/download/v0.33.0/kind-linux-amd64
curl -fsSL -o kind.sha256sum https://github.com/kubernetes-sigs/kind/releases/download/v0.33.0/kind-linux-amd64.sha256sum
mv kind kind-linux-amd64 && sha256sum -c kind.sha256sum
install -m 0755 kind-linux-amd64 ~/.local/bin/kind
kind version
```

`~/.local/bin` muss im `PATH` liegen (auf Desktop-Linux ist das meist der Fall).

## 2. Erster Lauf

```bash
git clone https://github.com/tatics-ug/modern-ops-showcase.git
cd modern-ops-showcase
make demo-list
make demo-run SCENARIO=01     # Terraform-Lebenszyklus, ~20 s
```

Lab 01 legt Dateien unter `labs/01-terraform-lifecycle/workspace/` an, führt die
Tests aus, zerstört alles wieder und schreibt
`labs/01-terraform-lifecycle/evidence/local-lifecycle.json`.

Kubernetes-Lab (benötigt Docker und kind):

```bash
make demo-run SCENARIO=03     # ~4-8 min: Cluster hoch, Deployment, Fehler, Fix, Aufräumen
```

## 3. Ergebnisse prüfen

```bash
make demo-list                        # Szenario-Überblick
python3 scripts/validate_evidence.py  # alle Nachweis-Dokumente validieren
cat labs/01-terraform-lifecycle/evidence/local-lifecycle.json
```

Nachweis-Dokumente werden gegen
`evidence/schema/scenario-result.schema.json` validiert. Committete Beispiele
liegen in `evidence/examples/` und sind echte Läufe (siehe ihr Feld `commit`).

## 4. Website lokal

```bash
python3 -m venv website/.venv
website/.venv/bin/pip install -r website/requirements.txt
make website-serve            # http://127.0.0.1:8000
make website                  # Build nach website/site (git-ignoriert)
```

Die Seite wird in der CI gebaut und von
`.github/workflows/deploy-pages.yml` auf GitHub Pages veröffentlicht.

## 5. Sicherheitshinweise

- Nichts im Standardablauf benötigt Credentials, und es sind keine gespeichert.
- Der State von Lab 01 enthält einen **Dummy**-Wert mit sensiblen Daten im
  Klartext. Das ist der Lerneffekt; der State ist git-ignoriert.
- Lab 03 legt einen lokalen kind-Cluster namens `modernops-lab03` an und löscht
  ihn am Ende wieder. Andere Cluster werden nie berührt.
- Die Labs nicht mit einer kubeconfig ausführen, die auf einen echten Cluster
  zeigt: Das Terraform von Lab 03 verwaltet den Namespace `demo` und würde ihn
  bei `destroy` löschen.

## 6. Fehlerbehebung

Siehe [RUNBOOK.de.md](RUNBOOK.de.md). Die häufigsten Probleme: kein Docker-Zugriff,
kind-Node-Image noch nicht heruntergeladen, Provider-Download hinter einem Proxy,
veraltetes `.terraform`-Verzeichnis nach dem Wechsel zwischen Terraform und
OpenTofu.

---

*Deutsche Fassung; maßgeblich ist die englische Originalfassung. Die Übersetzung kann hinter der englischen Version zurückliegen.*
