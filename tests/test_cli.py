from __future__ import annotations

import json
from pathlib import Path

import pytest

from doneproof.cli import main
from doneproof.receipt import load_receipt

ROOT = Path(__file__).resolve().parents[1]


def test_cli_check_passes() -> None:
    code = main(
        [
            "check",
            "--root",
            str(ROOT),
            "--receipt",
            str(ROOT / "examples" / "receipts" / "passing.json"),
        ]
    )

    assert code == 0


def test_cli_version_passes() -> None:
    with pytest.raises(SystemExit) as exc:
        main(["--version"])

    assert exc.value.code == 0


def test_cli_check_fails() -> None:
    code = main(
        [
            "check",
            "--root",
            str(ROOT),
            "--receipt",
            str(ROOT / "examples" / "receipts" / "failing.json"),
        ]
    )

    assert code == 1


def test_cli_report_json_outputs_structured_report(capsys: pytest.CaptureFixture[str]) -> None:
    code = main(
        [
            "report",
            "--root",
            str(ROOT),
            "--receipt",
            str(ROOT / "examples" / "receipts" / "passing.json"),
            "--format",
            "json",
        ]
    )

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["schema_version"] == "1.0"
    assert payload["ok"] is True
    assert payload["receipt"] == "examples/receipts/passing.json"
    assert payload["status"] == "awaiting_review"
    assert payload["changed_files"] == ["README.md"]
    assert payload["errors"] == []


def test_cli_badge_outputs_markdown(capsys: pytest.CaptureFixture[str]) -> None:
    code = main(
        [
            "badge",
            "--root",
            str(ROOT),
            "--receipt",
            str(ROOT / "examples" / "receipts" / "passing.json"),
            "--format",
            "markdown",
        ]
    )

    assert code == 0
    output = capsys.readouterr().out.strip()
    assert output.startswith("![DoneProof:")
    assert "img.shields.io/badge" in output
    assert "awaiting_review" in output


