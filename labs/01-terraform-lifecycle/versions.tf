terraform {
  # Terraform 1.6 or newer: `terraform_data`, stable `strcontains`, local backend.
  required_version = ">= 1.6.0, < 2.0.0"

  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }

  # Local state on purpose: this lab must not depend on any remote backend or
  # cloud account. The state file is git-ignored, see README.md section
  # "State handling and security".
  backend "local" {}
}
