# Code Quality Review

Status: published baseline review.

This review covers the first public baseline of DoneProof.

## Architecture

DoneProof is intentionally small:

- `cli.py` owns argument parsing and command routing;
- `receipt.py` owns receipt loading, writing, and validation;
- `policy.py` owns `.doneproof` project setup and policy loading;
- `defaults.py` owns the default policy and agent templates;
- `doctor.py` owns setup checks;
- `git.py` owns changed-file discovery.

This is a good v0.1 shape. The product is a CLI and receipt contract, not a server or framework.

## Stack

- Python package with `src/` layout;
- `setuptools` build backend;
- PyYAML for policy parsing;
- pytest for tests;
- ruff for lint;
- no telemetry;
- no runtime service;
- no cloud dependency.

The stack is conservative and appropriate for a first open-source CLI.

## Quality Checks Added

- `make check` for lint, tests, and smoke;
- `make check` also runs Python compile checks;
- `make prepublish` for lint, tests, compile checks, smoke fixture, receipt fixtures, local receipt check, wheel build, and installed console script check;
- tests for YAML parse, JSON schema load, public hygiene, release docs, and README relevance;
- adversarial tests for malformed policy, blank summaries, evidence shape, and unsafe paths;
- explicit repository-root handling when validating receipts outside the default receipt directory;
- doctor now derives required templates from the canonical template map.

## Findings Addressed

### Template Drift Risk

Before: `doctor.py` had a hard-coded template list.

Fix: `doctor.py` now derives expected templates from `defaults.TEMPLATES`, so new integrations are checked automatically.

### Weak Claim Scanning

Before: forbidden completion claims were not scanned inside evidence objects.

Fix: receipt validation now scans nested evidence and risks while preserving word-boundary checks so `doneproof` itself does not trigger the word `done`.

### Malformed Policy Crash Risk

Before: a malformed policy section could raise an exception instead of becoming a validation finding.

Fix: status, minimums, and claims policy shapes now produce explicit errors. Invalid minimum values do not crash validation.

### Schema And Policy Drift

Before: the JSON schema allowed empty `changed_files`, `commands`, and `evidence` arrays even though default policy rejected them.

Fix: the schema now includes `minItems: 1` for those arrays.

### Public Hygiene Blind Spot

Before: public hygiene tests skipped all `.doneproof` files, including public templates.

Fix: hygiene now scans `.doneproof` policy/templates and skips only receipts.

### External Receipt Path Inference

Before: a receipt path outside the repository could make changed-file checks infer the wrong root.

Fix: CLI validation now passes the explicit `--root` into the validator. Receipt-path inference remains only as a fallback.

### Thin Agent Integrations

Before: agent templates existed but were too minimal for a public release.

Fix: practical templates and docs now cover Codex, Claude Code, Cursor, OpenCode, OpenClaw-style local agents, Hermes-style orchestrators, Aider, and Cline.

## Remaining Risks

- The composite GitHub Action still needs a live GitHub Actions run after a remote exists.
- No visual demo/GIF exists yet.
- Public launch posts and major positioning changes still need separate owner approval.
- JSON schema validation is documented but not yet enforced by the CLI; v0.1 uses the local policy validator as the source of enforcement.

## Decision

The codebase is appropriate for a v0.1 public candidate after the remaining GitHub-only checks are completed.
