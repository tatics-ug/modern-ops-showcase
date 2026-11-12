# Replay

Replay makes a run followable without executing it again -- and without an API
key. It is a recording of a **real** run, never a simulation.

## Layout

```text
replay/
├── schema/recording.schema.json      structure of a recording
├── scenarios/agent-task-001.json     what the pipeline is supposed to do
└── recordings/                       one file per real run
```

## Honesty rules

1. A recording is derived from the run's own artefacts (triage, plan, events,
   tests, review, pull request). Missing steps are recorded as missing.
2. Every recording states `kind` and `llm`. The current pipeline is
   `kind: "scripted-pipeline"`, `llm: false`; it is **not** an AI agent run and
   does not pretend to be one.
3. `execution_mode: "live-ci"` means the run happened in GitHub Actions;
   `replay` would be a re-presentation of such a recording. Nothing here claims
   a live model call.
4. Pull requests are never merged automatically; the human gate is part of the
   recorded flow.

## Reading a recording

```bash
jq '.title, .events[] | {order, actor, action}' replay/recordings/<file>.json
```

The `events` array is ordered (`order`), each entry has a timestamp, the acting
role and a short detail. `changes`, `tests`, `review` and `pull_request` show
what actually happened.

## Validate recordings

```bash
python3 scripts/validate_evidence.py
```

## Current state

The first real recording was produced by the `agentic-issue` run
[43255005540](https://github.com/tatics-ug/modern-ops-showcase/actions/runs/43255005540):
`replay/recordings/agent-issue-1-43255005540.json`. It contains six ordered
events (triage, plan, implement, tests, review, recording), the plan, the test
result, the review checks and the pull request metadata (PR #2).

That file currently lives on the pipeline branch `agent/issue-1-43255005540` and
is part of [pull request #2](https://github.com/tatics-ug/modern-ops-showcase/pull/2).
It becomes part of `main` when a human merges the pull request -- the pipeline
never merges, which is the point of the human gate.
