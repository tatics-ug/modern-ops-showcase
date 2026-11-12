# ADR 0007 -- BYOK for live agent runs (not implemented)

**English** | [Deutsch](0007-byok-for-live-agent-runs.de.md)

- Status: proposed (design only, intentionally disabled)
- Date: 2026-11-12
- Deciders: repository owner

## Context

A live AI mode is attractive but must never use the repository owner's API key
for arbitrary visitors, and must never expose secrets to fork workflows.

## Decision (design)

If live mode is implemented: the visitor supplies their own key through an
environment secret or a repository/environment they control, the workflow is
`workflow_dispatch`-only (never automatic on issues/PRs), costs and limits are
displayed, and the key is never logged. Until then, live mode stays disabled.

## Alternatives considered

- Operator key: forbidden (public cost/abuse risk).
- Shared demo account: still operator-funded.

## Consequences

- No cost and no secret risk today.
- The agentic demo stays scripted; this is stated on the website and in the
  pipeline output.
