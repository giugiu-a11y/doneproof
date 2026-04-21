"""Receipt validation."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class Finding:
    level: str
    message: str


@dataclass
class ValidationResult:
    ok: bool
    receipt_path: Path
    findings: list[Finding] = field(default_factory=list)

    def errors(self) -> list[Finding]:
        return [finding for finding in self.findings if finding.level == "error"]

    def warnings(self) -> list[Finding]:
        return [finding for finding in self.findings if finding.level == "warning"]


def load_receipt(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"Receipt not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Receipt is not valid JSON: {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"Receipt must be a JSON object: {path}")
    return payload


def write_receipt(path: Path, receipt: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def build_receipt(
    *,
    task: str,
    status: str,
    summary: str,
    changed_files: list[str],
    commands: list[dict[str, str]],
    evidence: list[dict[str, str]],
    risks: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "task": task,
        "status": status,
        "summary": summary,
        "changed_files": changed_files,
        "commands": commands,
        "evidence": evidence,
        "risks": risks,
    }


def validate_receipt(
    receipt: dict[str, Any],
    policy: dict[str, Any],
    receipt_path: Path,
    repo_root: Path | None = None,
) -> ValidationResult:
    findings: list[Finding] = []
    required_fields = policy.get("required_fields", [])
    if not isinstance(required_fields, list):
        findings.append(Finding("error", "Policy required_fields must be a list"))
        required_fields = []

    for field_name in required_fields:
        if field_name not in receipt:
            findings.append(Finding("error", f"Missing required field: {field_name}"))

    _validate_required_text(receipt, findings)

    status = str(receipt.get("status", "")).strip().lower()
    status_policy = policy.get("status", {})
    allowed: set[str] = set()
    forbidden: set[str] = set()
    if not isinstance(status_policy, dict):
        findings.append(Finding("error", "Policy status must be an object"))
    else:
        allowed_items = status_policy.get("allowed", [])
        forbidden_items = status_policy.get("forbidden", [])
        if not isinstance(allowed_items, list):
            findings.append(Finding("error", "Policy status.allowed must be a list"))
        else:
            allowed = {str(item).lower() for item in allowed_items}
        if not isinstance(forbidden_items, list):
            findings.append(Finding("error", "Policy status.forbidden must be a list"))
        else:
            forbidden = {str(item).lower() for item in forbidden_items}
    if not status:
        findings.append(Finding("error", "Missing status"))
    elif status in forbidden:
        findings.append(Finding("error", f"Forbidden status: {receipt.get('status')}"))
    elif allowed and status not in allowed:
        findings.append(Finding("error", f"Status must be one of: {', '.join(sorted(allowed))}"))

    minimums = policy.get("minimums", {})
    if not isinstance(minimums, dict):
        findings.append(Finding("error", "Policy minimums must be an object"))
    else:
        _validate_minimums(receipt, minimums, findings)

    _validate_commands(receipt.get("commands", []), findings)
    _validate_evidence(receipt.get("evidence", []), findings)
    _validate_risks(receipt.get("risks", []), findings)
    _validate_changed_files(
        receipt.get("changed_files", []),
        receipt_path.parent,
        findings,
        repo_root=repo_root,
    )
    _validate_forbidden_claims(receipt, policy, findings)

    return ValidationResult(
        ok=not any(item.level == "error" for item in findings),
        receipt_path=receipt_path,
        findings=findings,
    )


def _validate_required_text(receipt: dict[str, Any], findings: list[Finding]) -> None:
    for field_name in ["task", "summary"]:
        if field_name in receipt and not str(receipt.get(field_name, "")).strip():
            findings.append(Finding("error", f"{field_name} must not be empty"))


def _validate_minimums(
    receipt: dict[str, Any],
    minimums: dict[str, Any],
    findings: list[Finding],
) -> None:
    for field_name, minimum in minimums.items():
        try:
            required_count = int(minimum)
        except (TypeError, ValueError):
            findings.append(Finding("error", f"Policy minimum for {field_name} must be an integer"))
            continue
        if required_count < 0:
            findings.append(Finding("error", f"Policy minimum for {field_name} must be >= 0"))
            continue
        value = receipt.get(field_name, [])
        if not isinstance(value, list):
            findings.append(Finding("error", f"{field_name} must be a list"))
            continue
        if len(value) < required_count:
            findings.append(
                Finding("error", f"{field_name} needs at least {required_count} item(s)")
            )


def _validate_commands(commands: Any, findings: list[Finding]) -> None:
    if not isinstance(commands, list):
        return
    for index, command in enumerate(commands, start=1):
        if not isinstance(command, dict):
            findings.append(Finding("error", f"commands[{index}] must be an object"))
            continue
        if not str(command.get("cmd", "")).strip():
            findings.append(Finding("error", f"commands[{index}] is missing cmd"))
        status = str(command.get("status", "")).strip().lower()
        if status not in {"passed", "failed", "skipped"}:
            findings.append(
                Finding("error", f"commands[{index}] status must be passed, failed, or skipped")
            )
        if status == "skipped" and not str(command.get("reason", "")).strip():
            findings.append(Finding("warning", f"commands[{index}] was skipped without a reason"))


def _validate_evidence(evidence_items: Any, findings: list[Finding]) -> None:
    if not isinstance(evidence_items, list):
        return
    for index, evidence in enumerate(evidence_items, start=1):
        if not isinstance(evidence, dict):
            findings.append(Finding("error", f"evidence[{index}] must be an object"))
            continue
        if not str(evidence.get("type", "")).strip():
            findings.append(Finding("error", f"evidence[{index}] is missing type"))
        if not str(evidence.get("value", "")).strip():
            findings.append(Finding("error", f"evidence[{index}] is missing value"))


def _validate_risks(risks: Any, findings: list[Finding]) -> None:
    if not isinstance(risks, list):
        return
    for index, risk in enumerate(risks, start=1):
        if not isinstance(risk, str):
            findings.append(Finding("error", f"risks[{index}] must be a string"))


def _validate_changed_files(
    changed_files: Any,
    receipt_base: Path,
    findings: list[Finding],
    repo_root: Path | None = None,
) -> None:
    if not isinstance(changed_files, list):
        return
    # Receipts often live in .doneproof/receipts; walk up to the likely repo root.
    resolved_root = repo_root or receipt_base
    if repo_root is None:
        if receipt_base.name == "receipts" and receipt_base.parent.name == ".doneproof":
            resolved_root = receipt_base.parent.parent
        for parent in [receipt_base, *receipt_base.parents]:
            if parent.name == ".doneproof":
                resolved_root = parent.parent
                break
            has_marker = (
                (parent / ".git").exists()
                or (parent / "pyproject.toml").exists()
                or (parent / "package.json").exists()
            )
            if has_marker:
                resolved_root = parent
                break
    for item in changed_files:
        path = str(item).strip()
        if not path:
            findings.append(Finding("error", "changed_files contains an empty path"))
            continue
        if path.startswith(("~", "/", "\\")) or "\\" in path or ".." in Path(path).parts:
            findings.append(
                Finding("error", f"changed_files path must be repo-relative and safe: {path}")
            )
            continue
        if not (resolved_root / path).exists():
            findings.append(Finding("warning", f"changed file does not exist locally: {path}"))


def _validate_forbidden_claims(
    receipt: dict[str, Any],
    policy: dict[str, Any],
    findings: list[Finding],
) -> None:
    claims_policy = policy.get("claims", {})
    if not isinstance(claims_policy, dict):
        findings.append(Finding("error", "Policy claims must be an object"))
        return
    forbidden = claims_policy.get("forbidden_phrases", [])
    if not isinstance(forbidden, list):
        findings.append(Finding("error", "Policy claims.forbidden_phrases must be a list"))
        return
    searchable_fields = [
        str(receipt.get("status", "")),
        str(receipt.get("summary", "")),
        " ".join(_string_values(receipt.get("evidence", []))),
        " ".join(_string_values(receipt.get("risks", []))),
    ]
    text = "\n".join(searchable_fields).lower()
    for phrase in forbidden:
        phrase_text = str(phrase).lower()
        if phrase_text and _contains_forbidden_phrase(text, phrase_text):
            findings.append(Finding("error", f"Forbidden completion claim found: {phrase}"))


def _contains_forbidden_phrase(text: str, phrase: str) -> bool:
    if not any(char.isalnum() for char in phrase):
        return phrase in text
    if " " in phrase:
        return phrase in text
    pattern = rf"(?<![a-z0-9_]){re.escape(phrase)}(?![a-z0-9_])"
    return re.search(pattern, text) is not None


def _string_values(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        values: list[str] = []
        for item in value.values():
            values.extend(_string_values(item))
        return values
    if isinstance(value, list):
        values = []
        for item in value:
            values.extend(_string_values(item))
        return values
    return []
