# ModernOps Showcase

**Modern Infrastructure & Agentic Engineering** -- a reproducible, hands-on
showcase. Explore Linux automation, Terraform, Kubernetes, cloud infrastructure,
CI/CD, observability, security and AI-powered software engineering, integrated in
one transparent reference project.

[:octicons-arrow-right-24: Browse the labs](labs/index.md){ .md-button .md-button--primary }
[:octicons-mark-github-16: Source code](https://github.com/tatics-ug/modern-ops-showcase){ .md-button }

## What you can actually run

| Lab | What it demonstrates | Status |
| --- | --- | --- |
| Lab 01 | Terraform lifecycle: modules, validation, plan/apply, state, destroy, drift | `validated` (local) |
| Lab 03 | Kubernetes platform on kind: deployment, probes, limits, fault case | `validated` (CI) |

Everything else in this project (Ansible, GitOps, observability, DevSecOps,
AWS emulation, AI infrastructure) is **planned** and labelled as such. No
dashboard, metric or benchmark on this site is fake -- if it is not implemented,
it says so.

## How the project is built

- **Infrastructure as code** with Terraform, local state, reproducible plans.
- **Real Kubernetes workloads** in a temporary kind cluster that is deleted after
  the demo, so nobody pays for idle resources.
- **Automated proof**: every lab run writes a structured evidence document.
- **CI on GitHub Actions** with least-privilege permissions and free runners.
- **Agentic engineering**: a scripted issue-to-PR pipeline with triage, plan,
  bounded change, tests, independent review, PR and a human merge gate.

## Free by design

No cloud account, no API key, no GPU, no credit card. The whole showcase runs on
free tooling: GitHub Free, GitHub Pages, standard GitHub-hosted runners (free for
public repositories), Terraform, kind, Docker, Python and MkDocs Material.

!!! warning "Honest labelling"
    Live AI agent runs are **not** enabled. The agentic pipeline in this
    repository is deterministic and contains no language model; that is stated
    on every artefact it produces.
