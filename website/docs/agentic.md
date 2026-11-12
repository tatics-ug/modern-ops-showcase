# Agentic Engineering

GitHub issues are the task source. A pipeline turns an issue into a reviewed
pull request -- and a human decides about the merge.

!!! warning "No LLM in this pipeline"
    The pipeline is **scripted and deterministic**. It implements the
    orchestration shape (triage, plan, bounded change, tests, independent
    review, PR, human gate) but contains no model and no API key. Every artefact
    it writes says so. Live AI runs are documented as a BYOK design only.

## Flow

```mermaid
flowchart LR
  issue[Issue: agent:task] --> triage[Triage]
  triage -->|reject| comment[Comment + stop]
  triage -->|accept| plan[Plan]
  plan --> impl[Implementer: 1 whitelisted file]
  impl --> test[Tester: pytest]
  test -->|fail| stop[Stop + failed record]
  test -->|pass| review[Reviewer: rule-based]
  review --> pr[Pull request]
  pr --> human{Human review}
  human --> merge[Merge]
```

## Guard rails

| Risk | Control |
| --- | --- |
| untrusted issue text | parsed by Python, never executed, dangerous patterns rejected |
| scope creep | whitelist: `evidence/agent-runs/`, `replay/recordings/` only |
| secrets | none needed; only the automatic `GITHUB_TOKEN` |
| auto-merge | not implemented; `main` is protected |
| runtime | workflow timeout, bounded plan limits |
| honesty | artefacts carry `kind: scripted-pipeline`, `llm: false` |

## Replay

Recordings of real runs live in `replay/recordings/` and follow
`replay/schema/recording.schema.json`: ordered events, plan, changes, tests,
review and PR metadata. A recording is never fabricated.

## Live mode (not implemented)

A BYOK design exists in ADR 0007: visitor-supplied key, manual trigger only, no
operator key, costs visible. It is disabled until it can be shipped safely.
