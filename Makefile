# ModernOps Showcase -- top-level demo and validation interface.
#
#   make demo-list                 show available scenarios
#   make demo-up   SCENARIO=01     prepare a scenario
#   make demo-run  SCENARIO=01     execute it (writes evidence)
#   make demo-reset SCENARIO=01    reset generated resources
#   make demo-down SCENARIO=01     remove everything the scenario created
#
# Only dedicated demo resources are touched: lab directories under labs/,
# the kind cluster "modernops-lab03" and local Terraform state inside the labs.

SCENARIO ?=
PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)
LAB01 := labs/01-terraform-lifecycle
LAB03 := labs/03-kubernetes-platform
MKDOCS := $(if $(wildcard website/.venv/bin/mkdocs),website/.venv/bin/mkdocs,mkdocs)

.DEFAULT_GOAL := help
.PHONY: help demo-list demo-up demo-run demo-reset demo-down clean-demo validate website website-serve clean

help: ## Show this help
	@grep -hE '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

demo-list: ## List the reproducible demo scenarios
	@printf '  %-4s %-42s %s\n' "ID" "SCENARIO" "STATUS"
	@printf '  %-4s %-42s %s\n' "01" "Terraform infrastructure lifecycle" "validated (local)"
	@printf '  %-4s %-42s %s\n' "03" "Kubernetes application platform" "implemented"
	@printf '\n  Run: make demo-run SCENARIO=01\n'

demo-up: ## Prepare a scenario (make demo-up SCENARIO=01|03)
	@case "$(SCENARIO)" in \
	  01) $(MAKE) -C $(LAB01) init ;; \
	  03) $(MAKE) -C $(LAB03) cluster-up build load ;; \
	  *) echo "unknown scenario '$(SCENARIO)' (use 01 or 03)"; exit 2 ;; \
	esac

demo-run: ## Execute a scenario end to end and write evidence
	@case "$(SCENARIO)" in \
	  01) $(MAKE) -C $(LAB01) lifecycle ;; \
	  03) $(MAKE) -C $(LAB03) lifecycle ;; \
	  *) echo "unknown scenario '$(SCENARIO)' (use 01 or 03)"; exit 2 ;; \
	esac

demo-reset: ## Reset generated resources of a scenario (keeps the cluster up)
	@case "$(SCENARIO)" in \
	  01) $(MAKE) -C $(LAB01) destroy; rm -rf $(LAB01)/workspace ;; \
	  03) $(MAKE) -C $(LAB03) destroy ;; \
	  *) echo "unknown scenario '$(SCENARIO)' (use 01 or 03)"; exit 2 ;; \
	esac

demo-down: ## Remove everything a scenario created
	@case "$(SCENARIO)" in \
	  01) $(MAKE) -C $(LAB01) destroy clean ;; \
	  03) $(MAKE) -C $(LAB03) destroy cluster-down clean ;; \
	  *) echo "unknown scenario '$(SCENARIO)' (use 01 or 03)"; exit 2 ;; \
	esac

clean-demo: ## Alias for demo-down (make clean-demo SCENARIO=01|03)
	@$(MAKE) demo-down SCENARIO=$(SCENARIO)

validate: ## Run repository checks (python tests, evidence schema, formatting)
	$(PYTHON) -m pytest tests -q
	$(PYTHON) scripts/validate_evidence.py
	$(MAKE) -C $(LAB01) fmt-check
	$(MAKE) -C $(LAB03) fmt-check

website: ## Build the static website
	$(MKDOCS) build --strict --config-file website/mkdocs.yml

website-serve: ## Serve the website locally on http://127.0.0.1:8000
	$(MKDOCS) serve --config-file website/mkdocs.yml

clean: ## Remove local build artifacts (site, caches, lab state)
	rm -rf website/site .pytest_cache tests/__pycache__ scripts/__pycache__
	rm -rf $(LAB01)/.terraform $(LAB01)/terraform.tfstate $(LAB01)/terraform.tfstate.backup \
		$(LAB01)/workspace $(LAB01)/evidence $(LAB01)/lab.tfplan
	rm -rf $(LAB03)/evidence $(LAB03)/kind/kubeconfig $(LAB03)/terraform/.terraform \
		$(LAB03)/terraform/terraform.tfstate $(LAB03)/terraform/terraform.tfstate.backup
