# Runbook

Operational procedures for the showcase. Nothing here requires paid services.

## 1. Runnable scenarios

| Scenario | Command | Duration | Creates | Removes |
| --- | --- | --- | --- | --- |
| 01 Terraform lifecycle | `make demo-run SCENARIO=01` | ~20 s | files in `labs/01-terraform-lifecycle/workspace/` | `make demo-down SCENARIO=01` |
| 03 Kubernetes platform | `make demo-run SCENARIO=03` | 4-8 min | kind cluster `modernops-lab03`, namespace `demo` | `make demo-down SCENARIO=03` |

Both write an evidence JSON (`labs/*/evidence/`) that is git-ignored; CI uploads
it as an artifact.

## 2. Routine checks

```bash
make validate                 # repo tests + evidence schema + terraform fmt
make website                  # strict MkDocs build
```

CI runs the same checks plus YAML, shell, workflow linting and a Trivy
filesystem scan (`.github/workflows/validate.yml`).

## 3. Failure handling

### Lab 01

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Inconsistent dependency lock file` | engine switched (tofu <-> terraform) and the lock file was rewritten | stay on one engine, or `git checkout -- labs/01-terraform-lifecycle/.terraform.lock.hcl` |
| `terraform init` cannot reach the registry | offline/proxy | configure `HTTPS_PROXY`, or pre-populate `.terraform/` |
| evidence missing after a failure | the evidence writer itself failed (e.g. broken `PYTHON`) | rerun with a working `python3`; a stale evidence file is never overwritten by a broken writer |
| second plan reports changes | manual edit inside `workspace/` | expected drift; `terraform apply` restores it |

### Lab 03

| Symptom | Cause | Fix |
| --- | --- | --- |
| `docker: permission denied` | user not in `docker` group | add the user to `docker`, re-login |
| kind cluster creation times out | node image download slow | `docker pull kindest/node:v1.33.12` first, retry |
| pods in `ErrImageNeverPull` during healthy tests | image not loaded into kind | `make load` after `make build` |
| `terraform destroy` fails | cluster already deleted manually | delete local state: `labs/03-kubernetes-platform/terraform/terraform.tfstate` |
| port 30080 already bound | another service uses the mapped port | change `extraPortMappings` in `kind/kind-config.yaml` |

## 4. Cleanup and reset

```bash
make demo-reset SCENARIO=01    # destroy Terraform resources, remove workspace files
make demo-down  SCENARIO=01    # reset + remove local Terraform working data
make demo-down  SCENARIO=03    # destroy resources + delete the kind cluster
docker ps                      # verify no modernops containers remain
kind get clusters              # verify modernops-lab03 is gone
```

## 5. GitHub workflows

| Workflow | Trigger | Purpose |
| --- | --- | --- |
| `validate` | push, PR | repository checks, website build, Trivy |
| `deploy-pages` | push to `main` | build the site and deploy to GitHub Pages |
| `demo-terraform` | push/PR touching Lab 01, manual | Lab 01 lifecycle in CI |
| `demo-kubernetes` | push/PR touching Lab 03, manual | Lab 03 lifecycle with kind |
| `agentic-issue` | issue labelled `agent:task`, manual | scripted triage/plan/implement/test/review, opens a PR |

All workflows use `permissions:` with the minimum required scope, and no
workflow has access to a paid secret.

## 6. GitHub Pages and custom domain

Pages is configured with **GitHub Actions** as the source. For the custom
domain `modern-ops-showcase.tatics.de` a DNS record must be created by whoever
controls the `tatics.de` zone (this project does not change DNS):

1. Create `CNAME` `modern-ops-showcase.tatics.de` -> `tatics-ug.github.io`.
2. In the repository: Settings -> Pages -> Custom domain ->
   `modern-ops-showcase.tatics.de`, save.
3. Enable "Enforce HTTPS" once GitHub has issued the certificate.
4. Verify: `dig +short modern-ops-showcase.tatics.de CNAME` and open the site.

Typical problems: the CNAME still points to the old host, the domain is claimed
by another repository, or HTTPS is enabled before the certificate exists.

## 7. Repository maintenance

- Actions are pinned by tag; pinning by commit SHA is a recommended hardening
  step (requires a PR, since `main` is protected).
- Dependabot alerts can be enabled in the repository settings (free for public
  repositories); no automatic PRs are configured on purpose.
- Evidence artifacts are retained for 14 days (demo workflows) to keep storage
  small.

## 8. Repository settings applied for this project (free tiers)

| Setting | Value |
| --- | --- |
| Visibility | public |
| Pages | GitHub Actions source, HTTPS enforced |
| Org policy | "Actions may create pull requests" enabled (merge still human-only) |
| Default workflow permissions | read-only |
| Labels | `agent:task`, `docs` |
| Branch protection | see SECURITY.md |

The policy "Actions may create pull requests" is an organisation-level setting
that needs the `admin:org` scope. It is required because the scripted pipeline
opens the PR with `GITHUB_TOKEN`; the token still cannot merge or approve.

## 9. Escalation

Only the repository owner can change security policies, branch protection,
secrets or cost-relevant settings. Anything that would create paid resources
must be approved explicitly and documented with cost estimate, region, TTL and
cleanup plan first.
