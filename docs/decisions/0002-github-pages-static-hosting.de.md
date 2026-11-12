# ADR 0002 -- GitHub Pages für die öffentliche Website

**Deutsch** | [English](0002-github-pages-static-hosting.md)

- Status: accepted
- Datum: 2026-11-12
- Entscheider: Repository-Eigentümer

## Kontext

Die Website soll das Projekt präsentieren, günstig sein und kein Backend
betreiben. Die eigene Domain `modern-ops-showcase.tatics.de` ist eine Subdomain
einer bestehenden Zone, die der Eigentümer kontrolliert.

## Entscheidung

Eine statische Seite mit GitHub Pages veröffentlichen, deployt von GitHub Actions
aus dem Build-Output von `website/`. Pages liefert nur statische Dateien aus; es
laufen nie Container, Datenbanken oder Agenten. DNS-Änderungen bleiben ein
manueller, vom Eigentümer ausgeführter Schritt und sind im Runbook dokumentiert.

## Verworfene Alternativen

- Netlify/Vercel/Cloudflare Pages: kostenlose Tarife existieren, bringen aber eine
  Drittanbieter-Abhängigkeit und ein Konto mit.
- Eigener Server: kostet Geld und erzeugt Betriebsaufwand.
- Keine Website: verfehlt das Produktziel.

## Konsequenzen

- Keine Kosten, HTTPS über GitHub, einfaches Rollback durch erneutes Ausführen
  eines Deployments.
- Keine serverseitigen Funktionen; interaktive Demos müssen in Actions oder lokal
  laufen.
- Die eigene Domain erfordert einen DNS-CNAME-Eintrag, den der Eigentümer anlegt.

---

*Deutsche Fassung; maßgeblich ist die englische Originalfassung. Die Übersetzung kann hinter der englischen Version zurückliegen.*
