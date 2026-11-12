# Getting Started

From a fresh clone to a successful demo in a few minutes. No cloud account, no
API key, no GPU, no cost.

## Prerequisites

| Tool | Version | For |
| --- | --- | --- |
| Terraform or OpenTofu | >= 1.6 | Labs 01, 03 |
| Python | >= 3.9 (3.12 recommended) | tests, website, pipeline |
| Docker | >= 24 | Lab 03 |
| kind | >= 0.2x | Lab 03 |
| kubectl | >= 1.28 | Lab 03 |
| make | GNU make | convenience commands |

## Clone and run

```bash
git clone https://github.com/tatics-ug/modern-ops-showcase.git
cd modern-ops-showcase
make demo-list
make demo-run SCENARIO=01     # ~20 s, writes evidence
make demo-run SCENARIO=03     # ~4-8 min, needs Docker + kind
```

## Development environment

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
python3 -m venv website/.venv
website/.venv/bin/pip install -r website/requirements.txt
make validate                  # repo tests + evidence validation + terraform fmt
make website-serve             # http://127.0.0.1:8000
```

## Security notes

- No credentials are required anywhere in the standard flow.
- Lab 01 state contains a dummy sensitive value in plaintext -- state is
  git-ignored; never commit it.
- Lab 03 manages the namespace `demo` in a local kind cluster only. Do not point
  it at a real cluster.
- Never add an operator API key to a workflow. BYOK is design-only today.

## Troubleshooting

- `docker: permission denied` -> add your user to the `docker` group, re-login.
- kind creation slow -> pre-pull `kindest/node:v1.33.12`.
- `Inconsistent dependency lock file` -> you switched between Terraform and
  OpenTofu; restore the lock file or stay on one engine.
- `command not found: mkdocs` -> use `make website`, which prefers
  `website/.venv`.

Full runbook:
[`docs/RUNBOOK.md`](https://github.com/tatics-ug/modern-ops-showcase/blob/main/docs/RUNBOOK.md).
