# Lab 03 -- Kubernetes-Anwendungsplattform

**Deutsch** | [English](README.md)

Führt eine kleine, echte Anwendung in einem echten (temporären)
Kubernetes-Cluster aus, provisioniert den Workload deklarativ mit Terraform,
belegt per automatisierten Tests, dass er gesund ist, bricht ihn absichtlich,
erkennt den Fehler, repariert ihn und entfernt alles wieder.

Cluster-Tooling: **Docker + kind**. Provisionierung: **Terraform-Provider
`hashicorp/kubernetes`**. Kein Cloud-Konto, kein managed Kubernetes, keine Kosten.

Status: **validated** -- der Workflow `demo-kubernetes` hat den vollständigen
Lebenszyklus erfolgreich ausgeführt (Cluster hoch, Apply, Tests,
Fehlererkennung, Reparatur, Destroy, Cluster löschen):
https://github.com/tatics-ug/modern-ops-showcase/actions/runs/43256482922

---

## 1. Zweck

| Frage | Antwort in diesem Lab |
| --- | --- |
| Wird ein Deployment Ready? | `kubectl wait --for=condition=available` in den Tests |
| Ist der Service erreichbar? | port-forward + echte HTTP-Anfragen (`/healthz`, `/api/info`) |
| Sind Probes, Limits und Security Context korrekt? | Tests prüfen die Live-Deployment-Spezifikation |
| Wird ein kaputtes Image erkannt? | Image-Tag `missing` + `imagePullPolicy: Never` -> `ErrImageNeverPull` |
| Lässt sich der Fehler reparieren? | Sollzustand erneut anwenden, alle Tests wieder grün |
| Ist das Aufräumen vollständig? | Terraform destroy + kind-Cluster löschen, vom Skript geprüft |

## 2. Voraussetzungen

- Docker läuft und ist für den aktuellen Benutzer nutzbar
- `kind` >= 0.2x, `kubectl`, Terraform >= 1.6 (oder OpenTofu >= 1.6), Python 3.9+ mit `pytest`
- ~2 GB freier Speicher für das kind-Node-Image, Netzzugang bei der ersten Cluster-Erzeugung
- Keine Cloud-Credentials, kein vorab vorhandener Kubernetes-Cluster

## 3. Architektur

```text
Host-Maschine
├── docker
│   └── kind-Cluster "modernops-lab03" (temporär, danach gelöscht)
│       └── Namespace demo                   <- von Terraform verwaltet
│           ├── ConfigMap demo-app-config
│           ├── Deployment demo-app (2 Replicas)
│           │   ├── image: modernops-showcase/demo-app:local (lokal gebaut, in kind geladen)
│           │   ├── liveness  /healthz
│           │   ├── readiness /readyz
│           │   ├── requests 25m/32Mi, limits 200m/128Mi
│           │   └── runAsNonRoot, schreibgeschütztes Root-Dateisystem, keine Capabilities
│           └── Service demo-app (ClusterIP, 80 -> 8080)
└── terraform/  (State lokal, git-ignoriert)
```

Cluster-Erzeugung und Ressourcen-Provisionierung sind bewusst getrennt: `kind`
erzeugt den Cluster, Terraform verwaltet nur Objekte in einem bestehenden Cluster
(siehe [ADR 0005](../../docs/decisions/0005-cluster-creation-separate-from-terraform.de.md)).
So kann `terraform destroy` niemals einen Cluster löschen.

## 4. Ausführen

```bash
cd labs/03-kubernetes-platform
make lifecycle            # vollständiger Lauf inkl. Fehlerszenario, Aufräumen, Nachweis
```

Schritt für Schritt:

```bash
make cluster-up           # kind create cluster (nur lokal)
make build                # App-Image mit docker bauen
make load                 # kind load docker-image
make apply                # terraform apply (Namespace, Deployment, Service anlegen)
make test                 # Integrationstests gegen den Live-Cluster
make fault                # bewusster Fehler + Erkennungstest
make apply                # Reparatur
make test                 # wieder grün
make destroy              # Kubernetes-Ressourcen entfernen
make cluster-down         # kind-Cluster löschen
```

Ohne `make`:

```bash
kind create cluster --name modernops-lab03 --config kind/kind-config.yaml --kubeconfig kind/kubeconfig --wait 120s
docker build -t modernops-showcase/demo-app:local app
kind load docker-image modernops-showcase/demo-app:local --name modernops-lab03
terraform -chdir=terraform init && terraform -chdir=terraform apply -auto-approve
KUBECONFIG=kind/kubeconfig python3 -m pytest tests -q
kind delete cluster --name modernops-lab03
```

