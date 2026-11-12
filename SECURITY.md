# Security Policy

## Reporting a vulnerability

Please do not open a public issue for security problems. Use GitHub's
**private vulnerability reporting** (Security tab -> "Report a vulnerability")
for this repository. You will get an acknowledgement as soon as possible; this
is a showcase project maintained by a single owner, so please allow a few days.

## Scope

In scope: workflow permissions and secret handling, the scripted agentic
pipeline and its untrusted-input handling, the Kubernetes lab manifests, the
Terraform lab configuration, and the website build.

Out of scope: vulnerabilities in third-party tools or actions themselves
(report those upstream), and the security of a visitor's local machine.

## Security model (what this project assumes)

| Assumption | Implementation |
| --- | --- |
| No secrets in the repository | `.gitignore` covers state, kubeconfigs, `.env`, tfvars; no secret is required to run anything |
| Least-privilege CI | every workflow sets explicit `permissions:`; default is `contents: read` |
| No secrets for untrusted input | no workflow uses `pull_request_target`; fork PRs get no secrets |
| Untrusted issue text is data, not code | the agentic pipeline parses issue text, validates it, and only touches a whitelisted path |
| No automatic merge | the pipeline may open/update a PR, never merge; `main` is protected |
| No cloud or paid resources | labs run locally and in free CI runners; AWS labs are `planned` and disabled |
| Reproducible providers | `.terraform.lock.hcl` is committed; provider versions are pinned |
| Container hardening (lab) | non-root UID, read-only root filesystem, all capabilities dropped, seccomp `RuntimeDefault`, no service account token |

## Secrets

- No credential is needed for any standard demo. There is no API key stored in
  this repository or in its workflows.
- Live AI runs (BYOK) are **not** implemented. If that mode is added later, the
  key must be an Actions secret provided by the visitor's own fork/environment,
  never an operator key, and never used for untrusted PRs. See
  [docs/decisions/0007-byok-for-live-agent-runs.md](docs/decisions/0007-byok-for-live-agent-runs.md).
- Terraform state can contain sensitive values in plaintext (demonstrated in
  Lab 01). State is git-ignored and never published.

## Branch protection

`main` is protected: pull requests required, at least one approving review,
force-pushes and branch deletion disabled. Changing security policies, secrets,
permissions or cost-relevant resources always requires human approval
(see AGENTS.md).

## Dependency and workflow hygiene

- GitHub Actions are referenced by version tag (`@v4`, `@v3`); pinning to commit
  SHAs is a recommended hardening step tracked in
  [docs/RUNBOOK.md](docs/RUNBOOK.md).
- Public repository security features (Dependabot alerts, secret scanning
  push protection where available for free) are recommended, not silently enabled.
- Scanning: Trivy runs in the validation workflow (filesystem/config scan);
  results are uploaded as workflow artifacts.

## Supported versions

Only the latest commit on `main` is supported. There are no released versions
and no production deployment; the website is static documentation.
