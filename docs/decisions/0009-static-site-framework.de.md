# ADR 0009 -- MkDocs Material für die Website

**Deutsch** | [English](0009-static-site-framework.md)

- Status: accepted
- Datum: 2026-11-12
- Entscheider: Repository-Eigentümer

## Kontext

Die Seite soll Markdown-basiert, leicht zu pflegen, barrierefrei, schnell zu
bauen und mit GitHub Pages kompatibel sein.

## Entscheidung

MkDocs mit dem Material-Theme verwenden, gepinnt in
`website/requirements.txt`, in der CI und lokal mit `--strict` gebaut
(`.venv` für die Entwicklung).

## Verworfene Alternativen

- Astro: mehr Designfreiheit, Node-Toolchain und mehr Pflegeaufwand.
- Reines HTML/CSS: volle Kontrolle, aber manuelle Navigation, Suche und SEO.
- Jekyll: GitHub-Pages-nativ, aber langsamere Builds und weniger Komponenten.

## Konsequenzen

- Markdown-first, Suche und responsive Navigation ohne Zusatzaufwand.
- Python-Toolchain (für die Tests ohnehin vorhanden) statt Node.
- Diagramme über Mermaid-Codeblöcke.

---

*Deutsche Fassung; maßgeblich ist die englische Originalfassung. Die Übersetzung kann hinter der englischen Version zurückliegen.*
