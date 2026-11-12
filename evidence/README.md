# Evidence

Structured proof of what was actually executed. Two kinds of documents live here:

| Location | Content | Produced by |
| --- | --- | --- |
| `schema/scenario-result.schema.json` | JSON Schema for a demo result | repository |
| `examples/*.json` | **real** results of local runs | `make demo-run`, lab lifecycle scripts |
| `agent-runs/*.json`, `agent-runs/*.md` | records of scripted pipeline runs | `agentic-issue` workflow |

Workflow artifacts are **not** committed (they expire); the committed examples
are real runs and carry the `commit` they were produced at. If a document here
were ever stale, the timestamp and commit make that visible.

## Validate

```bash
python3 scripts/validate_evidence.py          # needs jsonschema (requirements-dev.txt)
```

## Rules

1. Never invent results. A document in this directory is always the output of a
   real run, copied verbatim (only the file name may differ).
2. No secrets: results must not contain credentials, tokens, kubeconfigs or
   personal data.
3. Every result lists `checks[]` with real statuses and `limitations[]` with the
   honest gaps of the run.
4. Distinguish execution modes: `local` (developer machine), `live-ci` (GitHub
   Actions) and `replay` (recorded run being replayed).
5. A scenario may only be marked `validated` in the docs if a passing result
   exists.

## Example documents

- `examples/terraform-lifecycle.local.json` -- Lab 01 life cycle, local run,
  status `passed`, 11 checks.
Lab 03 results are produced by `demo-kubernetes` runs and uploaded as workflow
artifacts; the lab stays `implemented` until such a run is referenced here.
