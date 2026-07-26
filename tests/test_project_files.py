from __future__ import annotations

import json
import re
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def test_json_schema_loads() -> None:
    schema_path = ROOT / "schemas" / "receipt.schema.json"

    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    Draft202012Validator.check_schema(schema)
    assert schema["title"] == "DoneProof Receipt"
    assert schema["$id"] == "urn:doneproof:schema:receipt:1.0"
    assert "task" in schema["required"]


def test_packaged_schema_matches_public_schema() -> None:
    public_schema = (ROOT / "schemas" / "receipt.schema.json").read_text(encoding="utf-8")
    packaged_schema = (
        ROOT / "src" / "doneproof" / "schemas" / "receipt.schema.json"
    ).read_text(encoding="utf-8")

    assert packaged_schema == public_schema


def test_github_yaml_files_parse() -> None:
    yaml_paths = [
        ROOT / "action.yml",
        ROOT / ".github" / "dependabot.yml",
        ROOT / "docs" / "examples" / "github-pr-comment.yml",
        ROOT / ".github" / "ISSUE_TEMPLATE" / "config.yml",
    ]
    yaml_paths.extend(sorted(ROOT.joinpath(".github", "ISSUE_TEMPLATE").glob("*.yml")))
    yaml_paths.extend(sorted(ROOT.joinpath(".github", "workflows").glob("*.yml")))
    yaml_paths.extend(sorted(ROOT.joinpath("examples", "policies").glob("*.yml")))

    for path in yaml_paths:
        assert yaml.safe_load(path.read_text(encoding="utf-8")), path


def test_editor_task_examples_load() -> None:
    tasks_path = ROOT / "docs" / "examples" / "vscode-tasks.json"

    tasks = json.loads(tasks_path.read_text(encoding="utf-8"))

    labels = {task["label"] for task in tasks["tasks"]}
    assert "DoneProof: check receipt" in labels
    assert "DoneProof: report receipt" in labels
    assert "DoneProof: create receipt draft" in labels


def test_supply_chain_files_exist() -> None:
    assert (ROOT / "uv.lock").exists()
    config_path = ROOT / ".github" / "dependabot.yml"
    assert config_path.exists()

    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    ecosystems = {update["package-ecosystem"] for update in config["updates"]}
    assert ecosystems == {"github-actions", "uv"}


def test_security_workflow_is_history_complete_and_supply_chain_pinned() -> None:
    workflow = ROOT.joinpath(".github", "workflows", "security.yml").read_text(encoding="utf-8")

    assert "actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0" in workflow
    assert 'GITLEAKS_VERSION: "8.30.1"' in workflow
    assert "551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb" in workflow
    assert "sha256sum --check --strict" in workflow
    assert "fetch-depth: 0" in workflow
    assert 'gitleaks-bin git --redact --no-banner --log-opts="--all"' in workflow


def test_external_actions_are_pinned_in_workflows_and_copyable_example() -> None:
    yaml_paths = sorted(ROOT.joinpath(".github", "workflows").glob("*.yml"))
    yaml_paths.append(ROOT / "docs" / "examples" / "github-pr-comment.yml")
    external_uses: list[tuple[Path, str]] = []
    for path in yaml_paths:
        content = path.read_text(encoding="utf-8")
        for action in re.findall(r"^\s*-?\s*uses:\s*([^\s#]+)", content, flags=re.MULTILINE):
            if not action.startswith("./"):
                external_uses.append((path, action))

    assert external_uses
    for path, action in external_uses:
        assert "@" in action, (path, action)
        reference = action.rsplit("@", 1)[1]
        assert re.fullmatch(r"[0-9a-f]{40}", reference), (path, action)


