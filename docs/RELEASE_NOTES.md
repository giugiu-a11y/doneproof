# Release Notes

## Unreleased

No unreleased changes.

## v0.4.0

Released 2026-04-20.

Focused review workflows for larger repositories and easier adoption from editors and CI comments.

### Added

- GitHub Actions PR comment workflow example.
- VS Code task and Cursor rule snippets.
- Solo, team, and CI-gated policy presets.
- `doneproof evidence git-diff --mode` for staged, unstaged, and untracked summaries.

### Verified

- `make check` passed locally.
- `RM_BIN=rm make prepublish` passed locally.
- `gitleaks detect --no-git --source . --redact` found no leaks.
- Main branch CI and Action Smoke passed before release.

## v0.3.1

Released 2026-04-20.

Public-surface privacy polish for repository self-tests and install references.

### Changed

- Encoded private-marker fixtures in the public leak-scan test so the test itself does not visibly spell internal markers.
- Updated GitHub install and Action examples to `v0.3.1`.

### Verified

- `make check` passed locally.
- `RM_BIN=rm make prepublish` passed locally.
- `gitleaks detect --no-git --source . --redact` found no leaks.
- Current public text scan found no matches for the private marker set.

## v0.3.0

Released 2026-04-20.

Automation-friendly handoff output for pull requests, CI comments, and agent adapters.

### Added

- `doneproof report --format json` for automation adapters.
- `doneproof badge` with text, Markdown, and JSON output.

### Changed

- `report --format json` uses repo-relative receipt paths when possible.
- `scripts/prepublish_check.sh` now respects `RM_BIN` and the caller's `PATH`.

### Verified

- `make check` passed locally.
- `RM_BIN=rm make prepublish` passed locally.
- Manual JSON, text, Markdown, and failing-badge command checks passed locally.
- `gitleaks detect --no-git --source . --redact` found no leaks.

## v0.2.1

Released 2026-04-20.

Security and release hardening cleanup.

### Changed

- Raised the minimum supported Python version to 3.10.
- Raised the development `pytest` floor to `9.0.3`.
- Removed the temporary Dependabot ignore for `pytest`.

### Verified

- CI and Action Smoke pass on `main`.
- Dependabot security alert for `pytest` is cleared on the published repo.
- Public leak scan passed again before reopening the repository.

## v0.2.0

Released 2026-04-20.

Git diff evidence for review receipts.

### Added

- `doneproof evidence git-diff` writes a sanitized git diff summary for review receipts.
- Path filtering for git diff evidence artifacts.

### Safety

- Full diff content is omitted by default.
- Secret-like files are skipped by the git evidence helper.

### Maintenance

- Added `uv` Dependabot configuration for dependency updates.
- Raised the build backend floor to `setuptools>=82.0.1`.

### Verified

- CI and Action Smoke pass on `main`.
- `make prepublish` passed locally before release.
- Public leak scan passed before release.

## v0.1.1

Release polish for first public users.

### Added

- GitHub install path in the README.
- Public examples for solo-agent, multi-agent, and CI handoff workflows.
- Launch copy and a clearer public roadmap for contributors.

### Changed

- Package metadata now uses modern SPDX license syntax.
- `make prepublish` now tests editable install, dev install, `python -m build`, wheel install, and installed-package `init`/`doctor`.
- Development dependencies now include `build`.

### Verified

- CI and Action Smoke pass on `main`.
- The composite action was verified from a separate private fixture repository.
- Local and public leak scans passed before release.

## v0.1.0

Initial public release.

### Added

- `doneproof init`
- `doneproof new`
- `doneproof check`
- `doneproof report`
- `doneproof doctor`
- policy file generation
- agent templates for Codex, Claude, Cursor, OpenCode, OpenClaw-style local agents, Hermes-style orchestrators, Aider, and Cline
- receipt schema
- composite GitHub Action draft
- GitHub Actions smoke workflow for the composite action
- CODEOWNERS, Renovate config, and a checked-in `uv.lock`
- field lessons, value proof, pre-GitHub audit, and integration guides
- adversarial review and stronger policy/schema hardening
- tests and smoke checks

### Not Included

- telemetry
- SaaS dashboard
- cloud sync
- package publishing to PyPI
