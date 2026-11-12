locals {
  # The module needs an absolute path; the variable itself stays relative and
  # validated so the lab can never write outside its own directory.
  workspace_abs_dir = "${path.module}/${var.workspace_dir}"

  # Static, deterministic tag set: no timestamp() or uuid(), otherwise every
  # plan would show a diff and the idempotency test would be meaningless.
  tags = {
    project     = "modern-ops-showcase"
    lab         = "01-terraform-lifecycle"
    owner       = var.owner
    environment = var.environment
    managed_by  = "terraform"
  }
}

module "demo_workspace" {
  source = "./modules/demo_workspace"

  workspace_dir        = local.workspace_abs_dir
  workspace_name       = var.workspace_name
  environment          = var.environment
  file_permission      = var.file_permission
  sensitive_demo_value = var.sensitive_demo_value
  tags                 = local.tags
}
