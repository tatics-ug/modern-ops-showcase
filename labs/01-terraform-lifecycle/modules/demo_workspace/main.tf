locals {
  metadata_content = jsonencode({
    workspace_name = var.workspace_name
    environment    = var.environment
    provider       = "hashicorp/local"
    module         = "demo_workspace"
    managed_by     = "terraform"
    tags           = var.tags
  })

  metadata_path = "${var.workspace_dir}/metadata.json"
}

# Non-sensitive artefact: the machine readable summary of the workspace.
resource "local_file" "metadata" {
  filename        = local.metadata_path
  content         = local.metadata_content
  file_permission = var.file_permission
}

# Non-sensitive artefact rendered from a template, to demonstrate templatefile().
resource "local_file" "runtime_config" {
  filename = "${var.workspace_dir}/runtime.conf"
  content = templatefile("${path.module}/templates/runtime.conf.tftpl", {
    workspace_name = var.workspace_name
    environment    = var.environment
    tags_json      = jsonencode(var.tags)
  })
  file_permission = var.file_permission
}

# Sensitive artefact: mode 0600 and content flagged sensitive. This is a dummy
# value; it exists to show that sensitive values are redacted in the CLI and
# that they still live in the state file, which is why the state is protected.
resource "local_sensitive_file" "demo_credential" {
  filename        = "${var.workspace_dir}/demo-credential.txt"
  content         = var.sensitive_demo_value
  file_permission = "0600"
}

# Integrity manifest: hashes of the other artefacts, written after they exist.
resource "local_file" "checksums" {
  filename = "${var.workspace_dir}/checksums.txt"
  content = join("\n", [
    "metadata.json      ${sha256(local.metadata_content)}",
    "runtime.conf       ${sha256(local_file.runtime_config.content)}",
  ])
  file_permission = var.file_permission
}
