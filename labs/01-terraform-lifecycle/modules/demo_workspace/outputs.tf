output "workspace_path" {
  description = "Path of the generated workspace directory as managed by Terraform."
  value       = var.workspace_dir
}

output "metadata_path" {
  description = "Path of metadata.json as managed by Terraform."
  value       = local_file.metadata.filename
}

output "metadata_sha256" {
  description = "SHA-256 of the metadata content managed by Terraform."
  value       = local_file.metadata.content_sha256
}

output "runtime_config_path" {
  description = "Path of runtime.conf as managed by Terraform."
  value       = local_file.runtime_config.filename
}

output "sensitive_demo_value" {
  description = "Dummy sensitive value (redacted in CLI output)."
  value       = local_sensitive_file.demo_credential.content
  sensitive   = true
}

output "file_count" {
  description = "Number of files managed by this module."
  value = length([
    local_file.metadata,
    local_file.runtime_config,
    local_sensitive_file.demo_credential,
    local_file.checksums,
  ])
}
