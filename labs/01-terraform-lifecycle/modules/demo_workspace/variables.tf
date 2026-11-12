variable "workspace_dir" {
  description = "Absolute directory that receives the generated files."
  type        = string
}

variable "workspace_name" {
  description = "Logical name of the demo workspace."
  type        = string
}

variable "environment" {
  description = "Environment label written into the generated files."
  type        = string
}

variable "file_permission" {
  description = "POSIX permission for the non-sensitive files."
  type        = string
}

variable "sensitive_demo_value" {
  description = "Dummy value written to a file with mode 0600 to demonstrate sensitive handling."
  type        = string
  sensitive   = true
}

variable "tags" {
  description = "Tags written into metadata.json."
  type        = map(string)
}
