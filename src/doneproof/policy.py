"""Policy loading and project initialization."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .defaults import DEFAULT_POLICY, TEMPLATES


def policy_dir(root: Path) -> Path:
    return root / ".doneproof"


def receipts_dir(root: Path) -> Path:
    return policy_dir(root) / "receipts"


def templates_dir(root: Path) -> Path:
    return policy_dir(root) / "templates"


def policy_path(root: Path) -> Path:
    return policy_dir(root) / "policy.yml"


def load_policy(root: Path) -> dict[str, Any]:
    path = policy_path(root)
    if not path.exists():
        return dict(DEFAULT_POLICY)
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError(f"Policy must be a YAML object: {path}")
    return loaded


def init_project(root: Path, overwrite: bool = False) -> list[Path]:
    created: list[Path] = []
    policy_dir(root).mkdir(parents=True, exist_ok=True)
    receipts_dir(root).mkdir(parents=True, exist_ok=True)
    templates_dir(root).mkdir(parents=True, exist_ok=True)

    receipt_keep = receipts_dir(root) / ".gitkeep"
    if overwrite or not receipt_keep.exists():
        receipt_keep.write_text("", encoding="utf-8")
        created.append(receipt_keep)

    target_policy = policy_path(root)
    if overwrite or not target_policy.exists():
        target_policy.write_text(
            yaml.safe_dump(DEFAULT_POLICY, sort_keys=False, allow_unicode=False),
            encoding="utf-8",
        )
        created.append(target_policy)

    for name, body in TEMPLATES.items():
        target = templates_dir(root) / name
        if overwrite or not target.exists():
            target.write_text(body, encoding="utf-8")
            created.append(target)

    return created

