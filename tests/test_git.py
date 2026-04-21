from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from doneproof.git import git_diff_summary


def test_git_diff_summary_reports_clean_repo(tmp_path: Path) -> None:
    _init_repo(tmp_path)

    summary = git_diff_summary(tmp_path)

    assert "No changed files detected." in summary
    assert "Full diff content is intentionally omitted." in summary


def test_git_diff_summary_reports_dirty_repo_without_diff_content(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    tmp_path.joinpath("README.md").write_text("# Example\n\nChanged\n", encoding="utf-8")
    tmp_path.joinpath("notes.md").write_text("new note\n", encoding="utf-8")

    summary = git_diff_summary(tmp_path)

    assert "unstaged\t2\t0\tREADME.md" in summary
    assert "untracked\t-\t-\tnotes.md" in summary
    assert "Changed" not in summary
    assert "new note" not in summary


def test_git_diff_summary_filters_paths(tmp_path: Path) -> None:
    _init_repo(tmp_path, files={"README.md": "# Example\n", "docs/guide.md": "# Guide\n"})
    tmp_path.joinpath("README.md").write_text("# Example\n\nChanged\n", encoding="utf-8")
    tmp_path.joinpath("docs", "guide.md").write_text("# Guide\n\nChanged\n", encoding="utf-8")

    summary = git_diff_summary(tmp_path, paths=["docs"])

    assert "docs/guide.md" in summary
    assert "README.md" not in summary


def test_git_diff_summary_supports_staged_mode(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    tmp_path.joinpath("README.md").write_text("# Example\n\nStaged\n", encoding="utf-8")
    tmp_path.joinpath("notes.md").write_text("new note\n", encoding="utf-8")
    _run(tmp_path, "git", "add", "README.md")

    summary = git_diff_summary(tmp_path, mode="staged")

    assert "mode: staged" in summary
    assert "staged\t2\t0\tREADME.md" in summary
    assert "notes.md" not in summary


def test_git_diff_summary_supports_untracked_mode(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    tmp_path.joinpath("README.md").write_text("# Example\n\nChanged\n", encoding="utf-8")
    tmp_path.joinpath("notes.md").write_text("new note\n", encoding="utf-8")

    summary = git_diff_summary(tmp_path, mode="untracked")

    assert "mode: untracked" in summary
    assert "untracked\t-\t-\tnotes.md" in summary
    assert "README.md" not in summary


def test_git_diff_summary_skips_secret_like_files(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    tmp_path.joinpath(".env").write_text("VALUE=redacted\n", encoding="utf-8")
    tmp_path.joinpath("safe.txt").write_text("safe\n", encoding="utf-8")

    summary = git_diff_summary(tmp_path)

    assert ".env" not in summary
    assert "VALUE" not in summary
    assert "safe.txt" in summary


def test_git_diff_summary_rejects_unsafe_path_filter(tmp_path: Path) -> None:
    _init_repo(tmp_path)

    with pytest.raises(ValueError, match="repo-relative and safe"):
        git_diff_summary(tmp_path, paths=["../outside"])


def _init_repo(tmp_path: Path, files: dict[str, str] | None = None) -> None:
    _run(tmp_path, "git", "init", "-b", "main")
    _run(tmp_path, "git", "config", "user.name", "DoneProof Test")
    _run(tmp_path, "git", "config", "user.email", "doneproof.local")
    for raw_path, content in (files or {"README.md": "# Example\n"}).items():
        path = tmp_path / raw_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    _run(tmp_path, "git", "add", ".")
    _run(tmp_path, "git", "commit", "-m", "initial")


def _run(cwd: Path, *command: str) -> None:
    subprocess.run(command, cwd=cwd, check=True, capture_output=True, text=True)
