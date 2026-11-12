output "namespace" {
  description = "Namespace that contains the demo application."
  value       = kubernetes_namespace_v1.demo.metadata[0].name
}

output "deployment_name" {
  description = "Name of the application Deployment."
  value       = kubernetes_deployment_v1.app.metadata[0].name
}

output "service_name" {
  description = "Name of the ClusterIP Service."
  value       = kubernetes_service_v1.app.metadata[0].name
}

output "image" {
  description = "Container image that is requested by the Deployment."
  value       = local.image
}

output "replicas" {
  description = "Desired replica count."
  value       = var.replicas
}
