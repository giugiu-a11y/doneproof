# PyPI Readiness Path

Status: deferred until real install friction appears in public feedback.

This document defines when DoneProof should add a PyPI package surface and how to roll back safely if a publish causes confusion or breakage.

## Decision Inputs

Use only public signals (issues, discussions, PR comments, external adoption reports). Do not use private chats or internal-only pressure.

- Install friction: repeated reports that GitHub tag install blocks adoption.
- Adoption signal: at least one external repository uses DoneProof successfully.
- Scope signal: feedback asks for packaging/distribution, not a broader product pivot.

## Go / No-Go Rule

Default decision: **No-Go** until the signals above are present.

Only switch to **Go** when all conditions are true:

1. At least two independent public reports ask for PyPI-style install or tooling compatibility.
2. There is at least one external usage signal (issue, PR, or mention) showing real adoption.
3. `make check`, `make prepublish`, and secret scan pass on the candidate release commit.
4. Release owner confirms the rollback steps below are prepared before upload.

If any condition is missing, keep GitHub install as the only supported path.

## Rollback Path

If PyPI publish causes breakage, confusion, or incorrect package ownership:

1. Yank the affected PyPI release version immediately.
2. Update README/install docs back to the GitHub tag path as primary.
3. Cut a follow-up patch release only after the same verification gate passes again.
4. Open a public issue with what failed, impact, and next safe attempt criteria.

## Verification Path Before First Publish

Run on a clean checkout of the exact release commit:

1. Build artifacts (`python -m build`) and inspect metadata (`twine check dist/*`).
2. Validate local install in a fresh virtualenv and run:
   - `doneproof --help`
   - `doneproof init --root /tmp/doneproof-pypi-smoke`
   - `doneproof doctor --root /tmp/doneproof-pypi-smoke`
3. Run repository gates:
   - `make check`
   - `make prepublish`
4. Run secret scan (`gitleaks detect --no-git --source . --redact --no-banner`).
5. Verify release notes and rollback note are included before publish.

## Explicit Non-Goals

- No package publish from this document alone.
- No telemetry or cloud dependency changes.
- No expansion of DoneProof scope beyond receipt verification.
