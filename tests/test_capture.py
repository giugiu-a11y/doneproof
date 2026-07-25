from __future__ import annotations

import io
import json
import subprocess
import sys
from pathlib import Path

import pytest

from doneproof.capture import run_command
from doneproof.cli import main
from doneproof.git import git_scope_digest
from doneproof.policy import load_policy
from doneproof.receipt import (
    captured_proof_integrity,
    load_receipt,
    validate_receipt,
)


def test_capture_writes_valid_receipt_without_raw_output(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _init_doneproof_repo(tmp_path)
    _commit_script(tmp_path, "passing_check.py", "print('machine-check-ok')\n")
    tmp_path.joinpath("README.md").write_text("# Example\n\nCaptured\n", encoding="utf-8")

    code = main(
        [
            "capture",
            "--root",
            str(tmp_path),
            "--task",
            "Verify README",
            "--changed-file",
            "README.md",
            "--",
            sys.executable,
            "passing_check.py",
        ]
    )

    assert code == 0
    terminal = capsys.readouterr().out
    assert "machine-check-ok" in terminal
    assert "Captured Proof: PASS" in terminal
    receipt_path = tmp_path / ".doneproof" / "receipts" / "latest.json"
    receipt_text = receipt_path.read_text(encoding="utf-8")
    receipt = json.loads(receipt_text)
    proof = receipt["captured_proof"]
    assert "machine-check-ok" not in receipt_text
    assert receipt["status"] == "awaiting_review"
    assert receipt["changed_files"] == ["README.md"]
    assert proof["exit_code"] == 0
    assert proof["output"]["content_stored"] is False
    assert proof["git_scope"]["content_stored"] is False
    assert proof["git_scope"]["sha256"].startswith("sha256:")
    assert proof["integrity_sha256"] == captured_proof_integrity(proof)
    assert validate_receipt(
        receipt,
        load_policy(tmp_path),
        receipt_path,
        repo_root=tmp_path,
    ).ok


def test_capture_preserves_failure_exit_code_and_receipt(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _init_doneproof_repo(tmp_path)
    tmp_path.joinpath("README.md").write_text("# Example\n\nBroken\n", encoding="utf-8")

    code = main(
        [
            "capture",
            "--root",
            str(tmp_path),
            "--task",
            "Run failing check",
            "--changed-file",
            "README.md",
            "--",
            sys.executable,
            "-c",
            "raise SystemExit(7)",
        ]
    )

    assert code == 7
    assert "Captured Proof: FAIL" in capsys.readouterr().out
    receipt_path = tmp_path / ".doneproof" / "receipts" / "latest.json"
    receipt = load_receipt(receipt_path)
    assert receipt["status"] == "failed"
    assert receipt["captured_proof"]["exit_code"] == 7
    assert receipt["captured_proof"]["result"] == "failed"
    assert validate_receipt(
        receipt,
        load_policy(tmp_path),
        receipt_path,
        repo_root=tmp_path,
    ).ok


def test_capture_redacts_output_and_command_before_hashing_or_persisting(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _init_doneproof_repo(tmp_path)
    _commit_script(
        tmp_path,
        "redaction_check.py",
        (
            "import sys\n"
            "value = sys.argv[1].split('=', 1)[1]\n"
            "print(f'password={value}')\n"
        ),
    )
    tmp_path.joinpath("README.md").write_text("# Example\n\nSafe\n", encoding="utf-8")
    secret = "super-private-value"

    code = main(
        [
            "capture",
            "--root",
            str(tmp_path),
            "--task",
            "Verify redaction",
            "--changed-file",
            "README.md",
            "--",
            sys.executable,
            "redaction_check.py",
            f"--password={secret}",
        ]
    )

    assert code == 0
    terminal = capsys.readouterr().out
    receipt_path = tmp_path / ".doneproof" / "receipts" / "latest.json"
    receipt_text = receipt_path.read_text(encoding="utf-8")
    receipt = json.loads(receipt_text)
    assert secret not in terminal
    assert secret not in receipt_text
    assert "[REDACTED]" in terminal
    assert "[REDACTED]" in receipt["captured_proof"]["command"]
    assert "[LOCAL_PATH]" in receipt["captured_proof"]["command"]
    assert receipt["captured_proof"]["output"]["redactions"] == 1
    assert receipt["captured_proof"]["command_redactions"] >= 1


def test_capture_refuses_private_file_before_running_command(tmp_path: Path) -> None:
    _init_doneproof_repo(tmp_path)
    tmp_path.joinpath(".env").write_text("VALUE=private\n", encoding="utf-8")
    marker = tmp_path / "command-ran.txt"

    code = main(
        [
            "capture",
            "--root",
            str(tmp_path),
            "--task",
            "Must not run",
            "--changed-file",
            ".env",
            "--",
            sys.executable,
            "-c",
            f"from pathlib import Path; Path({str(marker)!r}).write_text('ran')",
        ]
    )

    assert code == 2
    assert not marker.exists()
    assert not tmp_path.joinpath(".doneproof", "receipts", "latest.json").exists()


def test_capture_refuses_clean_repo_before_running_command(tmp_path: Path) -> None:
    _init_doneproof_repo(tmp_path)
    marker = tmp_path / "command-ran.txt"

    code = main(
        [
            "capture",
            "--root",
            str(tmp_path),
            "--task",
            "Must not run without a changed scope",
            "--",
            sys.executable,
            "-c",
            f"from pathlib import Path; Path({str(marker)!r}).write_text('ran')",
        ]
    )

    assert code == 2
    assert not marker.exists()
    assert not tmp_path.joinpath(".doneproof", "receipts", "latest.json").exists()


def test_capture_redacts_windows_home_path_before_display_or_persistence(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _init_doneproof_repo(tmp_path)
    tmp_path.joinpath("README.md").write_text("# Example\n\nSafe\n", encoding="utf-8")
    local_path = r"C:\Users\alice\private-project\receipt.txt"

    code = main(
        [
            "capture",
            "--root",
            str(tmp_path),
            "--task",
            "Verify cross-platform path redaction",
            "--changed-file",
            "README.md",
            "--",
            sys.executable,
            "-c",
            f"print({local_path!r})",
        ]
    )

    assert code == 0
    terminal = capsys.readouterr().out
    receipt_text = tmp_path.joinpath(
        ".doneproof", "receipts", "latest.json"
    ).read_text(encoding="utf-8")
    assert local_path not in terminal
    assert local_path not in receipt_text
    assert "[LOCAL_PATH]" in terminal
    assert "[LOCAL_PATH]" in receipt_text


def test_capture_digest_matches_only_the_public_changed_files(tmp_path: Path) -> None:
    _init_doneproof_repo(tmp_path)
    _commit_script(tmp_path, "secrets.txt", "private baseline\n")
    tmp_path.joinpath("README.md").write_text("# Example\n\nPublic change\n", encoding="utf-8")
    tmp_path.joinpath("secrets.txt").write_text("private changed value\n", encoding="utf-8")

    code = main(
        [
            "capture",
            "--root",
            str(tmp_path),
            "--task",
            "Verify public scope",
            "--",
            sys.executable,
            "-c",
            "print('ok')",
        ]
    )

    assert code == 0
    receipt = load_receipt(tmp_path / ".doneproof" / "receipts" / "latest.json")
    assert receipt["changed_files"] == ["README.md"]
    assert receipt["captured_proof"]["git_scope"]["sha256"] == git_scope_digest(
        tmp_path,
        paths=["README.md"],
    )


def test_captured_proof_detects_tampering_and_cross_field_mismatch(tmp_path: Path) -> None:
    _init_doneproof_repo(tmp_path)
    tmp_path.joinpath("README.md").write_text("# Example\n\nChanged\n", encoding="utf-8")
    assert (
        main(
            [
                "capture",
                "--root",
                str(tmp_path),
                "--task",
                "Verify integrity",
                "--changed-file",
                "README.md",
                "--",
                sys.executable,
                "-c",
                "print('ok')",
            ]
        )
        == 0
    )
    receipt_path = tmp_path / ".doneproof" / "receipts" / "latest.json"
    receipt = load_receipt(receipt_path)

    receipt["captured_proof"]["duration_ms"] += 1
    tampered = validate_receipt(
        receipt,
        load_policy(tmp_path),
        receipt_path,
        repo_root=tmp_path,
    )
    assert "captured_proof integrity check failed" in [
        finding.message for finding in tampered.errors()
    ]

    receipt["captured_proof"]["integrity_sha256"] = captured_proof_integrity(
        receipt["captured_proof"]
    )
    mismatched = validate_receipt(
        receipt,
        load_policy(tmp_path),
        receipt_path,
        repo_root=tmp_path,
    )
    assert "captured command duration does not match proof" in [
        finding.message for finding in mismatched.errors()
    ]


def test_run_command_returns_timeout_and_missing_executable_codes(tmp_path: Path) -> None:
    timeout_output = io.StringIO()
    timed_out = run_command(
        [sys.executable, "-c", "import time; time.sleep(1)"],
        root=tmp_path,
        timeout_seconds=0.05,
        output=timeout_output,
    )
    missing_output = io.StringIO()
    missing = run_command(
        ["doneproof-command-that-does-not-exist"],
        root=tmp_path,
        timeout_seconds=1,
        output=missing_output,
    )

    assert timed_out.exit_code == 124
    assert timed_out.timed_out is True
    assert missing.exit_code == 127
    assert missing.timed_out is False
    assert "executable not found" in missing_output.getvalue()


def _init_doneproof_repo(root: Path) -> None:
    assert main(["init", "--root", str(root)]) == 0
    _run(root, "git", "init", "-b", "main")
    _run(root, "git", "config", "user.name", "DoneProof Test")
    _run(root, "git", "config", "user.email", "doneproof.local")
    root.joinpath("README.md").write_text("# Example\n", encoding="utf-8")
    _run(root, "git", "add", ".")
    _run(root, "git", "commit", "-m", "initial")


def _commit_script(root: Path, name: str, content: str) -> None:
    root.joinpath(name).write_text(content, encoding="utf-8")
    _run(root, "git", "add", name)
    _run(root, "git", "commit", "-m", f"add {name}")


def _run(cwd: Path, *command: str) -> None:
    subprocess.run(command, cwd=cwd, check=True, capture_output=True, text=True)
