# ADR 0004 -- Temporary kind clusters for Kubernetes

- Status: accepted
- Date: 2026-11-12
- Deciders: repository owner

## Context

Kubernetes demos need a real cluster, but a managed cluster costs money and a
permanent local cluster is stateful and risky on a developer machine.

## Decision

Use `kind` (Kubernetes in Docker) with a project-specific cluster name
(`modernops-lab03`), created for a demo and deleted afterwards. Node image is
pinned (`kindest/node:v1.33.12`).

## Alternatives considered

- minikube: heavier, VM driver variations.
- k3d/k3s: also viable, but kind is the de-facto standard for CI Kubernetes.
- Managed clusters: costs money.

## Consequences

- No cloud cost, fast creation, disposable.
- Single node only; no scheduling/autoscaler demos.
- Requires a working Docker daemon on the machine or runner.
