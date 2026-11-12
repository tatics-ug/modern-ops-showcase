# ModernOps Showcase

**Modern Infrastructure & Agentic Engineering** -- a reproducible, hands-on
showcase for modern infrastructure and agentic engineering. Explore Linux
automation, Terraform, Kubernetes, GitOps, CI/CD, observability, security and
AI-powered software engineering -- integrated in one transparent reference
project.

Website: <https://modern-ops-showcase.tatics.de> (custom domain planned) --
repository: <https://github.com/tatics-ug/modern-ops-showcase>

Every capability in this repository is either **actually executable** or
honestly labelled as planned. Nothing here is a screenshot of something that
does not exist.

---

## What is inside

| Area | Contents | Status |
| --- | --- | --- |
| Lab 01 | Terraform infrastructure lifecycle (modules, state, idempotency, destroy) | `validated` (local) |
| Lab 03 | Kubernetes application platform (kind, Terraform, probes, fault case) | `validated` (CI) |
| Lab 02, 04--09 | Ansible, Argo CD, observability, DevSecOps, AWS emulation, agentic lab, AI infrastructure | `planned` |
| CI/CD | Validation workflow, pages deployment, demo workflows | `implemented` |
| Website | MkDocs Material site published via GitHub Pages | `implemented` |
| Agentic engineering | Scripted reference pipeline (no LLM) + replay schema + BYOK design | `validated` (first real run: PR #2, pending human merge) |

Status vocabulary: `planned` -- described only, `experimental` -- exists but is
not reproducible yet, `implemented` -- code and tests exist, `validated` --
executed successfully and evidence is linked.

## Quick start

```bash
make demo-list                 # list available demo scenarios
make demo-up SCENARIO=01       # prepare a scenario
make demo-run SCENARIO=01      # execute it (writes evidence)
make demo-down SCENARIO=01     # remove everything again
```

Requirements for the labs: Terraform >= 1.6 (or OpenTofu >= 1.6), Python 3.12
with `pytest`, Docker, `kind`, `kubectl`, `make`. No cloud account, no API key,
no GPU.

## Repository structure

```text
.github/            workflows (validation, pages, demos, agentic pipeline), issue forms
agents/             scripted agent roles (triage, planner, implementer, tester, reviewer)
docs/               architecture, security, operations, technology matrix, ADRs
evidence/           result schema + real example results
labs/01-terraform-lifecycle/   Terraform lifecycle lab
labs/03-kubernetes-platform/   Kubernetes platform lab (kind + Terraform)
replay/             replay schema, scenarios and recordings of real runs
scripts/            repository tooling (evidence validation)
tests/              repository-wide tests
website/            MkDocs Material site (published to GitHub Pages)
```

## How it is executed

| Piece | Runs on |
| --- | --- |
| Website | GitHub Pages (static only, no backend) |
| Code, docs, issues, PRs | GitHub |
| Validation and demo workflows | GitHub Actions (free runners for public repositories) |
| Labs | local machine (Docker, kind, Terraform) and GitHub Actions |
| Cloud resources | none in the standard run; AWS is only an optional future demo |

## Cost and dependencies

Everything used here is free of charge: GitHub Free organisation with public
repositories, standard GitHub-hosted runners (free for public repositories),
GitHub Pages, and locally installed open-source tools (Terraform/OpenTofu,
kind, kubectl, Docker, Python, MkDocs Material, Terraform providers).

No AWS account, no paid API, no credit card is required. Ideas that would cost
money (real AWS resources, live LLM runs) are documented as *optional* and
disabled by default; see [docs/decisions](docs/decisions).

## Documentation

- [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md) -- prerequisites, local run, security notes
- [docs/RUNBOOK.md](docs/RUNBOOK.md) -- operate and troubleshoot the demos
- [docs/TECHNOLOGY_MATRIX.md](docs/TECHNOLOGY_MATRIX.md) -- every technology with an honest status
- [docs/AGENT_WORKFLOW.md](docs/AGENT_WORKFLOW.md) -- triage/plan/implement/test/review pipeline
- [ARCHITECTURE.md](ARCHITECTURE.md) -- system overview and execution model
- [SECURITY.md](SECURITY.md) -- security model, reporting, secret handling
- [AGENTS.md](AGENTS.md) -- rules for human and AI contributors
- [evidence/](evidence/README.md) -- result format and real example results

## Agentic engineering in one paragraph

GitHub issues are the task source. A GitHub Actions pipeline checks the issue
(triage), derives a bounded plan, applies a whitelisted change, runs the tests,
performs an independent rule-based review, and opens a pull request. The
pipeline contains **no LLM**: it is a deterministic reference implementation of
the orchestration shape and is labelled as such everywhere. A full replay of a
real run is stored under [replay/](replay/README.md). Live AI runs are a
separate, optional BYOK mode that is **not** enabled in this repository; no
operator key is ever exposed.

## Evidence

| Source | Link |
| --- | --- |
| Validation workflow | https://github.com/tatics-ug/modern-ops-showcase/actions/runs/43256482921 |
| Lab 01 lifecycle in CI | https://github.com/tatics-ug/modern-ops-showcase/actions/runs/43254091400 |
| Lab 03 lifecycle in CI | https://github.com/tatics-ug/modern-ops-showcase/actions/runs/43256482922 |
| Website deployment | https://github.com/tatics-ug/modern-ops-showcase/actions/runs/43256483294 |
| First real agentic pipeline run | https://github.com/tatics-ug/modern-ops-showcase/actions/runs/43255005540 (pull request #2) |

## License

[MIT](LICENSE)
