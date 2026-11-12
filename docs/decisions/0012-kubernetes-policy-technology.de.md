# ADR 0012 -- Kubernetes-Policy-Engine (Entscheidung vertagt)

**Deutsch** | [English](0012-kubernetes-policy-technology.md)

- Status: proposed (geplant für Lab 06)
- Datum: 2026-11-12
- Entscheider: Repository-Eigentümer

## Kontext

Policy-Durchsetzung (z. B. „keine privilegierten Pods“, „Images nur aus erlaubten
Registries“) ist eine gute DevSecOps-Demonstration. Kyverno und OPA/Gatekeeper
sind die beiden gängigen Optionen; beide gleichzeitig zu implementieren erhöht
die Komplexität ohne Vergleichsbedarf.

## Entscheidung

Die Wahl bis Lab 06 vertagen. Kyverno bevorzugen, wenn Policies in
Kubernetes-nativem YAML ausgedrückt werden sollen; OPA/Gatekeeper bevorzugen,
wenn Rego und die Wiederverwendung von Policies wichtiger sind. Genau eine
Variante implementieren.

## Verworfene Alternativen

- Beide Engines zum Vergleich: mehr Arbeit, kein MVP-Nutzen.
- Admission-Webhooks von Hand: das Rad neu erfinden.

## Konsequenzen

- Keine Policy-Engine im MVP; Lab 03 härtet den Workload stattdessen direkt
  (non-root, schreibgeschütztes Dateisystem, entfernte Capabilities).
- Die Entscheidung wird in Lab 06 mit konkreten Anforderungen überprüft.

---

*Deutsche Fassung; maßgeblich ist die englische Originalfassung. Die Übersetzung kann hinter der englischen Version zurückliegen.*
