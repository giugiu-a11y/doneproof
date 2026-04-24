# Publishing Checklist

Status: public repo open; latest release gate documented below; social launch not posted.

## Release Gate

- [x] Read `docs/FIELD_LESSONS.md` and confirm the public positioning still matches the actual product.
- [x] Read `docs/VALUE_PROOF.md` and confirm v0.1 still solves a real agent-ops problem.
- [x] Run `make check`.
- [x] Run `make prepublish`.
- [x] Run `doneproof doctor`.
- [x] Run `doneproof check`.
- [x] Search for private paths and secrets.
- [x] Confirm `ACTIVE_VERSION.json`, `PROJECT_STATUS.md`, and local `AGENTS.md` are not committed.
- [x] Review README quickstart against real command output.
- [x] Confirm examples are anonymous.
- [x] Confirm issue templates do not ask users to paste secrets.
- [x] Confirm `.github/CODEOWNERS` points to the approved owner.
- [x] Confirm `renovate.json5` is appropriate for the public repo.
- [x] Confirm `uv.lock` is current.
- [x] Confirm `action.yml` works against a fixture before release.
- [x] Confirm `.github/workflows/action-smoke.yml` passes on GitHub Actions.
- [x] Confirm LICENSE, SECURITY, CONTRIBUTING, and CODE_OF_CONDUCT exist.
- [x] Create release notes.
- [x] Review `docs/LAUNCH_COPY.md` manually.
- [x] Review `docs/PRE_GITHUB_AUDIT.md` manually.
- [x] Review `docs/ADVERSARIAL_REVIEW.md` manually.
- [x] Publish GitHub repository after approval.
- [x] Publish GitHub profile README.
- [x] Enable GitHub secret scanning and push protection.
- [x] Protect `main` with required release checks.
- [ ] Owner posts launch copy manually.

## Explicitly Forbidden Without Separate Approval

- package publishing
- additional public launch posts
- adding telemetry

## PyPI Readiness Gate (Issue #2)

Run this section only when public install feedback indicates packaging friction.

- [ ] Read `docs/PYPI_READINESS.md`.
- [ ] Confirm the Go / No-Go rule is satisfied using public evidence links.
- [ ] Confirm rollback owner and rollback command path before upload.
- [ ] Verify release notes include rollback guidance for the candidate version.
- [ ] Keep GitHub install as default path until the first PyPI publish is verified.
