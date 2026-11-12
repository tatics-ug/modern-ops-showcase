# Erste Schritte

Von einem frischen Clone zur erfolgreichen Demo in wenigen Minuten. Kein
Cloud-Konto, kein API-Schlüssel, keine GPU, keine Kosten.

## Voraussetzungen

| Werkzeug | Version | Für |
| --- | --- | --- |
| Terraform oder OpenTofu | >= 1.6 | Labs 01, 03 |
| Python | >= 3.9 (3.12 empfohlen) | Tests, Website, Pipeline |
| Docker | >= 24 | Lab 03 |
| kind | >= 0.2x | Lab 03 |
| kubectl | >= 1.28 | Lab 03 |
| make | GNU make | Komfortbefehle |

## Klonen und ausführen

```bash
git clone https://github.com/tatics-ug/modern-ops-showcase.git
cd modern-ops-showcase
make demo-list
make demo-run SCENARIO=01     # ~20 s, schreibt Nachweise
make demo-run SCENARIO=03     # ~4-8 min, benötigt Docker + kind
```

## Entwicklungsumgebung

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
python3 -m venv website/.venv
website/.venv/bin/pip install -r website/requirements.txt
make validate                  # Repo-Tests + Nachweis-Validierung + terraform fmt
make website-serve             # http://127.0.0.1:8000
```

## Sicherheitshinweise

- Im Standardablauf werden nirgends Credentials benötigt.
- Der State von Lab 01 enthält einen Dummy-Wert mit sensiblen Daten im Klartext
  -- der State ist git-ignoriert; niemals committen.
- Lab 03 verwaltet den Namespace `demo` nur in einem lokalen kind-Cluster. Nicht
  auf einen echten Cluster zeigen lassen.
- Niemals einen Betreiber-API-Schlüssel in einen Workflow aufnehmen. BYOK ist
  heute nur Design.

## Fehlerbehebung

- `docker: permission denied` -> Benutzer zur Gruppe `docker` hinzufügen, neu
  anmelden.
- kind-Erzeugung langsam -> `kindest/node:v1.33.12` vorab pullen.
- `Inconsistent dependency lock file` -> es wurde zwischen Terraform und OpenTofu
  gewechselt; Lock-Datei wiederherstellen oder bei einer Engine bleiben.
- `command not found: mkdocs` -> `make website` verwenden, das
  `website/.venv` bevorzugt.

Vollständiges Runbook: `docs/RUNBOOK.de.md` im Repository
([docs/](https://github.com/tatics-ug/modern-ops-showcase/tree/main/docs)).

---

*Deutsche Fassung; maßgeblich ist die englische Originalfassung. Die Übersetzung kann hinter der englischen Version zurückliegen.*
