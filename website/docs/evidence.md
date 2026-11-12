# Evidence / Results

This project proves what it executed. Demo runs write a structured JSON document
with scenario id, execution mode, timestamps, commit, per-check statuses and
known limitations.

## Real results in the repository

| Document | Scenario | Mode | Status |
| --- | --- | --- | --- |
| `evidence/examples/terraform-lifecycle.local.json` | Lab 01 | `local` | `passed` |
| workflow artifacts (`lab01-evidence`, `lab03-evidence`) | Labs 01/03 | `live-ci` | per run |

!!! note "Artifacts expire, examples are committed"
    GitHub Actions artifacts are retained for 14 days. The committed example is a
    real run; its `commit` field shows which revision produced it.

## Result format

```json
{
  "scenario_id": "terraform-lifecycle-001",
  "scenario_name": "Terraform Infrastructure Lifecycle",
  "execution_mode": "local",
  "status": "passed",
  "started_at": "2026-11-12T15:03:20Z",
  "completed_at": "2026-11-12T15:03:38Z",
  "commit": "53c37fe...",
  "workflow_run": null,
  "checks": [{ "name": "terraform-plan", "status": "passed" }],
  "artifacts": [{ "name": "evidence/local-lifecycle.json", "kind": "json" }],
  "limitations": ["Local run only; no GitHub Actions execution is recorded here."]
}
```

## Validation

```bash
python3 scripts/validate_evidence.py
```

Every document is validated against `evidence/schema/scenario-result.schema.json`;
replay recordings against `replay/schema/recording.schema.json`. A document that
does not validate fails CI.

## Live vs. replay

- `execution_mode: local` -- run on a developer machine.
- `execution_mode: live-ci` -- run in GitHub Actions.
- `execution_mode: replay` -- a recorded run being replayed; clearly marked.

No document is ever labelled as a live AI run unless a model actually ran --
which is not the case in this project today.
