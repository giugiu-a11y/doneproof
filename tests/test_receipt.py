from __future__ import annotations

from pathlib import Path

from doneproof.policy import init_project, load_policy
from doneproof.receipt import load_receipt, validate_receipt

ROOT = Path(__file__).resolve().parents[1]


def test_passing_receipt_passes() -> None:
    receipt_path = ROOT / "examples" / "receipts" / "passing.json"
    receipt = load_receipt(receipt_path)
    result = validate_receipt(receipt, load_policy(ROOT), receipt_path)

    assert result.ok
    assert result.errors() == []


def test_failing_receipt_fails() -> None:
    receipt_path = ROOT / "examples" / "receipts" / "failing.json"
    receipt = load_receipt(receipt_path)
    result = validate_receipt(receipt, load_policy(ROOT), receipt_path)

    assert not result.ok
    messages = [finding.message for finding in result.errors()]
    assert "Forbidden status: done" in messages
    assert "changed_files needs at least 1 item(s)" in messages
    assert "commands needs at least 1 item(s)" in messages
    assert "evidence needs at least 1 item(s)" in messages


def test_blank_summary_fails() -> None:
    receipt_path = ROOT / "examples" / "receipts" / "passing.json"
    receipt = load_receipt(receipt_path)
    receipt["summary"] = " "
    result = validate_receipt(receipt, load_policy(ROOT), receipt_path)

    assert not result.ok
    assert "summary must not be empty" in [finding.message for finding in result.errors()]


def test_product_name_does_not_trigger_done_claim() -> None:
    receipt_path = ROOT / "examples" / "receipts" / "passing.json"
    receipt = load_receipt(receipt_path)
    receipt["summary"] = "Ran doneproof against a receipt."
    result = validate_receipt(receipt, load_policy(ROOT), receipt_path)

    assert result.ok


def test_forbidden_claims_are_detected_inside_evidence_objects() -> None:
    receipt_path = ROOT / "examples" / "receipts" / "passing.json"
    receipt = load_receipt(receipt_path)
    receipt["evidence"] = [{"type": "note", "value": "This is fully validated."}]
    result = validate_receipt(receipt, load_policy(ROOT), receipt_path)

    assert not result.ok
    assert "Forbidden completion claim found: fully validated" in [
        finding.message for finding in result.errors()
    ]


def test_malformed_policy_reports_errors_instead_of_crashing() -> None:
    receipt_path = ROOT / "examples" / "receipts" / "passing.json"
    receipt = load_receipt(receipt_path)
    policy = {
        "required_fields": "task",
        "status": "bad",
        "minimums": {"changed_files": "many"},
        "claims": {"forbidden_phrases": "done"},
    }
    result = validate_receipt(receipt, policy, receipt_path)
    messages = [finding.message for finding in result.errors()]

    assert "Policy required_fields must be a list" in messages
    assert "Policy status must be an object" in messages
    assert "Policy minimum for changed_files must be an integer" in messages
    assert "Policy claims.forbidden_phrases must be a list" in messages


def test_evidence_object_requires_type_and_value() -> None:
    receipt_path = ROOT / "examples" / "receipts" / "passing.json"
    receipt = load_receipt(receipt_path)
    receipt["evidence"] = [{"type": "", "value": ""}]
    result = validate_receipt(receipt, load_policy(ROOT), receipt_path)
    messages = [finding.message for finding in result.errors()]

    assert "evidence[1] is missing type" in messages
    assert "evidence[1] is missing value" in messages


def test_windows_style_parent_path_is_rejected() -> None:
    receipt_path = ROOT / "examples" / "receipts" / "passing.json"
    receipt = load_receipt(receipt_path)
    receipt["changed_files"] = ["..\\secret.txt"]
    result = validate_receipt(receipt, load_policy(ROOT), receipt_path)

    assert not result.ok
    assert "changed_files path must be repo-relative and safe: ..\\secret.txt" in [
        finding.message for finding in result.errors()
    ]


def test_explicit_repo_root_is_used_for_external_receipt(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    receipt_dir = tmp_path / "external-receipts"
    repo_root.mkdir()
    receipt_dir.mkdir()
    repo_root.joinpath("README.md").write_text("# Example\n", encoding="utf-8")
    receipt = load_receipt(ROOT / "examples" / "receipts" / "passing.json")
    receipt["changed_files"] = ["README.md"]

    result = validate_receipt(
        receipt,
        load_policy(ROOT),
        receipt_dir / "latest.json",
        repo_root=repo_root,
    )

    assert result.ok
    assert result.warnings() == []


def test_receipt_under_doneproof_dir_uses_repo_root(tmp_path: Path) -> None:
    tmp_path.joinpath(".doneproof", "receipts").mkdir(parents=True)
    tmp_path.joinpath("README.md").write_text("# Example\n", encoding="utf-8")
    receipt_path = tmp_path / ".doneproof" / "receipts" / "latest.json"
    receipt = {
        "task": "Write README",
        "status": "awaiting_review",
        "summary": "Added README.",
        "changed_files": ["README.md"],
        "commands": [{"cmd": "echo ok", "status": "passed"}],
        "evidence": [{"type": "smoke", "value": "echo ok"}],
        "risks": [],
    }

    result = validate_receipt(receipt, load_policy(ROOT), receipt_path)

    assert result.ok
    assert result.warnings() == []


def test_init_project_creates_policy_and_templates(tmp_path: Path) -> None:
    created = init_project(tmp_path)

    assert tmp_path.joinpath(".doneproof", "policy.yml").exists()
    assert tmp_path.joinpath(".doneproof", "templates", "codex.md").exists()
    assert tmp_path.joinpath(".doneproof", "templates", "claude.md").exists()
    assert created
