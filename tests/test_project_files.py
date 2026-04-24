from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_json_schema_loads() -> None:
    schema_path = ROOT / "schemas" / "receipt.schema.json"

    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    assert schema["title"] == "DoneProof Receipt"
    assert "task" in schema["required"]


def test_github_yaml_files_parse() -> None:
    yaml_paths = [
        ROOT / "action.yml",
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
    assert (ROOT / "renovate.json5").exists()
    assert json.loads(ROOT.joinpath("renovate.json5").read_text(encoding="utf-8"))["extends"]


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
        ROOT / "scripts" / "render_demo_gif.py",
        ROOT / "docs" / "assets" / "doneproof-demo.gif",
        ROOT / "docs" / "assets" / "doneproof-demo.svg",
    ]

    for path in required:
        assert path.exists(), path


def test_readme_explains_relevance() -> None:
    readme = ROOT.joinpath("README.md").read_text(encoding="utf-8")

    assert "Why It Exists" in readme
    assert "real multi-agent work" in readme
    assert "When It Helps" in readme


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
