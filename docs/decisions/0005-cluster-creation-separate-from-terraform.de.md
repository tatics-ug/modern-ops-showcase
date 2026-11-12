# ADR 0005 -- Cluster-Erzeugung vom Terraform-Ressourcenmanagement trennen

**Deutsch** | [English](0005-cluster-creation-separate-from-terraform.md)

- Status: accepted
- Datum: 2026-11-12
- Entscheider: Repository-Eigentümer

## Kontext

Der Kubernetes-Provider von Terraform verwaltet Ressourcen in einem bestehenden
Cluster; er legt den Cluster nicht an. Beide Verantwortlichkeiten in einem apply
zu vermischen, versteckt die Abhängigkeit und macht `destroy` riskant.

## Entscheidung

Das Lab-Skript legt den kind-Cluster und seine kubeconfig an, danach verwaltet
Terraform nur namensraumgebundene Objekte (`namespace`, `configmap`,
`deployment`, `service`). Terraform-Output/-State referenziert den Cluster nie als
Ressource.

## Verworfene Alternativen

- Terraform ruft kind zusätzlich über Provisioner auf: benötigt local-exec,
  undurchsichtige Fehler, Probleme mit der Destroy-Reihenfolge.
- Cluster-Terraform-Provider (z. B. für verwaltete Dienste): kosten Geld,
  Cloud-Kopplung.

## Konsequenzen

- `terraform destroy` kann den Cluster nie löschen.
- Zwei Schritte müssen dokumentiert werden (`cluster-up` vor `apply`).
- Dieselbe Trennung lässt sich später auf echte Cluster übertragen.

---

*Deutsche Fassung; maßgeblich ist die englische Originalfassung. Die Übersetzung kann hinter der englischen Version zurückliegen.*