def test_public_files_do_not_contain_private_markers() -> None:
    def text(*codepoints: int) -> str:
        return "".join(chr(codepoint) for codepoint in codepoints)

    forbidden = [
        text(47, 85, 115, 101, 114, 115, 47, 118, 105, 115, 105, 116, 97, 110, 116, 101),
        text(67, 108, 97, 117, 100, 101, 45, 77, 105, 114, 114, 111, 114),
        text(77, 54, 48),
        "API_" + "KEY",
        "TO" + "KEN",
        "ghp" + "_",
        "sk" + "-",
        "BEGIN " + "PRIVATE KEY",
        "auth" + "_token",
        text(49, 50, 55, 46, 48, 46, 48, 46, 49, 58, 49, 56, 55, 56, 57),
        text(49, 50, 55, 46, 48, 46, 48, 46, 49, 58, 49, 56, 55, 57, 48),
        text(46, 111, 112, 101, 110, 99, 108, 97, 119, 47),
        text(46, 104, 101, 114, 109, 101, 115, 47),
    ]
    public_paths = [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and not (".doneproof" in path.parts and "receipts" in path.parts)
        and ".venv" not in path.parts
        and "venv" not in path.parts
        and ".ruff_cache" not in path.parts
        and ".pytest_cache" not in path.parts
        and "__pycache__" not in path.parts
        and not any(part.endswith(".egg-info") for part in path.parts)
        and "dist" not in path.parts
        and "build" not in path.parts
        and path.name not in {"ACTIVE_VERSION.json", "PROJECT_STATUS.md", "AGENTS.md"}
    ]

    hits: list[str] = []
    for path in public_paths:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for marker in forbidden:
            if marker in text:
                hits.append(f"{path.relative_to(ROOT)}: {marker}")

    assert hits == []


def test_release_readiness_docs_exist() -> None:
    required = [
        ROOT / "docs" / "FIELD_LESSONS.md",
        ROOT / "docs" / "VALUE_PROOF.md",
        ROOT / "docs" / "GITHUB_IMPORT_RUNBOOK.md",
        ROOT / "docs" / "LAUNCH_COPY.md",
        ROOT / "docs" / "PRE_GITHUB_AUDIT.md",
        ROOT / "docs" / "PUBLISHING_CHECKLIST.md",
        ROOT / "docs" / "PYPI_READINESS.md",
        ROOT / "docs" / "INTEGRATIONS.md",
        ROOT / "docs" / "EDITOR_TASKS.md",
        ROOT / "docs" / "POLICY_PRESETS.md",
        ROOT / "docs" / "CODE_QUALITY_REVIEW.md",
        ROOT / "docs" / "ADVERSARIAL_REVIEW.md",
        ROOT / "scripts" / "prepublish_check.sh",
        ROOT / "scripts" / "captured_proof_demo.py",
        ROOT / "scripts" / "render_demo_gif.py",
        ROOT / "docs" / "DEMO.md",
        ROOT / "docs" / "assets" / "doneproof-demo.gif",
        ROOT / "docs" / "assets" / "doneproof-demo-poster.png",
        ROOT / "docs" / "assets" / "doneproof-social-preview.png",
        ROOT / "docs" / "assets" / "doneproof-demo.svg",
    ]

    for path in required:
        assert path.exists(), path

    social_preview = ROOT / "docs" / "assets" / "doneproof-social-preview.png"
    with Image.open(social_preview) as image:
        assert image.size == (1280, 640)
    assert social_preview.stat().st_size < 1_000_000


def test_readme_explains_relevance() -> None:
    readme = ROOT.joinpath("README.md").read_text(encoding="utf-8")

    assert "Why It Exists" in readme
    assert "real multi-agent work" in readme
    assert "When It Helps" in readme


def test_readme_has_one_coherent_captured_proof_activation_path() -> None:
    readme = ROOT.joinpath("README.md").read_text(encoding="utf-8")

    assert "# Factbound Run" in readme
    assert "Review receipts for AI code changes." in readme
    assert "**The agent says it passed. Show the run.**" in readme
    assert (
        "**Captured Proof** turns the check you already run into a shareable **Review"
        in readme
    )
    assert (
        "seconds, locally, with no account, agent integration, policy file, or CI change."
        in readme
    )
    assert "**Review\nReceipt** tied to the current Git change" in readme
    assert "repository, Python package,\n> CLI, schema identifiers" in readme
    assert "It records locally observed execution evidence." in readme
    assert (
        'doneproof capture --task "Check this change" -- git diff --check'
        in readme
    )
    assert (
        "doneproof.git@038498b4ca41926150e4952a7f3eabf1c0f371f0"
        in readme
    )
    assert "doneproof report" in readme
    assert readme.index("## Create a Review Receipt") < readme.index(
        "## Manual Receipt Flow (v0.5.0)"
    )
    assert "## DoneProof System" not in readme
    assert "verify_agent_change.py" not in readme


def test_agent_integration_guides_exist() -> None:
    guides = [
        "CODEX.md",
        "CLAUDE.md",
        "CURSOR.md",
        "OPENCODE.md",
        "OPENCLAW.md",
        "HERMES.md",
        "AIDER.md",
        "CLINE.md",
    ]

    for guide in guides:
        assert ROOT.joinpath("docs", "integrations", guide).exists()
