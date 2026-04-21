# Examples

DoneProof is intentionally small. These examples show the workflows it is meant to protect.

## Solo Agent Work

A coding agent edits a repo and wants to hand back the task.

```bash
doneproof new \
  --task "Add health check endpoint" \
  --changed-file app/main.py \
  --changed-file tests/test_health.py \
  --command "passed:pytest tests/test_health.py" \
  --evidence "test:pytest tests/test_health.py passed" \
  --risk "Manual browser check not performed"

doneproof check
doneproof report
```

The final agent answer should say the work is `awaiting_review`, not approved.

## Structured Report Output

Use JSON output when another tool needs to consume the validated receipt:

```bash
doneproof report --format json
```

This returns the receipt summary plus validation errors and warnings in a stable structure.

## Badge Output

Use a compact badge in pull request descriptions, CI comments, or handoff notes:

```bash
doneproof badge --format markdown
```

Text and JSON output are also available:

```bash
doneproof badge
doneproof badge --format json
```

## Git Diff Evidence

When a reviewer needs a quick shape of the repo changes, create a sanitized diff summary:

```bash
doneproof evidence git-diff
```

This writes:

```text
.doneproof/evidence/git-diff-summary.txt
```

The artifact includes staged, unstaged, and untracked file names with addition/deletion counts. It does not include full diff content by default.

Use a path filter when the task only touched one area:

```bash
doneproof evidence git-diff --path docs
```

Use a narrower mode when the repo is large:

```bash
doneproof evidence git-diff --mode staged
doneproof evidence git-diff --mode unstaged
doneproof evidence git-diff --mode untracked
```

Then reference the artifact in the receipt:

```bash
doneproof new \
  --task "Update integration docs" \
  --changed-file docs/INTEGRATIONS.md \
  --command "passed:pytest" \
  --evidence "git-diff:.doneproof/evidence/git-diff-summary.txt" \
  --risk "Reviewer still needs to inspect the actual diff"
```

This helps review, but it does not replace code review.

## Multi-Agent Handoff

One agent writes code. Another agent reviews or continues later.

The receipt gives the second agent a concrete starting point:

- files changed;
- commands run;
- evidence captured;
- skipped checks;
- residual risks.

That is better than trusting a summary like "everything is done".

## Pull Request Gate

Use DoneProof in CI when agent-authored pull requests must include a receipt.

```yaml
name: DoneProof

on:
  pull_request:

jobs:
  receipt:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: giugiu-a11y/doneproof@v0.4.0
        with:
          receipt: .doneproof/receipts/latest.json
```

This does not prove the code is correct. It proves the handoff contains reviewable evidence.

For a pull request comment workflow, use:

```text
docs/examples/github-pr-comment.yml
```

## Editor Tasks

Use editor tasks when the team wants one-click receipt commands:

```text
docs/EDITOR_TASKS.md
docs/examples/vscode-tasks.json
docs/examples/cursor-doneproof-rule.mdc
```

## Policy Presets

Start from a small policy preset instead of inventing one from scratch:

```text
docs/POLICY_PRESETS.md
examples/policies/solo.yml
examples/policies/team.yml
examples/policies/ci-gated.yml
```

## What A Good Receipt Says

Good:

```json
{
  "task": "Add health check endpoint",
  "status": "awaiting_review",
  "summary": "Added endpoint and tests.",
  "changed_files": ["app/main.py", "tests/test_health.py"],
  "commands": [{"cmd": "pytest tests/test_health.py", "status": "passed"}],
  "evidence": [{"type": "test", "value": "pytest tests/test_health.py passed"}],
  "risks": ["Manual browser check not performed"]
}
```

Bad:

```json
{
  "task": "Fix app",
  "status": "done",
  "summary": "All good.",
  "changed_files": [],
  "commands": [],
  "evidence": [],
  "risks": []
}
```

DoneProof rejects the second receipt because it asks the reviewer to trust confidence instead of evidence.
