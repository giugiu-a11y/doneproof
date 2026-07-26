"""Receipt validation."""

from __future__ import annotations

import hashlib
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
    commands: list[dict[str, Any]],
    evidence: list[dict[str, Any]],
    risks: list[str],
    captured_proof: dict[str, Any] | None = None,
) -> dict[str, Any]:
    receipt: dict[str, Any] = {
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
    if captured_proof is not None:
        receipt["captured_proof"] = captured_proof
    return receipt


def captured_proof_integrity(proof: dict[str, Any]) -> str:
    """Return a stable integrity digest for a captured-proof object."""

    canonical = {key: value for key, value in proof.items() if key != "integrity_sha256"}
    encoded = json.dumps(
        canonical,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


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
    _validate_captured_proof(receipt, findings)
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


def _validate_captured_proof(receipt: dict[str, Any], findings: list[Finding]) -> None:
    proof = receipt.get("captured_proof")
    if proof is None:
        return
    if not isinstance(proof, dict):
        findings.append(Finding("error", "captured_proof must be an object"))
        return

    required = {
        "version",
        "captured_at",
        "command",
        "result",
        "exit_code",
        "duration_ms",
        "timed_out",
        "output",
        "command_redactions",
        "git_scope",
        "environment",
        "integrity_sha256",
    }
    for field_name in sorted(required - set(proof)):
        findings.append(Finding("error", f"captured_proof is missing {field_name}"))
    if required - set(proof):
        return

    result = proof.get("result")
    exit_code = proof.get("exit_code")
    duration_ms = proof.get("duration_ms")
    if proof.get("version") != "1.0":
        findings.append(Finding("error", "captured_proof version must be 1.0"))
    try:
        captured_at = datetime.fromisoformat(str(proof.get("captured_at")).replace("Z", "+00:00"))
        if captured_at.tzinfo is None or captured_at.utcoffset() is None:
            raise ValueError
    except ValueError:
        findings.append(
            Finding("error", "captured_proof captured_at must be a timezone-aware timestamp")
        )
    if not str(proof.get("command", "")).strip():
        findings.append(Finding("error", "captured_proof command must not be empty"))
    if result not in {"passed", "failed"}:
        findings.append(Finding("error", "captured_proof result must be passed or failed"))
    if not isinstance(exit_code, int) or isinstance(exit_code, bool):
        findings.append(Finding("error", "captured_proof exit_code must be an integer"))
    elif result != ("passed" if exit_code == 0 else "failed"):
        findings.append(Finding("error", "captured_proof result does not match exit_code"))
    if not isinstance(duration_ms, int) or isinstance(duration_ms, bool) or duration_ms < 0:
        findings.append(Finding("error", "captured_proof duration_ms must be >= 0"))
    if not isinstance(proof.get("timed_out"), bool):
        findings.append(Finding("error", "captured_proof timed_out must be a boolean"))
    elif proof.get("timed_out") is True and exit_code != 124:
        findings.append(Finding("error", "captured_proof timed_out requires exit_code 124"))
    if (
        not isinstance(proof.get("command_redactions"), int)
        or isinstance(proof.get("command_redactions"), bool)
        or proof.get("command_redactions", -1) < 0
    ):
        findings.append(Finding("error", "captured_proof command_redactions must be >= 0"))

    _validate_captured_output(proof.get("output"), findings)
    _validate_git_scope(proof.get("git_scope"), receipt.get("changed_files"), findings)
    _validate_capture_environment(proof.get("environment"), findings)

    integrity = proof.get("integrity_sha256")
    if not _is_sha256(integrity):
        findings.append(Finding("error", "captured_proof integrity_sha256 is invalid"))
    elif integrity != captured_proof_integrity(proof):
        findings.append(Finding("error", "captured_proof integrity check failed"))

    captured_commands = [
        command
        for command in receipt.get("commands", [])
        if isinstance(command, dict) and command.get("captured") is True
    ]
    if len(captured_commands) != 1:
        findings.append(Finding("error", "captured_proof requires exactly one captured command"))
    elif isinstance(exit_code, int):
        command = captured_commands[0]
        if command.get("exit_code") != exit_code:
            findings.append(Finding("error", "captured command exit_code does not match proof"))
        if command.get("status") != result:
            findings.append(Finding("error", "captured command status does not match proof"))
        if command.get("cmd") != proof.get("command"):
            findings.append(Finding("error", "captured command text does not match proof"))
        if command.get("duration_ms") != duration_ms:
            findings.append(Finding("error", "captured command duration does not match proof"))
        output = proof.get("output")
        if isinstance(output, dict) and command.get("output_sha256") != output.get("sha256"):
            findings.append(Finding("error", "captured command output digest does not match proof"))

    expected_status = "awaiting_review" if result == "passed" else "failed"
    if receipt.get("status") != expected_status:
        findings.append(Finding("error", "receipt status does not match captured proof"))


def _validate_captured_output(output: Any, findings: list[Finding]) -> None:
    if not isinstance(output, dict):
        findings.append(Finding("error", "captured_proof output must be an object"))
        return
    if not _is_sha256(output.get("sha256")):
        findings.append(Finding("error", "captured_proof output sha256 is invalid"))
    for field_name in ("bytes", "lines", "redactions"):
        value = output.get(field_name)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            findings.append(Finding("error", f"captured_proof output {field_name} must be >= 0"))
    if output.get("content_stored") is not False:
        findings.append(Finding("error", "captured_proof must not store raw output content"))
    if output.get("redaction_status") not in {"not_detected", "known_patterns_masked"}:
        findings.append(Finding("error", "captured_proof redaction_status is invalid"))
    redactions = output.get("redactions")
    redaction_status = output.get("redaction_status")
    if isinstance(redactions, int) and not isinstance(redactions, bool):
        expected = "known_patterns_masked" if redactions else "not_detected"
        if redaction_status != expected:
            findings.append(
                Finding("error", "captured_proof redaction_status does not match redactions")
            )


def _validate_git_scope(
    git_scope: Any,
    receipt_files: Any,
    findings: list[Finding],
) -> None:
    if not isinstance(git_scope, dict):
        findings.append(Finding("error", "captured_proof git_scope must be an object"))
        return
    if git_scope.get("mode") not in {"all", "staged", "unstaged", "untracked"}:
        findings.append(Finding("error", "captured_proof git_scope mode is invalid"))
    if not _is_sha256(git_scope.get("sha256")):
        findings.append(Finding("error", "captured_proof git_scope sha256 is invalid"))
    if git_scope.get("content_stored") is not False:
        findings.append(Finding("error", "captured_proof must not store git diff content"))
    if git_scope.get("changed_files") != receipt_files:
        findings.append(Finding("error", "captured_proof git scope does not match changed_files"))


def _validate_capture_environment(environment: Any, findings: list[Finding]) -> None:
    if not isinstance(environment, dict):
        findings.append(Finding("error", "captured_proof environment must be an object"))
        return
    allowed = {"os", "architecture", "python"}
    extra = set(environment) - allowed
    if extra:
        findings.append(
            Finding(
                "error",
                f"captured_proof environment contains unsafe field(s): {', '.join(sorted(extra))}",
            )
        )
    for field_name in allowed:
        if not str(environment.get(field_name, "")).strip():
            findings.append(Finding("error", f"captured_proof environment is missing {field_name}"))


def _is_sha256(value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch(r"sha256:[0-9a-f]{64}", value) is not None


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
