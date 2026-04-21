# Value Proof

This file explains why DoneProof is worth publishing as a standalone open-source piece.

## One-Sentence Value

DoneProof makes AI agent handoffs auditable before a human trusts them.

## Who Gets Value First

- solo developers using coding agents daily;
- founders running multiple repos with AI help;
- agencies handing agent work between clients;
- small engineering teams experimenting with Codex, Claude Code, Cursor, OpenCode, Cline, or Aider;
- maintainers who want PRs from agents to include proof, not just summaries.

## What It Catches Today

DoneProof v0.2 catches:

- missing receipt files;
- invalid JSON receipts;
- missing required receipt fields;
- forbidden completion statuses;
- empty changed-file lists;
- empty command lists;
- empty evidence lists;
- unsafe changed-file paths;
- malformed command records;
- skipped commands without a reason;
- common premature completion claims.
- sanitized git diff summaries with changed paths and addition/deletion counts.

## What It Does Not Catch Yet

DoneProof v0.2 does not prove:

- the command output is authentic;
- the tests cover the right behavior;
- the UX was visually checked;
- the product decision is correct;
- the code is secure;
- a human approved the work.

This is intentional. The first release is a proof discipline layer, not a full auditor.

## Why It Is Not Just A Checklist

A checklist lives in a prompt and disappears.

DoneProof creates a project artifact:

- machine-readable;
- reviewable;
- testable in CI;
- portable across agents;
- easy to extend with stricter policy later.

## Adoption Test

A new user should be able to:

1. install the package locally;
2. run `doneproof init`;
3. create a receipt with `doneproof new`;
4. run `doneproof check`;
5. understand exactly why a receipt failed.

If that takes more than five minutes, the release is not ready.

## Relevance Test

DoneProof remains relevant only if it keeps answering this question:

> What did the agent actually prove?

Features that do not improve that answer should not enter the core.
