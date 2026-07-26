# Factbound Run

Review receipts for AI code changes.

**The agent says it passed. Show the run.**

**Captured Proof** turns the check you already run into a shareable **Review
Receipt** tied to the current Git change. Create the first one in under 60
seconds, locally, with no account, agent integration, policy file, or CI change.

It records locally observed execution evidence. It does not prove that the code
is correct, secure, complete, independently attested, signed, or safe to merge.
Human review remains final.

> **Compatibility during candidate review:** the repository, Python package,
> CLI, schema identifiers, and stable release remain `doneproof`. Factbound Run
> is the proposed product identity; this draft does not rename or release those
> public surfaces.

![Captured Proof: command, Git scope, and reviewable receipt](docs/assets/doneproof-demo.gif)

[![CI](https://github.com/giugiu-a11y/doneproof/actions/workflows/ci.yml/badge.svg)](https://github.com/giugiu-a11y/doneproof/actions/workflows/ci.yml)
[![Action Smoke](https://github.com/giugiu-a11y/doneproof/actions/workflows/action-smoke.yml/badge.svg)](https://github.com/giugiu-a11y/doneproof/actions/workflows/action-smoke.yml)
[![Security](https://github.com/giugiu-a11y/doneproof/actions/workflows/security.yml/badge.svg)](https://github.com/giugiu-a11y/doneproof/actions/workflows/security.yml)
[![Release](https://img.shields.io/github/v/release/giugiu-a11y/doneproof)](https://github.com/giugiu-a11y/doneproof/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Create a Review Receipt

The current public release is still `v0.5.0`. Captured Proof is an unreleased
`v0.6` candidate being reviewed on this branch.

Requires Python 3.10+ and a Git repository with at least one current,
privacy-safe change:

```bash
python3 -m pip install "doneproof @ git+https://github.com/giugiu-a11y/doneproof.git@038498b4ca41926150e4952a7f3eabf1c0f371f0"
doneproof capture --task "Check this change" -- git diff --check
doneproof report
```

Factbound Run automatically selects the current privacy-safe changed files.
`git diff --check` is a universal first check for whitespace errors. Replace it
with the repository's real test, lint, build, or verification command when
evaluating the code itself.

### Close the loop on one real change

Trying the candidate is useful only if it answers the maintainer question:
did the receipt reduce review ambiguity, make no material difference, or add
ceremony?

Bring one public-safe, agent-authored change and its real check. You run the
command in a repository you control; the trial can be guided or self-serve and
requires no product integration. Use the
[five-minute validation trial](docs/VALIDATION_TRIAL.md), then report the
review outcome on
[draft pull request #35](https://github.com/giugiu-a11y/doneproof/pull/35).
A passing command alone is engineering evidence, not product validation.

## What You Get

- a small CLI for receipts, checks, reports, and git diff evidence;
- the **Captured Proof** mechanism, which runs a real command and binds its exit code,
  duration, sanitized output digest, and Git scope into the receipt;
- a composite GitHub Action for pull request gates;
- integration templates for Codex, Claude Code, Cursor, OpenCode, OpenClaw-style agents, and Hermes-style orchestrators;
- review language that blocks agents from claiming approval early.

See the visual walkthrough in [docs/DEMO.md](docs/DEMO.md).

## Why It Exists

Factbound Run comes from real multi-agent work where the expensive failures were not model intelligence failures.

They were operations failures:

- an agent said work was ready without enough evidence;
- a handoff lost the actual state of the project;
- a later agent trusted a confident summary instead of checking files;
- a task was reported as finished while review still had to happen;
- the human had to discover missing tests, missing files, or unclear risk after the fact.

Factbound Run turns those lessons into a small local rule: every agent delivery
needs a Review Receipt with files, commands, evidence, and risk.

## The Problem

AI agents are great at saying:

> Done.

But did the agent:

- change the files it claims it changed?
- run the command it claims it ran?
- preserve the evidence?
- mention the risks?
- avoid declaring victory before review?

Factbound Run adds one rule:

> If there is no receipt, the work is not ready.

## How Captured Proof Works

Run the complete isolated demo from a candidate checkout:

```bash
uv run --frozen --extra dev python scripts/captured_proof_demo.py
```

The script creates an isolated Git repository, changes a real file, auto-selects
that file, runs `git diff --check` through `doneproof capture`, validates the
receipt and JSON schema, and renders the human-readable report. The measured
runtime printed by the script is evidence for that run, not a cross-machine
performance guarantee.

Use the command in your own changed repository:

```bash
doneproof capture --task "Run the repository tests" -- python3 -m pytest -q
doneproof report
```

Captured Proof records:

- the real exit code and duration;
- a SHA-256 digest of sanitized command output, without storing raw output;
- a SHA-256 digest of the selected Git patch and untracked file bytes, without
  storing the diff;
- safe environment metadata and an integrity digest over the proof object.

Known secret patterns and local home paths are masked before output is shown or
hashed. This reduces accidental leakage; it is not a guarantee that arbitrary
secrets can never appear.

The integrity digest detects accidental or unsophisticated mutation inside the
receipt. It is not signed, remotely attested, or trustless. Human review of the
actual code and diff remains required.

The candidate acceptance criteria, trust boundary, and remaining release gates
are documented in
[docs/CAPTURED_PROOF_V0_6_REVIEW.md](docs/CAPTURED_PROOF_V0_6_REVIEW.md).

## Manual Receipt Flow (v0.5.0)

The stable release also supports manually authored receipts:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install "doneproof @ git+https://github.com/giugiu-a11y/doneproof.git@v0.5.0"
doneproof init
doneproof new \
  --task "Add health check endpoint" \
  --changed-file README.md \
  --command "passed:python3 -m pytest" \
  --evidence "test:pytest passed" \
  --risk "Manual browser check not performed"
doneproof check
doneproof schema-check
doneproof report
```

For local development on DoneProof itself:

```bash
git clone https://github.com/giugiu-a11y/doneproof.git
cd doneproof
uv sync --extra dev --frozen
make prepublish
```

## Demo

The animated walkthrough is generated from a real Captured Proof execution:

![DoneProof animated demo](docs/assets/doneproof-demo.gif)

Reproduction steps and the exact trust boundary:

- [docs/DEMO.md](docs/DEMO.md)

The stable `v0.5.0` receipt fixtures remain available:

```bash
doneproof check --receipt examples/receipts/passing.json
doneproof schema-check --receipt examples/receipts/passing.json
```

```text
DoneProof: PASS
```

Failing receipt:

```bash
doneproof check --receipt examples/receipts/failing.json
doneproof schema-check --receipt examples/receipts/failing.json
```

```text
DoneProof: FAIL
error: Forbidden status: done
error: changed_files needs at least 1 item(s)
error: commands needs at least 1 item(s)
error: evidence needs at least 1 item(s)
```

## Commands

```bash
doneproof init               # create policy and agent templates
doneproof new                # create a receipt draft
doneproof capture            # run a command and write Captured Proof (v0.6 candidate)
doneproof check              # validate a receipt
doneproof schema-check       # validate receipt JSON shape against schema
doneproof evidence git-diff  # write a sanitized git diff summary
doneproof evidence git-diff --mode staged
doneproof report             # print a human-readable receipt
doneproof report --format json
doneproof badge              # print a compact receipt badge
doneproof doctor             # check local setup
```

`check`, `schema-check`, and `report` default to:

```text
.doneproof/receipts/latest.json
```

`evidence git-diff` defaults to:

```text
.doneproof/evidence/git-diff-summary.txt
```

The git diff evidence helper stores file paths plus addition/deletion counts. It does not store full diff content by default. Reviewers should still inspect the actual diff before approval.

Captured Proof goes further: its Git-scope digest is calculated from the actual
selected patch and untracked file bytes. The receipt still stores only the
digest and privacy-safe file list.

## Receipt Format

```json
{
  "task": "Add a health check endpoint",
  "status": "awaiting_review",
  "summary": "Added endpoint and tests.",
  "changed_files": ["app/main.py", "tests/test_health.py"],
  "commands": [
    {
      "cmd": "pytest tests/test_health.py",
      "status": "passed"
    }
  ],
  "evidence": [
    {
      "type": "test",
      "value": "pytest tests/test_health.py passed"
    }
  ],
  "risks": ["Manual browser check not performed"]
}
```

Machine-readable schema:

```text
schemas/receipt.schema.json
```

## Status Values

Allowed by default:

- `awaiting_review`
- `blocked`
- `failed`

Rejected by default:

- `done`
- `complete`
- `completed`
- `validated`
- `100%`
- `pronto`

DoneProof intentionally prefers review language. A human approves. The agent provides evidence.

## Agent Templates

After `doneproof init`, templates are created in:

```text
.doneproof/templates/
```

Included templates:

- `codex.md`
- `claude.md`
- `cursor.md`
- `opencode.md`
- `openclaw.md`
- `hermes.md`
- `aider.md`
- `cline.md`

Copy the relevant template into your agent instructions and adapt it to your repo.

Integration guides:

```text
docs/INTEGRATIONS.md
docs/integrations/
```

## GitHub Action

DoneProof includes a composite GitHub Action.

```yaml
- uses: giugiu-a11y/doneproof@89f2b9da284b770feeda94a75261ac42e145cdc9 # v0.5.0
  with:
    receipt: .doneproof/receipts/latest.json
```

## PR Badge

Create a compact badge for pull request descriptions, CI comments, or handoff notes:

```bash
doneproof badge --format markdown
```

Example output:

```markdown
![DoneProof: awaiting_review | risks: 1](https://img.shields.io/badge/DoneProof-awaiting_review%20%7C%20risks%3A%201-yellow)
```

For automation, use structured output:

```bash
doneproof report --format json
doneproof badge --format json
```

Recommended pull request gate:

```yaml
name: DoneProof

on:
  pull_request:

jobs:
  receipt:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0 # v7.0.0
      - uses: giugiu-a11y/doneproof@89f2b9da284b770feeda94a75261ac42e145cdc9 # v0.5.0
        with:
          receipt: .doneproof/receipts/latest.json
```

## Agent Instruction

Paste this into `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, or your agent instructions:

```text
Before final response, create or update .doneproof/receipts/latest.json.
Run doneproof check --receipt .doneproof/receipts/latest.json.
Use status awaiting_review for successful work. Do not say the work is approved.
Include changed files, commands, evidence, and residual risks.
```

More examples:

```text
docs/EXAMPLES.md
docs/EDITOR_TASKS.md
docs/POLICY_PRESETS.md
docs/integrations/
```

## Design Principles

- local-first;
- no telemetry;
- no cloud dependency;
- born from real agent-ops incidents;
- evidence over confidence;
- review status over completion claims;
- clear failure messages;
- safe examples only.

## When It Helps

DoneProof is useful when:

- more than one agent or chat can touch the same project;
- a human reviews agent work after the agent leaves;
- a repo has many small changes that are easy to overclaim;
- CI passing is not enough to prove the requested work was actually handled;
- the team wants agents to say `awaiting_review` instead of pretending approval already happened.

It is not a replacement for tests, CI, code review, product QA, or human approval. It is a lightweight pressure point that makes those steps easier to trust.

## Release Status

Current public release: `v0.5.0`.

The `main` branch is checked by CI and by an Action Smoke workflow that runs the composite action against the passing receipt fixture.

Captured Proof `v0.6` is an unreleased candidate in public draft review. A clean
demonstration and candidate privacy review exist. Release remains blocked on
at least two qualified maintainer pain confirmations, one external real-change
receipt, one repeat use, a final exact-release privacy and engineering rerun,
and explicit owner approval.
