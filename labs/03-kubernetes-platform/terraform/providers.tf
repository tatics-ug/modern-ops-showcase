# The cluster is created outside Terraform (kind), see ../tests/run_lab.sh and
# ADR 0005. Terraform only manages resources inside the existing cluster, so it
# has no power to create or destroy the cluster itself.
provider "kubernetes" {
  config_path = var.kubeconfig_path
}
