"""Small git helpers used for receipt generation and evidence artifacts."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

DiffMode = Literal["all", "staged", "unstaged", "untracked"]


@dataclass(frozen=True)
class DiffSummaryEntry:
    section: str
    additions: str
    deletions: str
    path: str


def changed_files(root: Path) -> list[str]:
    """Return changed repo-relative files from git status.

    This intentionally avoids clever parsing. DoneProof should provide a useful
    starting point, not pretend it has perfect knowledge of the change.
    """

    try:
        result = subprocess.run(
            ["git", "-C", str(root), "status", "--short", "--untracked-files=all"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return []
    if result.returncode != 0:
        return []

    files: list[str] = []
    for raw_line in result.stdout.splitlines():
        path = _path_from_status_line(raw_line)
        if path and _is_public_candidate(path):
            files.append(path)
    return sorted(dict.fromkeys(files))


def git_diff_summary(root: Path, paths: list[str] | None = None, mode: DiffMode = "all") -> str:
    """Return a sanitized git diff summary.

    The summary intentionally uses `--numstat` and untracked file names only.
    Full diff content is not captured by default because receipts are review
    artifacts and can be copied into CI logs or public issue discussions.
    """

    filters = [_normalize_filter_path(path) for path in paths or []]
    _ensure_git_repo(root)
    if mode not in {"all", "staged", "unstaged", "untracked"}:
        raise ValueError(f"Unsupported git diff mode: {mode}")

    entries: list[DiffSummaryEntry] = []
    if mode in {"all", "staged"}:
        entries.extend(
            _numstat_entries(
                root,
                "staged",
                ["git", "-C", str(root), "diff", "--cached", "--numstat", "--relative", "--"],
                filters,
            )
        )
    if mode in {"all", "unstaged"}:
        entries.extend(
            _numstat_entries(
                root,
                "unstaged",
                ["git", "-C", str(root), "diff", "--numstat", "--relative", "--"],
                filters,
            )
        )
    if mode in {"all", "untracked"}:
        entries.extend(_untracked_entries(root, filters))

    return _render_diff_summary(entries, filters, mode)


def _path_from_status_line(line: str) -> str:
    if len(line) < 4:
        return ""
    path = line[3:].strip()
    if " -> " in path:
        path = path.rsplit(" -> ", 1)[1].strip()
    return path.strip('"')


def _is_public_candidate(path: str) -> bool:
    blocked_prefixes = (
        ".git/",
        ".pytest_cache/",
        ".ruff_cache/",
        "src/doneproof.egg-info/",
    )
    blocked_files = {
        "ACTIVE_VERSION.json",
        "PROJECT_STATUS.md",
        "AGENTS.md",
        ".doneproof/receipts/latest.json",
    }
    name = Path(path).name
    blocked_suffixes = (".pem", ".key", ".p12", ".pfx")
    secret_like = (
        name == ".env"
        or name.startswith(".env.")
        or name.endswith(blocked_suffixes)
        or "secret" in name.lower()
        or "token" in name.lower()
    )
    return not path.startswith(blocked_prefixes) and path not in blocked_files and not secret_like


def _ensure_git_repo(root: Path) -> None:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--is-inside-work-tree"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        raise ValueError("git executable is not available") from exc
    if result.returncode != 0 or result.stdout.strip() != "true":
        raise ValueError(f"Not a git repository: {root}")


def _normalize_filter_path(raw_path: str) -> str:
    path = raw_path.strip()
    while path.startswith("./"):
        path = path[2:]
    if not path:
        raise ValueError("Path filter must not be empty")
    path_obj = Path(path)
    if path_obj.is_absolute() or "\\" in path or ".." in path_obj.parts:
        raise ValueError(f"Path filter must be repo-relative and safe: {raw_path}")
    return path


def _numstat_entries(
    root: Path,
    section: str,
    base_command: list[str],
    filters: list[str],
) -> list[DiffSummaryEntry]:
    try:
        result = subprocess.run(
            [*base_command, *filters],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return []
    if result.returncode != 0:
        return []

    entries: list[DiffSummaryEntry] = []
    for line in result.stdout.splitlines():
        parts = line.split("\t", 2)
        if len(parts) != 3:
            continue
        additions, deletions, path = parts
        path = path.strip('"')
        if _is_public_candidate(path):
            entries.append(
                DiffSummaryEntry(
                    section=section,
                    additions=additions,
                    deletions=deletions,
                    path=path,
                )
            )
    return entries


def _untracked_entries(root: Path, filters: list[str]) -> list[DiffSummaryEntry]:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "ls-files", "--others", "--exclude-standard", "--", *filters],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return []
    if result.returncode != 0:
        return []

    entries = []
    for path in result.stdout.splitlines():
        if _is_public_candidate(path):
            entries.append(
                DiffSummaryEntry(
                    section="untracked",
                    additions="-",
                    deletions="-",
                    path=path,
                )
            )
    return entries


def _render_diff_summary(entries: list[DiffSummaryEntry], filters: list[str], mode: str) -> str:
    scope = ", ".join(filters) if filters else "all changed files"
    lines = [
        "# DoneProof git diff summary",
        "",
        "Full diff content is intentionally omitted.",
        "Reviewers should inspect the actual git diff before approval.",
        "",
        f"scope: {scope}",
        f"mode: {mode}",
        "format: section | additions | deletions | path",
        "",
    ]
    if not entries:
        lines.append("No changed files detected.")
    else:
        lines.append("section\tadditions\tdeletions\tpath")
        for entry in sorted(entries, key=lambda item: (item.path, item.section)):
            lines.append(f"{entry.section}\t{entry.additions}\t{entry.deletions}\t{entry.path}")
    return "\n".join(lines) + "\n"
