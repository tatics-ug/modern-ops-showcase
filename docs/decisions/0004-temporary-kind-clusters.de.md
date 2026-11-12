# ADR 0004 -- Temporäre kind-Cluster für Kubernetes

**Deutsch** | [English](0004-temporary-kind-clusters.md)

- Status: accepted
- Datum: 2026-11-12
- Entscheider: Repository-Eigentümer

## Kontext

Kubernetes-Demos brauchen einen echten Cluster, aber ein verwalteter Cluster
kostet Geld und ein dauerhafter lokaler Cluster ist zustandsbehaftet und riskant
auf einer Entwicklermaschine.

## Entscheidung

`kind` (Kubernetes in Docker) mit projektbezogenem Clusternamen
(`modernops-lab03`) verwenden, für eine Demo angelegt und danach gelöscht. Das
Node-Image ist gepinnt (`kindest/node:v1.33.12`).

## Verworfene Alternativen

- minikube: schwergewichtiger, Variationen bei den VM-Treibern.
- k3d/k3s: ebenfalls machbar, aber kind ist der De-facto-Standard für Kubernetes
  in CI.
- Verwaltete Cluster: kosten Geld.

## Konsequenzen

- Keine Cloud-Kosten, schnelle Erzeugung, wegwerfbar.
- Nur ein Node; keine Scheduling-/Autoscaler-Demos.
- Erfordert einen funktionierenden Docker-Daemon auf der Maschine oder dem Runner.

---

*Deutsche Fassung; maßgeblich ist die englische Originalfassung. Die Übersetzung kann hinter der englischen Version zurückliegen.*