Erwartete Ergebnisse: 2/2 Replicas Ready, alle Tests im Gesundzustand bestehen
(7 Tests), der Fehlertest bestätigt, dass das Deployment *nicht* verfügbar wird
und die Pods einen Image-Fehler melden, danach wird alles zerstört.

## 5. Der bewusste Fehler

`app_image_tag=missing` kombiniert mit `image_pull_policy=Never` lässt den kubelet
sofort scheitern (`ErrImageNeverPull`), ohne jeden Netzzugriff:

```bash
terraform -chdir=terraform apply -var app_image_tag=missing -var image_pull_policy=Never
kubectl get pods -n demo            # ImagePullBackOff / ErrImageNeverPull
EXPECT_FAULT=1 python3 -m pytest tests -q -k test_fault_is_detected
terraform -chdir=terraform apply    # Reparatur mit dem echten Tag
```

Der Fehlertest prüft *beides*: dass der Rollout nicht innerhalb von 40 s
abgeschlossen wird *und* dass der Container-Status einen Image-Fehler als Grund
trägt. Bei einem Rolling Update behalten die alten, bereiten Pods
`condition=available` auf `true`, weshalb diese Bedingung bewusst nicht als
Signal verwendet wird -- sie würde den Fehler verdecken.

## 6. Tests

| Test | Prüft |
| --- | --- |
| `test_deployment_becomes_available` | Rollout erreicht `Available` |
| `test_replicas_are_ready` | readyReplicas == gewünscht, keine nicht verfügbaren Replicas |
| `test_service_has_endpoints` | Service hat bereite Endpoint-Adressen |
| `test_resources_and_probes_are_configured` | Requests/Limits und Probe-Pfade im Live-Objekt |
| `test_pod_security_context_is_restrictive` | runAsNonRoot, seccomp, keine Capabilities, schreibgeschütztes Dateisystem |
| `test_http_endpoints_respond` | echtes HTTP über port-forward (`/healthz`, `/api/info`) |
| `test_fault_is_detected` | Rollout stockt und neue Pods melden einen Image-Fehler |

App-Unit-Tests (`app/tests/test_app.py`, ohne Cluster): 5 Tests.

## 7. State-Handling und Sicherheit

- Lokaler Terraform-State, git-ignoriert; kein Remote-Backend (das ist ein
  späteres Lab).
- Die kubeconfig wird nach `kind/kubeconfig` geschrieben (git-ignoriert) und mit
  dem Cluster gelöscht.
- Der App-Container läuft als UID 10001, non-root, mit schreibgeschütztem
  Root-Dateisystem, `RuntimeDefault`-seccomp, allen Capabilities entfernt,
  Service-Links deaktiviert, Service-Account-Token nicht eingebunden. Es werden
  keine Image-Pull-Secrets benötigt.
- Das Image ist lokal (`:local`) und wird nie in eine öffentliche Registry
  gepusht.

## 8. Aufräumen

```bash
make destroy       # Terraform-Ressourcen
make cluster-down  # kind-Cluster + kubeconfig
make clean         # State, Nachweise, Caches
```

`tests/run_lab.sh` führt Destroy und Cluster-Löschung bei Erfolg *und* bei Fehler
aus (best effort). Es löscht immer nur den Cluster namens `modernops-lab03` und
die kubeconfig des Labs selbst.

## 9. Nachweis

`tests/run_lab.sh` schreibt `evidence/local-kubernetes.json` (git-ignoriert) mit
Szenario-ID, Ausführungsmodus, Zeitstempeln, Commit, Status je Prüfung und
bekannten Einschränkungen. Der Workflow `demo-kubernetes` lädt die Datei als
Artefakt hoch.

## 10. Bekannte Einschränkungen

- Ein-Node-kind-Cluster: kein Multi-Node-Scheduling, kein Autoscaler.
- Kein Ingress-Controller, kein TLS, kein GitOps -- das sind spätere Labs
  (04/05).
- Das Image wird aus dem lokalen Docker-Daemon geladen, nicht aus einer Registry.
- Die CI führt dasselbe Skript aus, aber der Nachweis ist nur so gut wie der
  letzte Lauf.

---

*Deutsche Fassung; maßgeblich ist die englische Originalfassung. Die Übersetzung kann hinter der englischen Version zurückliegen.*
