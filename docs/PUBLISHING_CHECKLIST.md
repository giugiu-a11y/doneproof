# Publishing Checklist

Status: public repository live; Captured Proof candidate in draft review;
`v0.6.0` and distribution not approved.

## Candidate Gate

- [x] Define the category, promise, primary user, named mechanism, and truth
  boundary.
- [x] Demonstrate the real capture-to-review loop in under 60 seconds.
- [x] Keep raw command output and Git diff content out of the receipt.
- [x] Verify the functional baseline with 59 tests, package checks, installed
  wheel smoke, privacy scan, and five required GitHub checks.
- [x] Prepare release and channel copy without unsupported claims.
- [x] Open the candidate as a draft pull request.
- [x] Invite five maintainers with relevant agent-review workflows.

## Market Gate

- [ ] Receive qualified workflow-level pain confirmation from two of five
  maintainers.
- [ ] Produce and review one receipt from an external real change.
- [ ] Confirm one repeat external use.
- [ ] Record objections and revise only when evidence justifies it.
- [ ] Send no more than one follow-up per maintainer in the documented window.

## Exact Release Gate

- [ ] Freeze the exact release commit.
- [ ] Run `make check`.
- [ ] Run `make prepublish`.
- [ ] Build and install the wheel in a clean environment.
- [ ] Run `doneproof doctor`, a real `capture`, `check`, `schema-check`, and JSON
  `report` from the installed wheel.
- [ ] Confirm all required GitHub checks are green on the exact release commit.
- [ ] Scan the exact diff, added lines, copy, and generated assets for secrets,
  local paths, private systems, internal names, prompts, logs, and metadata.
- [ ] Confirm README, demo, release notes, and launch copy describe the same
  product and trust boundary.
- [ ] Confirm LICENSE, SECURITY, CONTRIBUTING, CODE_OF_CONDUCT, CODEOWNERS, and
  issue templates remain correct.
- [ ] Verify the public install and demo path while logged out.
- [ ] Obtain owner approval for the exact release.

## Distribution Gate

- [ ] Publish `v0.6.0` from the verified commit.
- [ ] Verify the tag, release assets, and public install path.
- [ ] Publish one approved channel only.
- [ ] Observe real replies before adapting the next channel.
- [ ] Never claim correctness, security, approval, adoption, or performance
  beyond the recorded evidence.

## Explicitly Forbidden Without Separate Approval

- merging or publishing `v0.6.0`;
- posting launch copy;
- publishing to PyPI;
- adding telemetry, a dashboard, hosted service, or paid infrastructure;
- presenting DoneProof, Continuity Loop, and Memory Boundary as a suite or
  umbrella brand.

## PyPI Readiness Gate

Evaluate PyPI only after observed public install friction:

- [ ] Read `docs/PYPI_READINESS.md`.
- [ ] Satisfy its evidence-based Go / No-Go rule.
- [ ] Confirm rollback ownership and commands before upload.
- [ ] Include rollback guidance in the candidate release notes.
- [ ] Keep the GitHub install path as default until the first PyPI release is
  independently verified.
