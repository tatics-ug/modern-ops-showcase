# ADR 0003 -- GitHub Actions as the execution layer

- Status: accepted
- Date: 2026-11-12
- Deciders: repository owner

## Context

Demos, validation and the agentic pipeline need a scheduler and runners. The
project must not cost money.

## Decision

Use GitHub Actions with standard GitHub-hosted runners. For public repositories
these runners are free, and usage does not reduce any included quota.

## Alternatives considered

- Self-hosted runners: no per-minute cost but permanent infrastructure to
  maintain and secure.
- Local-only execution: no reproducible evidence for visitors.

## Consequences

- Free execution; evidence is a workflow run URL.
- Untrusted input must be handled carefully: no secrets in fork/PR contexts,
  explicit `permissions:`, no `pull_request_target`.
- Vendor lock-in to GitHub is accepted; scripts remain runnable locally.
