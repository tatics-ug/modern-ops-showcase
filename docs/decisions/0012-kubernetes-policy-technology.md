# ADR 0012 -- Kubernetes policy engine (decision deferred)

- Status: proposed (planned for Lab 06)
- Date: 2026-11-12
- Deciders: repository owner

## Context

Policy enforcement (e.g. "no privileged pods", "images from allowed registries")
is a good DevSecOps demonstration. Kyverno and OPA/Gatekeeper are the two common
choices; implementing both at once adds complexity without a comparison need.

## Decision

Defer the choice until Lab 06. Prefer Kyverno if policies should be expressed in
Kubernetes-native YAML; prefer OPA/Gatekeeper if Rego and policy reuse matter
more. Implement exactly one.

## Alternatives considered

- Both engines for comparison: more work, no MVP value.
- Admission webhooks by hand: reinventing the wheel.

## Consequences

- No policy engine in the MVP; Lab 03 hardens the workload directly instead
  (non-root, read-only fs, dropped capabilities).
- The decision is revisited with concrete requirements in Lab 06.
