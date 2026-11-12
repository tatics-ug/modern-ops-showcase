variable "kubeconfig_path" {
  description = "Kubeconfig of the existing kind cluster (created outside Terraform)."
  type        = string
  default     = "../kind/kubeconfig"
}

variable "namespace" {
  description = "Namespace that contains the demo application."
  type        = string
  default     = "demo"

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{1,30}$", var.namespace))
    error_message = "namespace must be a DNS label: lowercase letters, digits and hyphens."
  }
}

variable "app_name" {
  description = "Name of the demo application (also used for labels)."
  type        = string
  default     = "demo-app"
}

variable "app_image_repository" {
  description = "Image repository built locally and loaded into the kind cluster."
  type        = string
  default     = "modernops-showcase/demo-app"
}

variable "app_image_tag" {
  description = "Image tag. Use a tag that does not exist to provoke the fault scenario."
  type        = string
  default     = "local"

  validation {
    condition     = can(regex("^[A-Za-z0-9_][A-Za-z0-9_.-]{0,127}$", var.app_image_tag))
    error_message = "app_image_tag must be a valid container image tag."
  }
}

variable "image_pull_policy" {
  description = "ImagePullPolicy. 'Never' makes the fault scenario fail fast without network access."
  type        = string
  default     = "IfNotPresent"

  validation {
    condition     = contains(["Always", "IfNotPresent", "Never"], var.image_pull_policy)
    error_message = "image_pull_policy must be one of: Always, IfNotPresent, Never."
  }
}

variable "replicas" {
  description = "Number of application replicas."
  type        = number
  default     = 2

  validation {
    condition     = var.replicas >= 1 && var.replicas <= 5
    error_message = "replicas must be between 1 and 5."
  }
}
