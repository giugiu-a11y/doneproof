# Adversarial Review

Status: published baseline review.

This pass tried to find issues that could appear after the first public release.

## Problems Found And Fixed

### Policy Shape Could Break Validation

Risk:

A user edits `.doneproof/policy.yml` and changes `status`, `minimums`, or `claims` into the wrong YAML type.

Fix:

Validation now reports policy-shape errors instead of crashing.

### Schema Accepted Empty Proof Arrays

Risk:

The JSON schema allowed empty `changed_files`, `commands`, and `evidence`, while the default policy rejected them.

Fix:

The schema now requires at least one item in those arrays.

### Evidence Could Be Too Weak

Risk:

An evidence object with missing `type` or `value` could satisfy the minimum item count.

Fix:

Evidence objects now require non-empty `type` and `value`.

### Public Hygiene Skipped Templates

Risk:

The public hygiene test skipped the entire `.doneproof` directory, so public agent templates could accidentally leak private markers.

Fix:

The hygiene scan now includes `.doneproof` policy/templates and skips only receipt files.

### Unsafe Windows-Style Paths

Risk:

A receipt using `..\secret.txt` could slip past a POSIX-only path traversal check.

Fix:

Changed-file paths now reject backslashes, absolute paths, home-directory paths, and parent traversal.

### External Receipt Root Inference

Risk:

When a caller passed a receipt path outside the repository, `changed_files` existence checks could infer the repository root from the receipt location instead of the explicit `--root`.

Fix:

The CLI now passes the explicit repository root into receipt validation, while the older receipt-location inference remains as a fallback for direct library use.

## Remaining Risks

- The CLI does not yet run full JSON Schema validation; it enforces the same core rules through the policy validator.
- The composite GitHub Action still needs a live GitHub Actions run after the remote exists.
- A static README demo exists; an animated social demo/GIF is still launch polish.
- Future public scope changes should go through the same release gate.

## Current Gate

The release gate for this pass is:

```bash
make prepublish
doneproof check --receipt .doneproof/receipts/latest.json
```
