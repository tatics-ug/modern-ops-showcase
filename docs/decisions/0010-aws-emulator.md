# ADR 0010 -- AWS emulation (decision deferred)

**English** | [Deutsch](0010-aws-emulator.de.md)

- Status: proposed (no emulator selected, nothing implemented)
- Date: 2026-11-12
- Deciders: repository owner

## Context

An AWS demo should show cloud concepts without AWS cost. A candidate named
"Floci" was mentioned in the specification but not verified. LocalStack is the
best-known emulator; its free community edition has limited API coverage and
licensing terms that must be checked for the exact version.

## Decision

Do not select an emulator yet. Before Lab 07 is implemented: verify the concrete
project, its maintenance status, API coverage, license and CI compatibility.
Real AWS resources stay disabled and require explicit approval with cost
estimate, region, TTL and cleanup plan.

## Alternatives considered

- LocalStack community edition: verify coverage/license for the chosen resource.
- Moto (Python mock): good for unit-level tests, not a full endpoint emulator.
- Real AWS with budget alarm: costs money, requires approval.

## Consequences

- No AWS-related claim appears in the documentation.
- Lab 07 remains `planned` until the evaluation is documented.
