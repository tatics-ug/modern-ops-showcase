# AGENTS.md -- Rules for contributors and AI agents

This file applies to every change in `tatics-ug/modern-ops-showcase`, human or
automated. If a rule here conflicts with a task instruction, stop and ask.

## 1. Project in one paragraph

ModernOps Showcase is a reproducible reference project for modern
infrastructure and agentic engineering. Two labs (Terraform lifecycle,
Kubernetes platform) are executable today; the website, validation workflow and
the scripted agentic reference pipeline exist as well. Everything else is
`planned` and must be labelled as such.

## 2. Architecture and layout

| Path | Purpose |
| --- | --- |
| `labs/01-terraform-lifecycle/` | Terraform module, state handling, lifecycle script |
| `labs/03-kubernetes-platform/` | kind cluster + Terraform-managed workload |
| `agents/` | scripted agent roles (triage, planner, implementer, tester, reviewer) |
| `.github/workflows/` | validation, pages, demo and agentic workflows |
| `replay/` | replay schema, scenario, recordings of real runs |
| `evidence/` | result schema and real example results |
| `docs/` | architecture, operations, technology matrix, ADRs |
| `website/` | MkDocs Material site (build input for GitHub Pages) |

Detailed context: [ARCHITECTURE.md](ARCHITECTURE.md),
[docs/decisions/](docs/decisions/).

## 3. Build and test commands

```bash
make demo-list                     # available scenarios
make demo-run SCENARIO=01          # Terraform lab, full lifecycle
make demo-run SCENARIO=03          # Kubernetes lab, full lifecycle
make website                       # build the site locally (needs mkdocs-material)
make validate                      # repository checks (python tests, evidence, yaml)
make clean-demo SCENARIO=01        # remove lab artifacts
```

Lab-level commands:

```bash
cd labs/01-terraform-lifecycle && make lifecycle
cd labs/03-kubernetes-platform && make lifecycle
```

## 4. Conventions

- Documentation, comments, commit messages, PR text and code: **English**.
- Status vocabulary exactly: `planned`, `experimental`, `implemented`, `validated`.
- Formatting: `terraform fmt` (Terraform), `python3 -m compileall` and `pytest`,
  `bash -n` for shell scripts, `yamllint` for YAML.
- One concern per commit; imperative, descriptive commit subject
  (`feat(lab03): ...`, `docs: ...`, `fix(ci): ...`).
- No hard-coded absolute paths, no user names, no local machine specifics.
- New dependencies need a reason, a pinned version and a free/open-source license.

## 5. Tests and documentation

- Every behaviour you add needs at least one automated test or a documented
  reason why testing is impossible (and then it must be marked `planned`).
- Every lab gets a README with: purpose, prerequisites, architecture, run
  instructions, expected result, tests, failure case, cleanup, limitations.
- Documentation and website status tables must match reality. A lab may only be
  `validated` if a real run produced evidence.
- Never invent test results, benchmarks, customers, agent runs or cloud resources.

## 6. Security rules (mandatory)

- Never commit secrets, tokens, kubeconfigs, state files, private keys or
  `.env` files. Use `.env.example` with dummy values only.
- Workflows: explicit least-privilege `permissions:`. No secrets for untrusted
  contexts (`pull_request_target`, fork PRs, issue text executed with privileges).
- Never run untrusted issue/PR text as shell commands or pass it to privileged
  actions unvalidated.
- No automatic merge, no `gh pr merge`, no force-push to `main`.
- Cloud resources: not allowed in the standard flow. Any paid or external
  resource needs explicit human approval, a cost estimate, a region, a TTL and a
  cleanup plan.
- Destructive scripts must be limited to dedicated demo resources and must check
  the resolved path/target before deleting anything.

## 7. Forbidden actions

- Publishing secrets or generated state.
- Creating cloud resources (AWS or otherwise) without explicit written approval.
- Adding an LLM API key of the repository owner to a public workflow.
- Faking agent runs, replay data, test results or maturity.
- Deleting or overwriting work without reading it first.
- Rewriting git history on `main` or pushing directly to a protected branch.

## 8. When requirements are unclear

1. Read the relevant docs and ADRs.
2. Prefer the smallest reversible change.
3. If the ambiguity affects cost, security, data loss or irreversible changes:
   stop and ask the repository owner.
4. Record the decision in `docs/decisions/` if it is architectural.

## 9. Definition of Done

A change is done when:

1. The goal and design are documented (README/ADR as appropriate).
2. Prerequisites are complete and reproducible.
3. An automated test exists and passes.
4. Cleanup is documented and tested.
5. No secrets are exposed and CI stays green.
6. Status tables/website show the real state.
7. Known limitations are documented.
