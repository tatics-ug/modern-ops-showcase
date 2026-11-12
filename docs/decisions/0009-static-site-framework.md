# ADR 0009 -- MkDocs Material for the website

**English** | [Deutsch](0009-static-site-framework.de.md)

- Status: accepted
- Date: 2026-11-12
- Deciders: repository owner

## Context

The site must be Markdown-based, easy to maintain, accessible, fast to build and
compatible with GitHub Pages.

## Decision

Use MkDocs with the Material theme, pinned in `website/requirements.txt`, built
with `--strict` in CI and locally (`.venv` for development).

## Alternatives considered

- Astro: more design freedom, Node toolchain and more maintenance.
- Plain HTML/CSS: full control but manual navigation, search and SEO.
- Jekyll: GitHub Pages native, but slower builds and fewer components.

## Consequences

- Markdown-first, search and responsive navigation for free.
- Python toolchain (already present for tests) instead of Node.
- Diagrams via Mermaid code fences.
