# Captured Proof v0.6 Review

Status: unreleased public draft candidate

Captured Proof changes the DoneProof evidence model from a typed command claim
to a command that DoneProof executes itself. The resulting receipt binds the
observed exit code, duration, sanitized-output digest, and Git-scope digest into
one integrity-checked object.

## Candidate Acceptance

The candidate is acceptable for release review only while all remain true:

- the command is executed as an argument list, without a shell;
- the child exit code is returned by `doneproof capture`;
- passing, failing, missing, and timed-out commands still write a receipt;
- the receipt does not store raw command output or Git diff content;
- known credential shapes and local home paths are masked before output is
  displayed or hashed;
- the Git-scope digest changes when selected file content changes;
- mutation of any integrity-bound field makes receipt validation fail;
- the bundled and repository JSON Schemas accept the same Captured Proof shape;
- the real demo completes capture, receipt validation, and schema validation in
  under 60 seconds.

## Trust Boundary

Captured Proof is machine-captured and tamper-evident inside one receipt. It is
not a signed attestation, trusted execution environment, correctness proof, or
proof that the machine itself was uncompromised. Consequential work still
requires inspection of the code, diff, checks, and relevant environment.

Redaction is intentionally conservative but cannot recognize every secret
format. Do not pass secrets in command-line arguments. Review every receipt
before sharing it.

## Functional Candidate Evidence — 2026-07-25

Functional baseline:
`d1502aa2488c6a6e0b9fb292757f1b854879ce71`

Public review:
[draft pull request #35](https://github.com/giugiu-a11y/doneproof/pull/35)

Evidence on that functional baseline:

- all 59 repository tests passed;
- Ruff, bytecode compilation, frozen-lockfile, package, and installed-wheel
  checks passed;
- the installed wheel passed `doctor`, a real `capture`, `check`,
  `schema-check`, and JSON `report`;
- a fresh isolated demo completed the full path in 0.50 seconds;
- the shareable GIF is 1100 by 620 pixels, 10.4 seconds, four frames, and 94,674
  bytes;
- the social preview is 1280 by 640 pixels;
- the receipt stored neither raw command output nor Git diff content;
- the exact pushed candidate passed Action Smoke, Secret scan, and Python 3.10,
  3.11, and 3.12 CI.

Documentation-only changes after the functional baseline require their own
exact-head checks. Always verify the live pull request head and checks instead
of treating this file as a self-referential commit record.

## Release Gates

1. **Engineering:** repeat the complete local and remote checks on the exact
   release head.
2. **Privacy:** scan the exact release diff, copy, and generated assets.
3. **Pain confirmation:** receive workflow-level confirmation from at least two
   of five maintainers.
4. **External activation:** one maintainer produces and reviews a receipt from a
   real change.
5. **Repeat use:** one external user repeats the workflow.
6. **Owner approval:** approve the exact release and first distribution post.

Invitations, green tests, and a polished demonstration do not satisfy the
external-use gates.

## Current Gate Status

- Engineering: passed on the functional baseline; must pass again on the final
  documentation-synchronized head.
- Privacy: passed on the functional baseline; must be repeated on the final
  release diff.
- Pain confirmation: 0 of 2 qualified confirmations.
- External activation: 0 of 1.
- Repeat use: 0 of 1.
- Owner approval: candidate work and maintainer outreach approved; release and
  public distribution not approved.

The candidate is available for review in a draft pull request. The stable
release remains `v0.5.0`.
