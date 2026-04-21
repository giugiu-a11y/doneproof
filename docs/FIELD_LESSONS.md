# Field Lessons

DoneProof is not a generic prompt wrapper. It is a small product extracted from repeated agent-ops failures in real local work.

The original incidents are private. This document keeps only the reusable public lesson.

## Lesson 1 - Confidence Is Not Evidence

Problem:

An agent can sound certain before it has checked the actual file, command, endpoint, or UI.

DoneProof response:

- require at least one changed file;
- require at least one command record;
- require at least one evidence item;
- reject completion language like `done`, `complete`, `validated`, and `100%`.

Why it matters:

The receipt makes the agent expose the proof it has, instead of hiding behind fluent prose.

## Lesson 2 - Review Is A State, Not A Vibe

Problem:

Agent work often needs a human review step, but the agent reports as if approval already happened.

DoneProof response:

- default status is `awaiting_review`;
- public examples use review language;
- forbidden statuses block premature approval claims.

Why it matters:

Teams can separate "the agent produced evidence" from "the owner accepted the work."

## Lesson 3 - Handoffs Need Receipts

Problem:

When work moves between chats, agents, editors, or days, context becomes fragile. The next agent may inherit a summary instead of the real state.

DoneProof response:

- store the task, changed files, commands, evidence, and risks in one JSON receipt;
- keep the format local and easy to read;
- provide `doneproof report` for human handoff.

Why it matters:

The next reviewer can inspect the receipt before trusting the story.

## Lesson 4 - Local First Wins Trust

Problem:

Teams hesitate to send private repo state, logs, or agent traces to another service just to verify basic work.

DoneProof response:

- no telemetry;
- no cloud dependency;
- plain files inside the repo;
- policy file owned by the project.

Why it matters:

A team can add proof discipline without adopting a platform.

## Lesson 5 - Small Friction Beats Big Cleanup

Problem:

The costliest failures are usually discovered late: after a confident handoff, after a bad merge, or after a human assumes verification happened.

DoneProof response:

- fail fast on missing proof;
- make skipped checks visible;
- preserve residual risks instead of burying them.

Why it matters:

One extra receipt is cheaper than a cleanup cycle caused by false confidence.

## Public Product Principle

DoneProof should stay small. Its job is not to become the whole agent operating system.

Its job is to make one rule easy to adopt:

> No proof, no done.
