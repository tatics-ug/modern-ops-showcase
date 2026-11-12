# Lab 03 -- Kubernetes Application Platform
#
# Cluster creation is intentionally separate from Terraform: kind creates the
# cluster, Terraform manages only resources inside it (see ADR 0005).

LAB_DIR := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))
TF ?= terraform
PYTHON ?= python3
KUBECONFIG ?= $(LAB_DIR)/kind/kubeconfig
CLUSTER ?= modernops-lab03
IMAGE ?= modernops-showcase/demo-app:local
TFCMD := $(TF) -chdir="$(LAB_DIR)/terraform"
export KUBECONFIG

.DEFAULT_GOAL := help
.PHONY: help cluster-up cluster-down build load init fmt-check validate plan apply test fault lifecycle destroy clean

help: ## Show this help
	@grep -hE '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

cluster-up: ## Create the temporary kind cluster
	kind create cluster --name $(CLUSTER) --config "$(LAB_DIR)/kind/kind-config.yaml" \
		--kubeconfig "$(KUBECONFIG)" --wait 120s

cluster-down: ## Delete the temporary kind cluster (only this one)
	kind delete cluster --name $(CLUSTER)
	rm -f "$(KUBECONFIG)"

build: ## Build the demo application image locally
	docker build -t $(IMAGE) "$(LAB_DIR)/app"

load: ## Load the locally built image into the kind cluster
	kind load docker-image $(IMAGE) --name $(CLUSTER)

init: ## Initialise Terraform providers
	$(TFCMD) init -input=false

fmt-check: ## Fail if the Terraform configuration is not formatted
	$(TFCMD) fmt -check -recursive

validate: init ## Validate the Terraform configuration
	$(TFCMD) validate

plan: init ## Show the planned Kubernetes resources
	$(TFCMD) plan -input=false

apply: init ## Create the Kubernetes resources
	$(TFCMD) apply -input=false -auto-approve

test: ## Run the integration tests against the running cluster
	cd "$(LAB_DIR)" && $(PYTHON) -m pytest tests -q

fault: init ## Provoke the deliberate fault (missing image tag)
	$(TFCMD) apply -input=false -auto-approve \
		-var "app_image_tag=missing" -var "image_pull_policy=Never"
	cd "$(LAB_DIR)" && EXPECT_FAULT=1 $(PYTHON) -m pytest tests -q -k test_fault_is_detected

lifecycle: ## Full lifecycle: cluster, image, apply, tests, fault, fix, cleanup, evidence
	cd "$(LAB_DIR)" && bash tests/run_lab.sh

destroy: init ## Remove the Kubernetes resources managed by Terraform
	$(TFCMD) destroy -input=false -auto-approve

clean: ## Remove local state, evidence and the lab kubeconfig
	rm -rf "$(LAB_DIR)/.pytest_cache" "$(LAB_DIR)/evidence" "$(LAB_DIR)/kind/kubeconfig" \
		"$(LAB_DIR)/terraform/.terraform" "$(LAB_DIR)/terraform/terraform.tfstate" \
		"$(LAB_DIR)/terraform/terraform.tfstate.backup" "$(LAB_DIR)/terraform/lab.tfplan" \
		"$(LAB_DIR)/tests/__pycache__" "$(LAB_DIR)/app/tests/__pycache__"
