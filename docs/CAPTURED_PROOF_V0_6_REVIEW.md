# Captured Proof v0.6 Review

Status: unreleased candidate

Captured Proof changes the DoneProof evidence model from a typed command claim
to a command that DoneProof executes itself. The resulting receipt binds the
observed exit code, duration, sanitized output digest, and Git-scope digest into
one integrity-checked object.

## Candidate Acceptance

The candidate is acceptable for release review when all of these statements
remain true:

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
not a signed attestation, a trusted execution environment, or proof that the
machine itself was uncompromised. A person reviewing consequential work must
still inspect the code, diff, and relevant environment.

Redaction is intentionally conservative but cannot recognize every possible
secret format. Secrets should not be passed in command-line arguments because
other local processes may be able to inspect the operating system process
table. Prefer scoped environment injection or an existing secret manager, and
review the command output before sharing a receipt.

## Release Gates

The implementation and demo do not authorize publication. Release still
requires:

1. the complete test, lint, schema, package, and installed-wheel checks;
2. a privacy scan of the exact release diff and assets;
3. one qualified conversation with a maintainer who operates an agent workflow;
4. final owner review of the public release and distribution copy.

Until all four close, the public release remains `v0.5.0`.

## Candidate Evidence — 2026-07-25

Candidate implementation commit:
`8d8549692f7295815e3f1b6a842c05922762021e`

Public review:
[draft pull request #35](https://github.com/giugiu-a11y/doneproof/pull/35)

Candidate verification is complete:

- all 57 repository tests passed;
- Ruff, bytecode compilation, and the frozen lockfile check passed;
- a `doneproof-0.6.0-py3-none-any.whl` wheel was built and installed in a clean
  Python 3.12 environment;
- the installed wheel passed `doctor`, a real `capture`, `check`,
  `schema-check`, and JSON `report`;
- the latest isolated demo completed capture, receipt validation, and schema
  validation in `0.58` seconds (`0.70` seconds wall time);
- the exact pushed Git range passed Gitleaks 8.30.1 with no leaks;
- added lines passed the internal-runtime marker scan; the three deliberate
  privacy-fixture lines were reviewed; generated assets passed embedded-string
  and metadata checks;
- GitHub completed `action-smoke`, `Secret scan`, and the Python 3.10, 3.11,
  and 3.12 CI jobs successfully on that exact commit.

## Gate Status

1. **Engineering gate: passed for the candidate commit.** Local verification
   and all five required GitHub checks are green on the exact pushed head.
2. **Privacy gate: passed for the candidate commit.** The exact pushed range,
   added lines, generated assets, and public copy were checked. This gate must
   be repeated if the release diff changes.
3. **Maintainer feedback gate: pending.** An invitation is not a qualified
   conversation; a concrete maintainer response is required.
4. **Owner gate: partially approved.** Creating the public candidate PR and
   maintainer outreach is approved. Publishing the release or distribution copy
   still requires a separate final review.

The candidate is live as a draft public review PR. It is not ready for a
`v0.6.0` release.
