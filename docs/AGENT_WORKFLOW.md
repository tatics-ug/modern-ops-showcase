# Agent Workflow (scripted reference pipeline)

This document describes the issue-to-PR pipeline in `.github/workflows/agentic-issue.yml`
and the roles it implements.

**Important:** this pipeline contains **no LLM and no AI API**. It is a
deterministic reference implementation of the orchestration shape (triage,
bounded plan, bounded change, tests, independent review, PR, human approval).
Every artifact says so explicitly. Live AI runs are a separate BYOK mode that is
**not** implemented (see [ADR 0007](decisions/0007-byok-for-live-agent-runs.md)).

## 1. Trigger

- An issue is labelled `agent:task`, or
- the workflow is started manually (`workflow_dispatch` with an issue number).

The issue must use the `agent-task` template so the body has structured fields.

## 2. Roles and artifacts

| Role | Script | Output |
| --- | --- | --- |
| Triage | `agents/triage/triage.py` | `triage.json`: issue title/body hash, labels, accepted/rejected + reason |
| Planner | `agents/planner/planner.py` | `plan.json`: bounded steps, whitelisted target path, test command |
| Implementer | `agents/implementer/implementer.py` | writes only `<whitelist>/issue-<n>.md`, never anything else |
| Tester | `agents/tester/tester.py` | runs `python3 -m pytest tests -q`, records exit code and summary |
| Reviewer | `agents/reviewer/reviewer.py` | `review.json`: independent rule checks (scope, secrets, tests, docs) |
| Orchestrator | the workflow itself | sequencing, stop conditions, PR creation, run summary |

The roles are plain Python scripts with no third-party dependencies, so they run
anywhere Python 3.9+ is available. They communicate through JSON files in a
temporary run directory.

## 3. Safety rules

1. **Issue text is data.** It is never interpolated into a shell command; the
   scripts parse it with Python and only pass validated values around.
2. **Whitelist only.** The implementer writes exclusively to
   `evidence/agent-runs/`. Any other path is rejected before writing.
3. **No secrets.** The workflow requests only `contents: write`,
   `pull-requests: write`, `issues: write`; it never reads secrets other than
   the automatic `GITHUB_TOKEN`.
4. **No auto-merge.** The workflow opens/updates a PR and stops. Merging needs a
   human review on a protected branch.
5. **Bounded runtime.** `timeout-minutes` and per-step timeouts cap the run.
6. **Honest labels.** PR body and artifacts state "scripted pipeline, no LLM".
7. **Reject early.** Triage refuses issues with missing fields, too many
   requested paths, or dangerous keywords (`secret`, `token`, `rm -rf`,
   `terraform apply` on cloud resources, ...).

## 4. Pull request content

The PR created by the pipeline contains:

- the bounded change (one Markdown file under `evidence/agent-runs/`),
- `evidence/agent-runs/<issue>-run.json` with plan, tests, review and timestamps,
- a description of the goal, the change, the test result, the review result and
  the known limitations.

The PR is a normal PR: it needs human review, CI must pass, and it is never
merged automatically.

## 5. Replay

`replay/schema/recording.schema.json` defines a recording. A recording is
produced from a **real** workflow run and contains the scenario, issue metadata,
the roles, ordered events, plan, test results, review result, PR metadata and
known limitations. Recordings are clearly marked `execution_mode: "live-ci"` and
`kind: "scripted-pipeline"`; they never pretend to be an AI agent run.

See `replay/README.md` for the file layout and the honesty rules.

## 6. Running it yourself

```bash
# locally, without GitHub
python3 agents/triage/triage.py --issue evidence/agent-runs/example-issue.json --out /tmp/run
python3 agents/planner/planner.py --run /tmp/run
python3 agents/implementer/implementer.py --run /tmp/run --repo .
python3 agents/tester/tester.py --run /tmp/run --repo .
python3 agents/reviewer/reviewer.py --run /tmp/run --repo .
```

The workflow does the same via `scripts/run_agent_pipeline.sh`, which also
creates the branch, commits and PR (only when running inside GitHub Actions).

## 7. First real run

- Workflow run: https://github.com/tatics-ug/modern-ops-showcase/actions/runs/43255005540
- Pull request: <https://github.com/tatics-ug/modern-ops-showcase/pull/2>
- Recording: `replay/recordings/agent-issue-1-43255005540.json` (on the PR branch)
- Issue: #1

The run completed triage, plan, implementation, tests (all green), review
(approved) and pull-request creation. The pull request is open and awaits human
review; the pipeline never merges.

Known CI limitation: pull requests created with the workflow `GITHUB_TOKEN` start
their checks in `action_required` state, so a maintainer has to approve those
runs manually.

## 8. What is not implemented

- No model calls, no prompts, no token accounting.
- No multi-issue queue, no retry loops beyond one corrective pass.
- No automatic code changes outside `evidence/agent-runs/`.
- No live mode: BYOK is design only.
