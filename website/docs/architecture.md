# Architecture

ModernOps Showcase is a reference platform, not a product: small reproducible
scenarios plus the automation around them.

## Execution model

| Component | Runs on | Cost |
| --- | --- | --- |
| Website | GitHub Pages (static only) | free |
| Code, issues, PRs | GitHub | free |
| Validation and demos | GitHub Actions, standard runners | free for public repos |
| Terraform lab | local machine or Actions | free (local provider) |
| Kubernetes lab | Docker + kind, local or Actions | free |
| Agentic pipeline | GitHub Actions, no LLM | free |

GitHub Pages **never executes anything**. Demos run in Actions or locally.

## Repository layout

```text
labs/        executable scenarios (Terraform, Kubernetes)
agents/      scripted pipeline roles
replay/      schema, scenario, recordings of real runs
evidence/    result schema + real example results
website/     this site (MkDocs Material -> GitHub Pages)
docs/        getting started, runbook, technology matrix, ADRs
.github/     workflows and issue forms
```

## Trust boundaries

- Issue text is untrusted input: parsed, never executed, never interpolated into
  shell commands.
- Fork pull requests get no secrets and read-only tokens.
- The Kubernetes lab never pulls from a registry: the image is local.
- The agentic pipeline writes only to `evidence/agent-runs/` and
  `replay/recordings/`, and never merges.

## Decisions

Twelve Architecture Decision Records document the choices -- single repository,
GitHub Pages, Actions as execution layer, kind clusters, cluster/resource split,
replay as default mode, BYOK for future live runs, scripted orchestration, MkDocs
Material, AWS emulator (deferred), observability stack (planned), policy engine
(deferred).

[:octicons-arrow-right-24: All ADRs](https://github.com/tatics-ug/modern-ops-showcase/tree/main/docs/decisions)

## Known gaps

Labs 02, 04--09 are not implemented; the agentic pipeline is scripted, not AI;
Terraform state is local without locking; no observability stack yet.
