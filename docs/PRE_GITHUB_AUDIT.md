# Pre-GitHub Audit

Status: published after owner approval on 2026-04-20.

This audit records the local state used for the first GitHub publication.

## Product Relevance

DoneProof is relevant because it turns repeated agent-ops failures into a small enforceable artifact:

- false confidence becomes forbidden completion language;
- missing proof becomes a failing receipt;
- fragile handoff becomes a JSON record;
- unclear review state becomes `awaiting_review`;
- residual risk becomes explicit.

The public story is based on anonymized operational lessons, not on private project details.

## Local Verification

Latest local gate run:

```bash
make prepublish
```

Observed result:

- ruff passed;
- 26 pytest tests passed;
- Python compile check passed;
- smoke fixture passed;
- passing receipt fixture passed;
- failing receipt fixture failed as expected;
- local receipt check passed when present;
- wheel build passed;
- wheel install in a temporary venv passed;
- installed `doneproof` console script responded.

## Publication Status

Published state:

- public source files are present;
- GitHub workflow is present;
- composite action smoke workflow is present;
- issue and PR templates are present;
- CODEOWNERS and Renovate config are present;
- `uv.lock` is present as the development dependency baseline;
- release docs are present;
- import runbook is present;
- launch copy draft is present;
- adversarial review is present;
- static README demo is present.

Still separate from repository publication:

- animated social demo/GIF is still optional launch polish;
- public launch posts still need separate approval.

## Final Rule

Future package publishing, launch posts, telemetry, or major scope changes need explicit owner approval.
