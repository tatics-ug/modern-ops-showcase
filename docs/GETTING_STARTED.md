# Getting Started

This guide takes you from a fresh clone to a successful demo run in a few
minutes. No cloud account, no API key, no GPU, no cost.

## 1. Prerequisites

| Tool | Version | Needed for |
| --- | --- | --- |
| Terraform *or* OpenTofu | >= 1.6 | Lab 01, Lab 03 |
| Python | >= 3.9 (3.12 recommended) with `pytest` | all tests, website |
| Docker | >= 24 | Lab 03 (kind) |
| kind | >= 0.2x | Lab 03 |
| kubectl | >= 1.28 | Lab 03 |
| make | any GNU make | convenience commands |

Optional: `mkdocs-material` (website build), `shellcheck`, `yamllint` (local lint
parity with CI).

### Installing Terraform (Ubuntu/Mint, free)

The HashiCorp apt repository is the convenient route. On Linux Mint the
distribution codename (`zara`, `xia`, ...) is **not** a HashiCorp suite; use the
Ubuntu base codename instead (`noble` for Mint 22.x):

```bash
sudo install -m 0755 -d /usr/share/keyrings
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com noble main" \
  | sudo tee /etc/apt/sources.list.d/hashicorp-terraform.list
sudo apt-get update && sudo apt-get install -y terraform
terraform version
```

OpenTofu works identically through `make TF=tofu ...`.

### Installing kind (free, single binary)

```bash
curl -fsSL -o kind https://github.com/kubernetes-sigs/kind/releases/download/v0.33.0/kind-linux-amd64
curl -fsSL -o kind.sha256sum https://github.com/kubernetes-sigs/kind/releases/download/v0.33.0/kind-linux-amd64.sha256sum
mv kind kind-linux-amd64 && sha256sum -c kind.sha256sum
install -m 0755 kind-linux-amd64 ~/.local/bin/kind
kind version
```

`~/.local/bin` must be in `PATH` (it usually is on desktop Linux).

## 2. First run

```bash
git clone https://github.com/tatics-ug/modern-ops-showcase.git
cd modern-ops-showcase
make demo-list
make demo-run SCENARIO=01     # Terraform lifecycle, ~20 s
```

Lab 01 creates files under `labs/01-terraform-lifecycle/workspace/`, runs the
tests, destroys everything and writes
`labs/01-terraform-lifecycle/evidence/local-lifecycle.json`.

Kubernetes lab (needs Docker and kind):

```bash
make demo-run SCENARIO=03     # ~4-8 min: cluster up, deploy, fault, fix, cleanup
```

## 3. Inspecting results

```bash
make demo-list                        # scenario overview
python3 scripts/validate_evidence.py  # validate all evidence documents
cat labs/01-terraform-lifecycle/evidence/local-lifecycle.json
```

Evidence documents are validated against
`evidence/schema/scenario-result.schema.json`. Committed examples live in
`evidence/examples/` and are real runs (see their `commit` field).

## 4. Website locally

```bash
python3 -m venv website/.venv
website/.venv/bin/pip install -r website/requirements.txt
make website-serve            # http://127.0.0.1:8000
make website                  # build into website/site (git-ignored)
```

The site is built in CI and deployed to GitHub Pages by
`.github/workflows/deploy-pages.yml`.

## 5. Security notes

- Nothing in the standard flow needs credentials, and none are stored.
- Lab 01 state contains a **dummy** sensitive value in plaintext. That is the
  teaching point; state is git-ignored.
- Lab 03 creates a local kind cluster named `modernops-lab03` and deletes it at
  the end. It never touches other clusters.
- Do not run the labs with a kubeconfig pointing at a real cluster: Lab 03
  Terraform manages the namespace `demo` and would delete it on `destroy`.

## 6. Troubleshooting

See [RUNBOOK.md](RUNBOOK.md). The most common issues: no Docker access, kind
node image not yet downloaded, provider download behind a proxy, stale
`.terraform` directory after switching between Terraform and OpenTofu.
