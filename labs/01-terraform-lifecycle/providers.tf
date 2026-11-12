# The local provider writes files on the machine running Terraform (or the CI
# runner). It needs no credentials, no cloud account and no network access
# after `terraform init` has cached the provider.
provider "local" {}
