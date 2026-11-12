# ADR 0001 -- One repository at the start

**English** | [Deutsch](0001-single-repository.de.md)

- Status: accepted
- Date: 2026-11-12
- Deciders: repository owner

## Context

The showcase contains labs (Terraform, Kubernetes, later Ansible, GitOps,
observability, DevSecOps, AWS emulation, AI infrastructure), a website, CI and an
agentic pipeline. Splitting into multiple repositories would multiply CI setups,
secret scopes and cross-repository versioning from day one.

## Decision

Use exactly one repository (`tatics-ug/modern-ops-showcase`) and organise modules
in directories. Split only when there is a concrete technical or organisational
reason.

## Alternatives considered

- One repository per lab: better isolation, but duplicated CI, more maintenance.
- Monorepo plus published artefacts: unnecessary for a showcase.

## Consequences

- Simple onboarding, one branch protection, one Pages setup.
- Lab directories must stay independent (each has its own Makefile and state).
- A later split is still possible; nothing depends on the monorepo layout.
