# Release Notes

## Unreleased

### Added

- Added `doneproof capture`, which executes a command without a shell and writes
  a Captured Proof object containing the observed exit code, measured duration,
  sanitized-output digest, selected Git-scope digest, and proof integrity
  digest.
- Added receipt and JSON Schema validation for Captured Proof.
- Added an isolated real-run demonstration plus animated, static, and accessible
  visual artifacts.

### Safety

- Raw command output and Git diff content are not stored in the receipt.
- Known credential shapes and Unix and Windows home paths are masked before
  command output is displayed or hashed.
- Capture refuses to execute when it cannot first resolve a privacy-safe changed
  Git scope.
- Commands run as argument vectors without a shell, and timed-out process groups
  are terminated.

### Trust boundary

- Captured Proof is tamper-evident inside a receipt; it is not signed or remotely
  attested.
- It records what ran, not whether the selected check was sufficient or whether
  the code is semantically correct. Human review remains required.

### Verified for the release candidate

- The isolated capture, receipt validation, and schema validation flow completed
  in `0.42` seconds on the development machine; this is a measured run, not a
  cross-machine performance claim.

### Changed

- Pinned every external GitHub Action used by CI, security, smoke tests, and the copyable PR-comment example to a verified full commit SHA.
- Upgraded Checkout to v7 and added a regression test that rejects mutable Action references.

## v0.5.0

Released 2026-07-14.

### Added

- `doneproof schema-check` with a bundled Draft 2020-12 receipt schema and machine-readable output.
- Full-history secret scanning with a checksum-verified Gitleaks binary and a commit-pinned checkout action.
- PyPI readiness decision path with explicit Go/No-Go criteria, rollback steps, and verification gate in `docs/PYPI_READINESS.md`.

### Changed

- Default schema output now uses a stable logical label instead of exposing an installation path.
- Publishing checklist now links PyPI readiness checks to issue #2 without publishing by default.

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
