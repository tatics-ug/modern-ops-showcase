# ADR 0002 -- GitHub Pages for the public website

**English** | [Deutsch](0002-github-pages-static-hosting.de.md)

- Status: accepted
- Date: 2026-11-12
- Deciders: repository owner

## Context

The website must present the project, be cheap, and must not run any backend. The
custom domain `modern-ops-showcase.tatics.de` is a subdomain of an existing zone
controlled by the owner.

## Decision

Publish a static site with GitHub Pages, deployed by GitHub Actions from the
`website/` build output. Pages serves static files only; it never runs
containers, databases or agents. DNS changes remain a manual, owner-executed
step and are documented in the runbook.

## Alternatives considered

- Netlify/Vercel/Cloudflare Pages: free tiers exist, but add a third-party
  dependency and an account.
- Own server: costs money and adds operations overhead.
- No website: fails the product goal.

## Consequences

- Zero cost, HTTPS via GitHub, simple rollback by re-running a deployment.
- No server-side features; interactive demos must run in Actions or locally.
- Custom domain requires a DNS CNAME record created by the owner.
