# Lab 01 -- Terraform Infrastructure Lifecycle

**English** | [Deutsch](README.de.md)

Hands-on lab that demonstrates the full Infrastructure-as-Code lifecycle with
Terraform in a controlled environment: **format, validate, plan, apply, verify,
detect drift, destroy, cleanup**. It uses the `hashicorp/local` provider, so it
creates no cloud resources and costs nothing. `terraform init` needs network
access once to download the provider; everything after that runs offline.

Files are written to `./workspace/`. Nothing outside this lab directory is
touched. State stays local and is git-ignored.

Status: **validated locally** -- all acceptance criteria are covered by
automated tests. The GitHub Actions workflow runs the same script; see the
workflow run under *Actions* for CI evidence.

---

## 1. Purpose

The lab answers the question "what does Terraform actually do?" with observable
evidence instead of a configuration file:

| Lifecycle step | Demonstrated by | Evidence |
| --- | --- | --- |
| Formatting | `terraform fmt -check -recursive` | exit code 0 |
| Validation | `terraform validate` | exit code 0 |
| Planning | `terraform plan -out=lab.tfplan` | saved plan file |
| Applying | `terraform apply lab.tfplan` | files on disk |
| Outputs | `terraform output -json` | paths, SHA-256, redacted secret |
| State | local `terraform.tfstate` | git-ignored, checked by test |
| Idempotency | second `plan -detailed-exitcode` | exit code 0 (no changes) |
| Failure case | invalid variable value | validation error, exit code != 0 |
| Teardown | `terraform destroy` | workspace removed, state empty |

## 2. Prerequisites

- Terraform >= 1.6 (validated with 1.17.2) or OpenTofu >= 1.6
- Python 3.9+ with `pytest`
- `make` (convenience targets only, all commands work without it)
- Network access for `terraform init` (provider download), ~30 MB disk

Installing Terraform itself is **not** part of this lab. On the reference
machine it was installed from the HashiCorp apt repository (`noble` suite, since
Linux Mint 22.2 is Ubuntu 24.04 based); any Terraform 1.6+ or OpenTofu 1.6+
binary works.

## 3. Architecture

```text
labs/01-terraform-lifecycle/
├── versions.tf              Terraform/provider version constraints, local backend
├── providers.tf             hashicorp/local provider
├── variables.tf             inputs + validation rules
├── main.tf                  locals, tag set, module call
├── outputs.tf               lifecycle outputs
├── terraform.tfvars.example example variable file
├── modules/demo_workspace/  reusable module: files + template + sensitive file
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── versions.tf
│   └── templates/runtime.conf.tftpl
├── tests/
│   ├── test_lab.py          pytest verification against the applied workspace
│   └── run_lifecycle.sh     full lifecycle incl. cleanup + evidence JSON
└── Makefile                 thin wrapper around the commands above
```

Generated at runtime: `workspace/`, `.terraform/`, `terraform.tfstate`,
`lab.tfplan`, `evidence/` -- all git-ignored. `.terraform.lock.hcl` is generated
as well but **is committed**, so provider versions and hashes stay reproducible.

The `workspace/` directory contains four artefacts:

| File | Mode | Purpose |
| --- | --- | --- |
| `metadata.json` | 0644 | machine-readable summary, tags, provider |
| `runtime.conf` | 0644 | rendered from a `templatefile()` |
| `demo-credential.txt` | 0600 | dummy "secret" via `local_sensitive_file` |
| `checksums.txt` | 0644 | SHA-256 manifest of the other files |

## 4. Run it

```bash
cd labs/01-terraform-lifecycle
make lifecycle            # complete run, ends with destroy + evidence JSON
```

or step by step:

```bash
make init                 # provider download, local backend
make fmt-check            # formatting gate
make validate
make plan                 # writes lab.tfplan
make apply
make output               # paths, hash, redacted sensitive value
make test                 # pytest verification
make destroy              # remove all managed resources
make clean                # remove local working data and artefacts
```

Without `make`:

```bash
terraform init -input=false
terraform fmt -check -recursive
terraform validate
terraform plan -input=false -out=lab.tfplan
terraform apply -input=false lab.tfplan
python3 -m pytest tests -q
terraform destroy -input=false -auto-approve
```

Engine selection: every command accepts `TF=<binary>`, e.g.
`make TF=tofu lifecycle`. The test suite inherits the same engine, so a
OpenTofu run really executes the OpenTofu binary end to end (the HCL only uses
constructs supported by both tools).

Caveat when switching engines: `tofu init` rewrites the committed
`.terraform.lock.hcl` (provider source `registry.opentofu.org`, different
hashes). Afterwards `terraform` refuses to run with "Inconsistent dependency
lock file". Either stay on one engine or restore the lock file with
`git checkout -- .terraform.lock.hcl` before switching back.

Expected results: `make plan` reports **4 to add** on a clean workspace;
`make apply` writes the four files above; `make test` passes all tests;
`make destroy` removes them and leaves `terraform state list` empty.

