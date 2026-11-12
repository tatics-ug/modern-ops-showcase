locals {
  selector_labels = {
    "app.kubernetes.io/name"       = var.app_name
    "app.kubernetes.io/part-of"    = "modernops-showcase"
    "app.kubernetes.io/managed-by" = "terraform"
  }

  image = "${var.app_image_repository}:${var.app_image_tag}"
}

resource "kubernetes_namespace_v1" "demo" {
  metadata {
    name = var.namespace
    labels = {
      "app.kubernetes.io/part-of"    = "modernops-showcase"
      "app.kubernetes.io/managed-by" = "terraform"
      "modernops/lab"                = "03-kubernetes-platform"
    }
  }
}

resource "kubernetes_config_map_v1" "app" {
  metadata {
    name      = "${var.app_name}-config"
    namespace = kubernetes_namespace_v1.demo.metadata[0].name
  }

  data = {
    APP_NAME    = var.app_name
    APP_VERSION = var.app_image_tag
    PORT        = "8080"
  }
}

resource "kubernetes_deployment_v1" "app" {
  # The tests wait for the rollout explicitly. Without this the fault scenario
  # would block the apply for five minutes and fail before it can be diagnosed.
  wait_for_rollout = false

  metadata {
    name      = var.app_name
    namespace = kubernetes_namespace_v1.demo.metadata[0].name
    labels    = local.selector_labels
  }

  spec {
    replicas = var.replicas

    selector {
      match_labels = {
        "app.kubernetes.io/name" = var.app_name
      }
    }

    template {
      metadata {
        labels = local.selector_labels
      }

      spec {
        automount_service_account_token = false
        enable_service_links            = false

        security_context {
          run_as_non_root = true
          run_as_user     = 10001
          run_as_group    = 10001

          seccomp_profile {
            type = "RuntimeDefault"
          }
        }

        container {
          name              = var.app_name
          image             = local.image
          image_pull_policy = var.image_pull_policy

          port {
            name           = "http"
            container_port = 8080
          }

          env_from {
            config_map_ref {
              name = kubernetes_config_map_v1.app.metadata[0].name
            }
          }

          resources {
            requests = {
              cpu    = "25m"
              memory = "32Mi"
            }
            limits = {
              cpu    = "200m"
              memory = "128Mi"
            }
          }

          liveness_probe {
            http_get {
              path = "/healthz"
              port = "http"
            }
            initial_delay_seconds = 3
            period_seconds        = 5
            timeout_seconds       = 2
            failure_threshold     = 3
          }

          readiness_probe {
            http_get {
              path = "/readyz"
              port = "http"
            }
            initial_delay_seconds = 2
            period_seconds        = 3
            timeout_seconds       = 2
            failure_threshold     = 2
          }

          security_context {
            allow_privilege_escalation = false
            read_only_root_filesystem  = true

            capabilities {
              drop = ["ALL"]
            }
          }
        }
      }
    }
  }

  # Do not fail the apply while a rollout is still in progress; the test suite
  # waits for the rollout explicitly and reports the real state.
  timeouts {
    create = "5m"
    update = "5m"
  }
}

resource "kubernetes_service_v1" "app" {
  metadata {
    name      = var.app_name
    namespace = kubernetes_namespace_v1.demo.metadata[0].name
    labels    = local.selector_labels
  }

  spec {
    type = "ClusterIP"

    selector = {
      "app.kubernetes.io/name" = var.app_name
    }

    port {
      name        = "http"
      port        = 80
      target_port = "http"
      protocol    = "TCP"
    }
  }
}
