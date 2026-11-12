# ADR 0006 -- Replay as the default demonstration mode

- Status: accepted
- Date: 2026-11-12
- Deciders: repository owner

## Context

Visitors must be able to follow the agentic flow without an API key. Live agent
runs cost money and must never expose an operator key.

## Decision

Recorded runs are the default: structured JSON recordings are presented as
recordings and labelled as such. Live execution is optional and requires the
visitor's own key (BYOK).

## Alternatives considered

- Operator-funded live demo: cost and abuse risk.
- Screenshots: not verifiable.

## Consequences

- Zero cost, reproducible presentation.
- Replay data must be produced by real runs; fabricated recordings are forbidden.
- Replay is explicitly marked `execution_mode: live-ci` plus `kind:
  scripted-pipeline` until a real AI run exists.
