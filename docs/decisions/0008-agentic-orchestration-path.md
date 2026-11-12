# ADR 0008 -- Scripted agent orchestration for the MVP

**English** | [Deutsch](0008-agentic-orchestration-path.de.md)

- Status: accepted
- Date: 2026-11-12
- Deciders: repository owner

## Context

The MVP needs a real issue-to-PR pipeline with triage, plan, bounded change,
tests, independent review and a human merge gate. Candidate orchestrators are
GitHub Agentic Workflows (`gh-aw`) and issue/PR agents, all of which need an LLM
API key and therefore money for arbitrary visitors.

## Decision

Implement the orchestration shape as a deterministic, rule-based pipeline in
GitHub Actions (`agents/` + `agentic-issue` workflow), explicitly labelled
"scripted, no LLM". Do not introduce `gh-aw` or any other agent framework in the
MVP.

## Alternatives considered

- `gh-aw`: promising, requires review of permissions/costs, and an LLM key.
- Custom agent with a free-tier API: quota/terms uncertainty, not reliable.
- Manual demonstration only: fails the MVP acceptance criterion.

## Consequences

- Free, reproducible, auditable, no secret handling.
- No LLM reasoning: the "intelligence" is the workflow, not a model. This is
  stated everywhere.
- The live AI mode can be added later behind the BYOK design (ADR 0007).
