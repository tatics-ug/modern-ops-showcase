# ADR 0005 -- Separate cluster creation from Terraform resource management

- Status: accepted
- Date: 2026-11-12
- Deciders: repository owner

## Context

The Kubernetes provider of Terraform manages resources in an existing cluster; it
does not create the cluster. Mixing both responsibilities into one apply hides the
dependency and makes `destroy` risky.

## Decision

The lab script creates the kind cluster and its kubeconfig, then Terraform
manages only namespaced objects (`namespace`, `configmap`, `deployment`,
`service`). Terraform output/state never references the cluster as a resource.

## Alternatives considered

- Terraform also calling kind via provisioners: needs local-exec, opaque errors,
  destroy ordering problems.
- Cluster Terraform providers (e.g. for managed services): costs money, cloud
  coupling.

## Consequences

- `terraform destroy` can never delete the cluster.
- Two steps must be documented (`cluster-up` before `apply`).
- The same split generalises to real clusters later.
