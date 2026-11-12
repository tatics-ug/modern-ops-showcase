# ADR 0011 -- Prometheus + Grafana as the observability stack

- Status: proposed (planned for Lab 05)
- Date: 2026-11-12
- Deciders: repository owner

## Context

Observability is a core showcase area, but building several stacks in parallel is
wasteful. Prometheus/Grafana are the market standard for metrics and dashboards.

## Decision

Target Prometheus + Grafana + Alertmanager with the existing demo app as the
metric source, exposed in the kind cluster. Add Loki/OpenTelemetry later; do not
run alternatives (e.g. VictoriaMetrics, OpenSearch) in parallel.

## Alternatives considered

- Managed services: cost.
- Multiple stacks: maintenance and unclear message.

## Consequences

- One coherent story with real metrics (no fake dashboards).
- Requires a metrics endpoint in the demo app (currently only health endpoints),
  which is part of the Lab 05 work.
- Until implemented, no dashboard or alert is claimed.
