# ADR 0011 -- Prometheus + Grafana als Observability-Stack

**Deutsch** | [English](0011-observability-stack.md)

- Status: proposed (geplant für Lab 05)
- Datum: 2026-11-12
- Entscheider: Repository-Eigentümer

## Kontext

Observability ist ein Kernbereich des Showcase, aber mehrere Stacks parallel zu
bauen ist verschwenderisch. Prometheus/Grafana sind der Marktstandard für Metriken
und Dashboards.

## Entscheidung

Auf Prometheus + Grafana + Alertmanager setzen, mit der bestehenden Demo-App als
Metrikquelle, bereitgestellt im kind-Cluster. Loki/OpenTelemetry später ergänzen;
keine Alternativen (z. B. VictoriaMetrics, OpenSearch) parallel betreiben.

## Verworfene Alternativen

- Verwaltete Dienste: Kosten.
- Mehrere Stacks: Pflegeaufwand und unklare Botschaft.

## Konsequenzen

- Eine kohärente Geschichte mit echten Metriken (keine Fake-Dashboards).
- Erfordert einen Metrics-Endpunkt in der Demo-App (derzeit gibt es nur
  Health-Endpunkte), was Teil der Lab-05-Arbeit ist.
- Bis zur Implementierung werden kein Dashboard und kein Alert behauptet.

---

*Deutsche Fassung; maßgeblich ist die englische Originalfassung. Die Übersetzung kann hinter der englischen Version zurückliegen.*
