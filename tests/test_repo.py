"""Repository-wide consistency tests.

These run without Docker, Kubernetes or network access and are used both locally
(`make validate`) and in CI.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DOCUMENTS = [
    "README.md",
    "AGENTS.md",
    "SECURITY.md",
    "ARCHITECTURE.md",
    "LICENSE",
    "docs/GETTING_STARTED.md",
    "docs/RUNBOOK.md",
    "docs/TECHNOLOGY_MATRIX.md",
    "docs/AGENT_WORKFLOW.md",
]

EXPECTED_ADRS = [
    "0001-single-repository.md",
    "0002-github-pages-static-hosting.md",
    "0003-github-actions-as-execution-layer.md",
    "0004-temporary-kind-clusters.md",
    "0005-cluster-creation-separate-from-terraform.md",
    "0006-replay-as-default-mode.md",
    "0007-byok-for-live-agent-runs.md",
    "0008-agentic-orchestration-path.md",
    "0009-static-site-framework.md",
    "0010-aws-emulator.md",
    "0011-observability-stack.md",
    "0012-kubernetes-policy-technology.md",
]

SECRET_PATTERNS = (
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"-----BEGIN [A-Z ]+PRIVATE KEY-----"),
    re.compile(r"(?i)(api[_-]?key|token|password)\s*[:=]\s*['\"][^'\"]{8,}['\"]"),
)


def tracked_files() -> list[Path]:
    """Files under version control (falls back to a directory walk outside git)."""
    if (REPO_ROOT / ".git").exists():
        import subprocess

        out = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "ls-files"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        return [REPO_ROOT / line for line in out.splitlines() if line.strip()]
    skip = {".git", ".venv", "node_modules", "site", "__pycache__", ".pytest_cache", ".terraform", "evidence"}
    files = []
    for path in REPO_ROOT.rglob("*"):
        if path.is_file() and not any(part in skip for part in path.parts):
            files.append(path)
    return files


def test_required_documents_exist() -> None:
    missing = [name for name in REQUIRED_DOCUMENTS if not (REPO_ROOT / name).is_file()]
    assert not missing, f"missing required documents: {missing}"


def test_all_adrs_exist() -> None:
    missing = [name for name in EXPECTED_ADRS if not (REPO_ROOT / "docs" / "decisions" / name).is_file()]
    assert not missing, f"missing ADRs: {missing}"


def test_workflows_have_explicit_permissions() -> None:
    workflows = sorted((REPO_ROOT / ".github" / "workflows").glob("*.yml"))
    assert workflows, "no workflows found"
    for workflow in workflows:
        data = yaml.safe_load(workflow.read_text(encoding="utf-8"))
        assert "permissions" in data, f"{workflow.name} has no explicit permissions block"
        raw = workflow.read_text(encoding="utf-8")
        assert "pull_request_target" not in raw, f"{workflow.name} must not use pull_request_target"
        # No secrets other than the automatic token may be referenced.
        for match in re.finditer(r"secrets\.([A-Za-z0-9_]+)", raw):
            assert match.group(1) == "GITHUB_TOKEN", f"{workflow.name} references unexpected secret {match.group(1)}"


class _MkDocsLoader(yaml.SafeLoader):
    """SafeLoader plus MkDocs' python/name tags (used for mermaid fences)."""


_MkDocsLoader.add_multi_constructor(
    "tag:yaml.org,2002:python/name:",
    lambda loader, suffix, node: suffix,
)


def load_yaml(path: Path) -> dict:
    return yaml.load(path.read_text(encoding="utf-8"), Loader=_MkDocsLoader)


def test_yaml_files_parse() -> None:
    # mkdocs.yml uses MkDocs-specific tags and is validated by `mkdocs build --strict`.
    for path in sorted(REPO_ROOT.rglob("*.yml")) + sorted(REPO_ROOT.rglob("*.yaml")):
        if any(part in {".venv", "site", ".terraform"} for part in path.parts):
            continue
        if path.name == "mkdocs.yml":
            continue
        yaml.safe_load(path.read_text(encoding="utf-8"))


def test_evidence_examples_validate() -> None:
    jsonschema = pytest.importorskip("jsonschema")
    schema = json.loads((REPO_ROOT / "evidence/schema/scenario-result.schema.json").read_text())
    documents = sorted((REPO_ROOT / "evidence" / "examples").glob("*.json"))
    assert documents, "no evidence examples committed"
    for document in documents:
        jsonschema.validate(json.loads(document.read_text()), schema)


def test_replay_recordings_validate() -> None:
    jsonschema = pytest.importorskip("jsonschema")
    schema = json.loads((REPO_ROOT / "replay/schema/recording.schema.json").read_text())
    for document in sorted((REPO_ROOT / "replay" / "recordings").glob("*.json")):
        jsonschema.validate(json.loads(document.read_text()), schema)


def test_no_secrets_in_tracked_files() -> None:
    hits = []
    text_suffixes = {".md", ".yml", ".yaml", ".json", ".py", ".sh", ".tf", ".txt", ".tftpl", ""}
    for path in tracked_files():
        if path.suffix not in text_suffixes or not path.is_file():
            continue
        if path.name == "test_repo.py":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                hits.append(f"{path.relative_to(REPO_ROOT)}: {pattern.pattern}")
    assert not hits, f"possible secrets found: {hits}"


def test_state_and_env_files_are_git_ignored() -> None:
    if not (REPO_ROOT / ".git").exists():
        pytest.skip("not a git repository")
    import subprocess

    for candidate in (
        "labs/01-terraform-lifecycle/terraform.tfstate",
        "labs/03-kubernetes-platform/kind/kubeconfig",
        "website/.venv/bin/python",
        "website/site/index.html",
        ".venv/bin/python",
        "labs/03-kubernetes-platform/evidence/run.json",
    ):
        proc = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "check-ignore", "-q", candidate],
            capture_output=True,
        )
        assert proc.returncode == 0, f"{candidate} must be git-ignored"


def test_website_navigation_targets_exist() -> None:
    config = load_yaml(REPO_ROOT / "website" / "mkdocs.yml")
    docs_dir = REPO_ROOT / "website" / (config.get("docs_dir") or "docs")

    def walk(nav):
        for item in nav:
            if isinstance(item, dict):
                for value in item.values():
                    yield from walk(value if isinstance(value, list) else [value])
            else:
                yield item

    missing = []
    for target in walk(config["nav"]):
        if isinstance(target, str) and target.endswith(".md") and not (docs_dir / target).is_file():
            missing.append(target)
    assert not missing, f"navigation entries without file: {missing}"
