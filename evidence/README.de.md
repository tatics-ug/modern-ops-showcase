# Nachweise

**Deutsch** | [English](README.md)

Strukturierter Beleg dafür, was tatsächlich ausgeführt wurde. Hier liegen zwei
Arten von Dokumenten:

| Ort | Inhalt | Erzeugt von |
| --- | --- | --- |
| `schema/scenario-result.schema.json` | JSON-Schema für ein Demo-Ergebnis | Repository |
| `examples/*.json` | **echte** Ergebnisse lokaler Läufe | `make demo-run`, Lifecycle-Skripte der Labs |
| `agent-runs/*.json`, `agent-runs/*.md` | Aufzeichnungen geskripteter Pipeline-Läufe | Workflow `agentic-issue` |

Workflow-Artefakte werden **nicht** committet (sie laufen ab); die committeten
Beispiele sind echte Läufe und tragen den `commit`, bei dem sie entstanden sind.
Wäre ein Dokument hier jemals veraltet, machen Zeitstempel und Commit das
sichtbar.

## Validieren

```bash
python3 scripts/validate_evidence.py          # benötigt jsonschema (requirements-dev.txt)
```

## Regeln

1. Ergebnisse nie erfinden. Ein Dokument in diesem Verzeichnis ist immer die
   Ausgabe eines echten Laufs, unverändert übernommen (nur der Dateiname darf
   abweichen).
2. Keine Secrets: Ergebnisse dürfen keine Credentials, Tokens, kubeconfigs oder
   personenbezogenen Daten enthalten.
3. Jedes Ergebnis listet `checks[]` mit echten Statuswerten und `limitations[]`
   mit den ehrlichen Lücken des Laufs.
4. Ausführungsmodi unterscheiden: `local` (Entwicklermaschine), `live-ci`
   (GitHub Actions) und `replay` (aufgezeichneter Lauf, der wiedergegeben wird).
5. Ein Szenario darf in der Doku nur dann als `validated` markiert werden, wenn
   ein bestandenes Ergebnis existiert.

## Beispieldokumente

- `examples/terraform-lifecycle.local.json` -- Lebenszyklus von Lab 01, lokaler
  Lauf, Status `passed`, 11 Checks.

Lab-03-Ergebnisse werden von `demo-kubernetes`-Läufen erzeugt und als
Workflow-Artefakte hochgeladen; das Lab bleibt `implemented`, bis hier auf einen
solchen Lauf verwiesen wird.

---

*Deutsche Fassung; maßgeblich ist die englische Originalfassung. Die Übersetzung kann hinter der englischen Version zurückliegen.*
