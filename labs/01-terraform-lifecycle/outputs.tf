output "workspace_dir" {
  description = "Path of the generated demo workspace, relative to the lab directory."
  value       = module.demo_workspace.workspace_path
}

output "workspace_name" {
  description = "Logical name of the demo workspace."
  value       = var.workspace_name
}

output "metadata_path" {
  description = "Path of the generated metadata.json, relative to the lab directory."
  value       = module.demo_workspace.metadata_path
}

output "metadata_sha256" {
  description = "SHA-256 of metadata.json as written by Terraform."
  value       = module.demo_workspace.metadata_sha256
}

output "runtime_config_path" {
  description = "Path of the generated runtime.conf, relative to the lab directory."
  value       = module.demo_workspace.runtime_config_path
}

output "file_count" {
  description = "Number of files the module manages."
  value       = module.demo_workspace.file_count
}

output "sensitive_demo_value" {
  description = "Dummy sensitive value, redacted in plan/apply output and CLI output."
  value       = module.demo_workspace.sensitive_demo_value
  sensitive   = true
}