def test_cli_badge_handles_blocked_receipt(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(["init", "--root", str(tmp_path)]) == 0
    tmp_path.joinpath("README.md").write_text("# Example\n", encoding="utf-8")
    receipt_path = tmp_path / ".doneproof" / "receipts" / "blocked.json"
    receipt_path.write_text(
        json.dumps(
            {
                "task": "Blocked task",
                "status": "blocked",
                "summary": "Waiting on an external review before proceeding.",
                "changed_files": ["README.md"],
                "commands": [{"cmd": "python3 -m pytest", "status": "passed"}],
                "evidence": [{"type": "test", "value": "python3 -m pytest passed"}],
                "risks": ["External dependency is not resolved."],
            }
        ),
        encoding="utf-8",
    )
    capsys.readouterr()

    code = main(
        ["badge", "--root", str(tmp_path), "--receipt", str(receipt_path), "--format", "json"]
    )

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["schema_version"] == "1.0"
    assert payload["state"] == "blocked"
    assert payload["risks"] == 1
    assert payload["color"] == "orange"


def test_cli_badge_json_reports_invalid_receipt(capsys: pytest.CaptureFixture[str]) -> None:
    code = main(
        [
            "badge",
            "--root",
            str(ROOT),
            "--receipt",
            str(ROOT / "examples" / "receipts" / "failing.json"),
            "--format",
            "json",
        ]
    )

    assert code == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["schema_version"] == "1.0"
    assert payload["ok"] is False
    assert payload["state"] == "failed"
    assert payload["errors"] > 0


def test_cli_comment_outputs_expected_shape(tmp_path: Path) -> None:
    badge = (
        "![DoneProof: awaiting_review | no risks listed]"
        "(https://img.shields.io/badge/DoneProof-awaiting_review%20%7C%20no%20risks%20listed-brightgreen)"
    )
    report = {
        "schema_version": "1.0",
        "ok": True,
    }
    tmp_path.joinpath("doneproof-badge.md").write_text(f"{badge}\n", encoding="utf-8")
    tmp_path.joinpath("doneproof-report.json").write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    code = main(
        [
            "comment",
            "--root",
            str(tmp_path),
            "--badge-file",
            "doneproof-badge.md",
            "--report-file",
            "doneproof-report.json",
            "--output",
            "doneproof-comment.md",
        ]
    )

    assert code == 0
    output = tmp_path.joinpath("doneproof-comment.md").read_text(encoding="utf-8")
    expected = ROOT.joinpath("docs", "examples", "github-pr-comment.expected.md").read_text(
        encoding="utf-8"
    )
    assert output == expected


def test_cli_comment_falls_back_when_artifacts_are_missing(tmp_path: Path) -> None:
    code = main(
        [
            "comment",
            "--root",
            str(tmp_path),
            "--badge-file",
            "missing-badge.md",
            "--report-file",
            "missing-report.json",
            "--output",
            "doneproof-comment.md",
        ]
    )

    assert code == 0
    output = tmp_path.joinpath("doneproof-comment.md").read_text(encoding="utf-8")
    assert "report_unavailable" in output
    assert "Missing report file: missing-report.json" in output


def test_cli_init_creates_files(tmp_path: Path) -> None:
    code = main(["init", "--root", str(tmp_path)])

    assert code == 0
    assert tmp_path.joinpath(".doneproof", "policy.yml").exists()
    assert tmp_path.joinpath(".doneproof", "templates", "opencode.md").exists()
    assert tmp_path.joinpath(".doneproof", "templates", "openclaw.md").exists()
    assert tmp_path.joinpath(".doneproof", "templates", "hermes.md").exists()


def test_cli_doctor_passes_after_init(tmp_path: Path) -> None:
    assert main(["init", "--root", str(tmp_path)]) == 0

    code = main(["doctor", "--root", str(tmp_path)])

    assert code == 0


def test_cli_doctor_requires_all_templates(tmp_path: Path) -> None:
    assert main(["init", "--root", str(tmp_path)]) == 0
    tmp_path.joinpath(".doneproof", "templates", "hermes.md").unlink()

    code = main(["doctor", "--root", str(tmp_path)])

    assert code == 1


def test_cli_doctor_fails_on_invalid_policy_yaml(tmp_path: Path) -> None:
    assert main(["init", "--root", str(tmp_path)]) == 0
    tmp_path.joinpath(".doneproof", "policy.yml").write_text("- bad\n", encoding="utf-8")

    code = main(["doctor", "--root", str(tmp_path)])

    assert code == 1


def test_cli_new_creates_default_receipt(tmp_path: Path) -> None:
    assert main(["init", "--root", str(tmp_path)]) == 0
    tmp_path.joinpath("README.md").write_text("# Example\n", encoding="utf-8")

    code = main(
        [
            "new",
            "--root",
            str(tmp_path),
            "--task",
            "Write README",
            "--changed-file",
            "README.md",
            "--command",
            "passed:python3 -m pytest",
            "--evidence",
            "test:pytest passed",
            "--risk",
            "Example risk",
        ]
    )

    assert code == 0
    receipt_path = tmp_path / ".doneproof" / "receipts" / "latest.json"
    receipt = load_receipt(receipt_path)
    assert receipt["task"] == "Write README"
    assert receipt["commands"][0]["status"] == "passed"
    assert receipt["evidence"][0]["type"] == "test"
    assert main(["check", "--root", str(tmp_path)]) == 0


def test_cli_evidence_git_diff_writes_summary(tmp_path: Path) -> None:
    assert main(["init", "--root", str(tmp_path)]) == 0
    _run(tmp_path, "git", "init", "-b", "main")
    _run(tmp_path, "git", "config", "user.name", "DoneProof Test")
    _run(tmp_path, "git", "config", "user.email", "doneproof.local")
    tmp_path.joinpath("README.md").write_text("# Example\n", encoding="utf-8")
    _run(tmp_path, "git", "add", "README.md")
    _run(tmp_path, "git", "commit", "-m", "initial")
    tmp_path.joinpath("README.md").write_text("# Example\n\nChanged\n", encoding="utf-8")

    code = main(["evidence", "git-diff", "--root", str(tmp_path), "--mode", "unstaged"])

    assert code == 0
    summary_path = tmp_path / ".doneproof" / "evidence" / "git-diff-summary.txt"
    summary = summary_path.read_text(encoding="utf-8")
    assert "mode: unstaged" in summary
    assert "README.md" in summary
    assert "Changed" not in summary


def test_cli_evidence_git_diff_rejects_unsafe_path_filter(tmp_path: Path) -> None:
    assert main(["init", "--root", str(tmp_path)]) == 0

    code = main(["evidence", "git-diff", "--root", str(tmp_path), "--path", "../secret"])

    assert code == 1


def _run(cwd: Path, *command: str) -> None:
    import subprocess

    subprocess.run(command, cwd=cwd, check=True, capture_output=True, text=True)
