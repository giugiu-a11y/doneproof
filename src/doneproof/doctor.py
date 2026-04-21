"""Project setup checks for DoneProof."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .defaults import TEMPLATES
from .policy import load_policy, policy_path, templates_dir


@dataclass
class DoctorResult:
    ok: bool
    checks: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def run_doctor(root: Path) -> DoctorResult:
    checks: list[str] = []
    errors: list[str] = []
    warnings: list[str] = []

    if policy_path(root).exists():
        try:
            load_policy(root)
        except ValueError as exc:
            errors.append(str(exc))
        else:
            checks.append("policy exists")
    else:
        errors.append("missing .doneproof/policy.yml; run doneproof init")

    expected_templates = sorted(TEMPLATES)
    missing_templates = [
        name for name in expected_templates if not templates_dir(root).joinpath(name).exists()
    ]
    if missing_templates:
        errors.append(f"missing templates: {', '.join(missing_templates)}")
    else:
        checks.append("agent templates exist")

    if root.joinpath(".git").exists():
        checks.append("git repository detected")
    else:
        warnings.append("git repository not detected; changed file discovery will be limited")

    if root.joinpath("README.md").exists():
        checks.append("README exists")
    else:
        warnings.append("README.md not found")

    return DoctorResult(ok=not errors, checks=checks, errors=errors, warnings=warnings)
