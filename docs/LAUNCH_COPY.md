# Launch Copy

Status: prepared for gated release; not approved or posted.

Do not publish this copy until the release gates in `docs/LAUNCH_PLAN.md` are
closed. Start with one channel, answer real objections, and revise only from
observed feedback.

## Message Contract

- Category: local check evidence for AI code changes.
- Hook: Your agent says the check passed. Review what actually ran.
- Promise: Run the check. Get a shareable receipt tied to the current Git
  change.
- Mechanism: Captured Proof connects one observed command result to the
  selected Git scope.
- Boundary: it records observed local evidence. It does not prove correctness,
  security, authorship, or approval.

## X

Your agent says the check passed. Review what actually ran.

Captured Proof runs one local check and creates a shareable receipt tied to the
current Git change.

It records observed evidence. It does not replace code review, security review,
or judgment.

No proof, no done.

https://github.com/giugiu-a11y/doneproof

## LinkedIn

AI coding agents can produce convincing summaries before a reviewer has enough
evidence to trust the change.

Captured Proof, inside DoneProof, runs one local check and creates a shareable
receipt tied to the current Git change. The receipt records:

- the exact command;
- its observed exit code and duration;
- the selected changed files;
- privacy-safe digests for output and Git scope;
- an explicit `awaiting_review` status.

That boundary matters: DoneProof records what ran. It does not claim the code is
correct, secure, or approved.

The goal is a smaller review gap between “the agent says it passed” and “I can
inspect the evidence.”

No proof, no done.

https://github.com/giugiu-a11y/doneproof

## Hacker News

Preferred title:

> Show HN: DoneProof — receipts for checks run on AI code changes

Post:

I built Captured Proof after repeatedly seeing coding-agent handoffs that
sounded complete but did not make the executed check easy to review.

`doneproof capture` runs one command without a shell and writes a receipt tied
to the selected Git change. It records the observed exit code, duration, and
privacy-safe digests without storing raw command output or Git diff content.

The successful review state is `awaiting_review`, not `done`.

It is deliberately a local evidence layer, not an agent, hosted dashboard, or
claim that the code is correct.

Repo: https://github.com/giugiu-a11y/doneproof

## Reddit / Developer Community

I am looking for maintainer feedback on a narrow problem: reviewing the check
an AI coding agent says it ran.

Captured Proof runs one local command and creates a receipt tied to the current
Git change. The receipt contains the observed result and review state, while
omitting raw output and diff content.

It does not replace CI or human review. It makes one check easier to inspect and
share.

If you maintain a repository that accepts agent-authored changes, I would value
feedback on whether this receipt would reduce review ambiguity in a real pull
request.

Repo: https://github.com/giugiu-a11y/doneproof

## Reply Templates

If someone asks “Does this prove the code is correct?”:

```text
No. Captured Proof records one observed local check and binds it to the selected
Git change. Correctness, security, coverage, and approval still require their
own review.
```

If someone asks “Why not just use CI?”:

```text
CI remains essential. Captured Proof addresses the handoff before or alongside
CI: which local check ran, what Git scope it covered, and what still needs
review. The two layers complement each other.
```

If someone asks “What can I safely share?”:

```text
The receipt omits raw command output and Git diff content. Known credential and
home-path shapes are masked before output is displayed or hashed. Review every
receipt before sharing because no redactor can recognize every secret format.
```

If someone asks “Why is the repository named DoneProof?”:

```text
DoneProof is the existing project name. Captured Proof is the specific
mechanism: run one check and receive a reviewable receipt tied to the Git
change. We are testing the mechanism before considering any broader brand
architecture.
```

## Product Boundary

DoneProof does not manage session selection, cross-session continuity, or memory
promotion. Continuity Loop and Memory Boundary are independent products with
their own categories and first-use paths.

Do not present the three projects as a system, suite, platform, family, bundle,
or required sequence.

## Manual Posting Checklist

- Confirm the exact release candidate is the reviewed and published `v0.6.0`
  tag.
- Confirm all required checks are green on that exact commit.
- Repeat the privacy scan after the final release diff.
- Run the public install and Captured Proof path in a clean environment.
- Open the README and demo asset while logged out.
- Confirm the release gates and owner approval are recorded.
- Publish one channel only; observe before adapting the next channel.
- Do not add unsupported adoption, performance, security, or correctness
  claims.
- Do not expose private systems, clients, paths, prompts, logs, or operational
  details.
