# Lab 01 -- Terraform Infrastructure Lifecycle
#
# All targets run inside this lab directory, so `make -C labs/01-terraform-lifecycle <target>`
# behaves exactly like running the target from inside the directory.
#
# Override the binary with e.g. `make TF=tofu plan`; the configuration is
# compatible with Terraform >= 1.6 and OpenTofu >= 1.6.

LAB_DIR := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))
TF ?= terraform
RUN := cd "$(LAB_DIR)" && $(TF)
PYTHON ?= python3

.DEFAULT_GOAL := help
.PHONY: help init fmt fmt-check validate plan apply output test lifecycle evidence destroy clean

help: ## Show this help
	@grep -hE '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

init: ## Download providers and initialise the local backend
	$(RUN) init -input=false

fmt: ## Rewrite configuration files to canonical format
	$(RUN) fmt -recursive

fmt-check: ## Fail if any file is not canonically formatted
	$(RUN) fmt -check -recursive

validate: init ## Validate the configuration
	$(RUN) validate

plan: init ## Create a plan and save it as lab.tfplan
	$(RUN) plan -input=false -out=lab.tfplan

apply: init ## Apply the current configuration
	$(RUN) apply -input=false -auto-approve

output: ## Show all outputs (sensitive values stay redacted)
	$(RUN) output

test: ## Run the automated verification against an applied workspace
	cd "$(LAB_DIR)" && TF="$(TF)" TF_BIN="$(TF)" $(PYTHON) -m pytest tests -q

lifecycle: ## Full lifecycle: init, fmt, validate, plan, apply, test, destroy, evidence
	cd "$(LAB_DIR)" && bash tests/run_lifecycle.sh

evidence: ## Run the full lifecycle (alias, writes evidence JSON)
	$(MAKE) lifecycle

destroy: ## Remove everything this lab created
	$(RUN) destroy -input=false -auto-approve

clean: ## Remove local Terraform working data and generated artefacts
	cd "$(LAB_DIR)" && rm -rf .terraform lab.tfplan workspace evidence .pytest_cache tests/__pycache__
	cd "$(LAB_DIR)" && rm -f terraform.tfstate terraform.tfstate.backup