## 5. Inputs and outputs

| Variable | Default | Notes |
| --- | --- | --- |
| `workspace_dir` | `workspace` | relative, must stay inside the lab, no `..` |
| `workspace_name` | `lab01-demo` | `^[a-z][a-z0-9-]{2,30}$` |
| `environment` | `demo` | one of `demo`, `dev`, `test` |
| `owner` | `modernops-showcase` | tag value |
| `file_permission` | `0644` | octal mode for non-sensitive files |
| `sensitive_demo_value` | dummy placeholder | marked `sensitive`, never a real credential |

| Output | Meaning |
| --- | --- |
| `workspace_dir` | path of the workspace, relative to the lab directory |
| `workspace_name` | echoed input |
| `metadata_path` | path of `metadata.json`, relative to the lab directory |
| `metadata_sha256` | SHA-256 Terraform considers authoritative |
| `runtime_config_path` | path of `runtime.conf`, relative to the lab directory |
| `file_count` | number of managed files (4) |
| `sensitive_demo_value` | redacted in CLI output (`sensitive = true`) |

## 6. Tests

`tests/test_lab.py` verifies the applied result, not the intent:

- generated files exist and match `terraform output`
- `metadata.json` content and SHA-256 match Terraform's own hash
- `runtime.conf` was templated with the expected values
- `checksums.txt` matches the files on disk
- file modes are `0644`/`0600` as configured
- the sensitive output is flagged and redacted in plain `terraform output`
- the "credential" file contains only the dummy placeholder
- a second plan has no changes (idempotency)
- `workspace_name=Invalid_Name` and an absolute `workspace_dir` are rejected
- `terraform.tfstate` is git-ignored (state never published)

```bash
make apply   # tests verify an applied workspace
make test
```

## 7. Deliberate failure case

Two reproducible negative cases exist as tests, both fail *before* anything is
created:

```bash
terraform plan -var workspace_name=Invalid_Name
# Error: Invalid value for variable -> workspace_name must match ^[a-z][a-z0-9-]{2,30}$

terraform plan -var workspace_dir=/tmp/lab01-escape
# Error: Invalid value for variable -> workspace_dir must be a non-empty relative path
```

The second case is the important one: it makes the "this lab cannot write
outside its own directory" property testable instead of assumed.

## 8. State handling and security

- Local backend (`backend "local"`), so there is no remote state, no bucket and
  no cloud account involved.
- `terraform.tfstate` contains the dummy sensitive value in plaintext. That is
  the point of the demo: **sensitive outputs are redacted in the CLI but stored
  in the state**. The state is therefore git-ignored and never committed.
- `.terraform.lock.hcl` **is** committed, so provider versions and hashes are
  reproducible.
- No credentials are required: the `local` provider needs none, and the only
  "secret" is the documented placeholder.
- `.gitignore` (repository root) excludes `*.tfstate*`, `.terraform/`,
  `*.tfplan`, `workspace/` and `evidence/`; a test verifies the state is
  ignored.
- `tests/run_lifecycle.sh` deletes only paths inside this lab directory, guarded
  by a path-containment check. Note: the guard uses bash's logical `pwd`, so a
  symlinked `workspace/` caused by external manipulation is removed as a link
  (the link target itself is never deleted by `rm -rf`).

For production use the state would live in an encrypted remote backend with
locking and restricted access. That is documented here as a gap, not simulated.

## 9. Cleanup

```bash
make destroy     # destroy managed resources (idempotent, safe to repeat)
make clean       # remove .terraform/, lab.tfplan, workspace/, evidence/, state
```

`tests/run_lifecycle.sh` also destroys on failure (best effort) and verifies
that the workspace directory and the state are empty afterwards.

## 10. CI

`.github/workflows/demo-terraform.yml` runs the same lifecycle on
`ubuntu-latest` with `permissions: contents: read`, a `timeout-minutes` limit
and `terraform destroy` in an `always()` step. It uploads `evidence/` as an
artifact. The workflow is implemented but **not yet executed** (no remote with
Actions available in this environment); it is therefore not marked `validated`.

## 11. Known limitations

- Single-machine demo: no remote backend, no state locking, no multi-user
  workflow.
- Provider download requires network on first `init`.
- The "secret" is a documented dummy; the lab does not show real secret
  management (that is a later lab).
- CI parity is prepared, not proven.

## 12. Competence evidence

| Claim | Evidence in this lab |
| --- | --- |
| Terraform module design | `modules/demo_workspace` with typed, validated inputs |
| Variable validation | three validation blocks plus two negative tests |
| Templates | `templatefile()` producing `runtime.conf` |
| Outputs | seven outputs, one sensitive |
| State awareness | git-ignore test, documented plaintext-state risk |
| Idempotency | `plan -detailed-exitcode` gate in tests and lifecycle script |
| Lifecycle | `tests/run_lifecycle.sh` from init to destroy with evidence JSON |
| Least privilege | `permissions: contents: read`, no credentials used |
