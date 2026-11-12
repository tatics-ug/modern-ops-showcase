variable "workspace_dir" {
  description = "Relative directory (inside this lab) that receives the generated files."
  type        = string
  default     = "workspace"

  validation {
    condition = (
      var.workspace_dir != "" &&
      !startswith(var.workspace_dir, "/") &&
      !strcontains(var.workspace_dir, "..")
    )
    error_message = "workspace_dir must be a non-empty relative path without '..' so that the lab only writes inside its own directory."
  }
}

variable "workspace_name" {
  description = "Logical name of the demo workspace. Also used as a file prefix in the generated metadata."
  type        = string
  default     = "lab01-demo"

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,30}$", var.workspace_name))
    error_message = "workspace_name must match ^[a-z][a-z0-9-]{2,30}$: lowercase letters, digits and hyphens, 3 to 31 characters."
  }
}

variable "environment" {
  description = "Target environment label written into the generated files."
  type        = string
  default     = "demo"

  validation {
    condition     = contains(["demo", "dev", "test"], var.environment)
    error_message = "environment must be one of: demo, dev, test."
  }
}

variable "owner" {
  description = "Owner label used for the resource tags."
  type        = string
  default     = "modernops-showcase"
}

variable "file_permission" {
  description = "POSIX permission of the generated, non-sensitive files."
  type        = string
  default     = "0644"

  validation {
    condition     = can(regex("^0[0-7]{3}$", var.file_permission))
    error_message = "file_permission must be a four digit octal mode such as 0644 or 0600."
  }
}

variable "sensitive_demo_value" {
  description = "Dummy value used to demonstrate redaction of sensitive values. Never put a real credential here."
  type        = string
  default     = "demo-only-placeholder-not-a-secret"
  sensitive   = true
}
