# ModernOps Showcase

**Moderne Infrastruktur & Agentic Engineering** -- ein reproduzierbares,
praxisnahes Showcase. Erkunde Linux-Automatisierung, Terraform, Kubernetes,
Cloud-Infrastruktur, CI/CD, Observability, Sicherheit und KI-gestützte
Softwareentwicklung, integriert in einem transparenten Referenzprojekt.

[:octicons-arrow-right-24: Labs ansehen](labs/index.md){ .md-button .md-button--primary }
[:octicons-mark-github-16: Quellcode](https://github.com/tatics-ug/modern-ops-showcase){ .md-button }

## Was tatsächlich ausführbar ist

| Lab | Was es zeigt | Status |
| --- | --- | --- |
| Lab 01 | Terraform-Lebenszyklus: Module, Validierung, Plan/Apply, State, Destroy, Drift | `validated` (lokal) |
| Lab 03 | Kubernetes-Plattform auf kind: Deployment, Probes, Limits, Fehlerfall | `validated` (CI) |

Alles andere in diesem Projekt (Ansible, GitOps, Observability, DevSecOps,
AWS-Emulation, KI-Infrastruktur) ist **planned** und als solches gekennzeichnet.
Kein Dashboard, keine Metrik und kein Benchmark auf dieser Seite ist erfunden --
was nicht implementiert ist, sagt das auch.

## Wie das Projekt gebaut ist

- **Infrastructure as Code** mit Terraform, lokalem State, reproduzierbaren Plänen.
- **Echte Kubernetes-Workloads** in einem temporären kind-Cluster, der nach der
  Demo gelöscht wird, damit niemand für Leerlaufressourcen zahlt.
- **Automatisierter Nachweis**: Jeder Lab-Lauf schreibt ein strukturiertes
  Nachweis-Dokument.
- **CI auf GitHub Actions** mit Berechtigungen nach dem Prinzip der geringsten
  Rechte und kostenlosen Runnern.
- **Agentic Engineering**: eine geskriptete Issue-zu-PR-Pipeline mit Triage, Plan,
  begrenzter Änderung, Tests, unabhängigem Review, PR und menschlichem Merge-Gate.

## Von Grund auf kostenlos

Kein Cloud-Konto, kein API-Schlüssel, keine GPU, keine Kreditkarte. Das gesamte
Showcase läuft mit kostenlosen Werkzeugen: GitHub Free, GitHub Pages, standardmäßige
GitHub-gehostete Runner (kostenlos für öffentliche Repositories), Terraform, kind,
Docker, Python und MkDocs Material.

!!! warning "Ehrliche Kennzeichnung"
    Live-KI-Agenten-Läufe sind **nicht** aktiviert. Die Agentic-Pipeline in diesem
    Repository ist deterministisch und enthält kein Sprachmodell; das wird auf
    jedem erzeugten Artefakt gesagt.

---

*Deutsche Fassung; maßgeblich ist die englische Originalfassung. Die Übersetzung kann hinter der englischen Version zurückliegen.*
