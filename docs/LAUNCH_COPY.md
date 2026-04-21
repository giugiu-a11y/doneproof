# Launch Copy

Status: ready to copy, not posted.

Use one post first. Watch replies for confusion around install, PyPI, GitHub Actions, or whether DoneProof claims to verify correctness.

## X Short

Agent summaries are not evidence.

DoneProof is a small local CLI that makes coding agents leave a receipt before handoff:

- changed files
- commands run
- evidence
- risks
- review status

It says `awaiting_review`, not `done`.

No proof, no done.

https://github.com/giugiu-a11y/doneproof

## X Builder Version

I kept seeing the same failure mode with coding agents.

Not "bad code". False confidence.

The agent says "done", but the handoff does not clearly answer:

- what changed?
- what ran?
- what evidence exists?
- what risk remains?
- is this approved, or just ready for review?

So I built DoneProof.

It is a small local CLI for verification receipts:

```bash
doneproof init
doneproof new
doneproof check
doneproof report
doneproof badge
doneproof evidence git-diff
```

It works with Codex, Claude Code, Cursor, Aider, Cline, OpenCode, OpenClaw-style local agents, and Hermes-style orchestrators because the contract is just files plus JSON.

Human review stays final. The agent provides evidence.

Repo: https://github.com/giugiu-a11y/doneproof

## LinkedIn

I like AI coding agents. I do not like confident handoffs with weak proof.

The painful failures are not always model failures. A lot of them are operational:

- the summary sounds finished;
- the tests were not actually run;
- changed files are vague;
- risk is hidden inside confident language;
- the next agent trusts the previous agent instead of checking the repo.

DoneProof is my small answer to that.

It makes the agent leave a local receipt before handoff:

- changed files;
- commands run;
- evidence;
- residual risks;
- review status.

The default successful status is `awaiting_review`, not `done`.

It does not replace tests, CI, security review, QA, or human judgment. It makes those steps easier to trust because the handoff is concrete.

No proof, no done.

Repo: https://github.com/giugiu-a11y/doneproof

## Technical Thread

1. Coding agents are getting better. The operating layer around them is still messy.
2. The expensive failure is not always wrong code. Often it is a confident handoff with weak evidence.
3. "Done" is not a useful status when a human still has to review the work.
4. DoneProof adds a tiny receipt contract to the repo.
5. A receipt records changed files, commands, evidence, and risks.
6. `doneproof check` rejects missing proof and premature completion language.
7. `doneproof report --format json` gives automation a stable output.
8. `doneproof badge --format markdown` gives PRs a compact receipt badge.
9. `doneproof evidence git-diff --mode staged` keeps diff evidence focused.
10. The GitHub Action can fail a PR when the receipt is missing or weak.
11. It does not replace tests, CI, review, security, or QA.
12. It makes those steps easier to trust because the handoff is concrete.

Repo: https://github.com/giugiu-a11y/doneproof

## Hacker News

Title options:

- Show HN: DoneProof - verification receipts for AI agent work
- Show HN: No proof, no done for coding agents
- Show HN: A local receipt checker for AI coding agents

Post:

I made a small local CLI for a problem I kept hitting with coding agents: they can sound finished before they have left enough evidence to review.

DoneProof creates and checks a receipt with changed files, commands run, evidence, residual risks, and review status.

It is not an agent, dashboard, or hosted service. It is a small pressure point around handoffs.

The default successful status is `awaiting_review`, not `done`.

Repo: https://github.com/giugiu-a11y/doneproof

## Reddit / Community

I made a small open-source CLI for a problem I kept hitting with coding agents: they can sound finished before they have left enough evidence to review.

DoneProof creates and checks a local receipt with:

- changed files;
- commands run;
- evidence;
- residual risks;
- review status.

It is deliberately not an agent and not a dashboard. It is a pressure point around agent handoffs.

The default successful status is `awaiting_review`, not `done`.

Repo: https://github.com/giugiu-a11y/doneproof

I would especially like feedback from people using Codex, Claude Code, Cursor, Aider, Cline, OpenCode, OpenClaw-style local agents, Hermes-style orchestrators, or custom local agents.

## Reply Templates

If someone asks "Does this prove the code is correct?":

```text
No. DoneProof does not replace tests, code review, security review, or QA.

It makes the handoff concrete: changed files, commands run, evidence, risks, and review status.
```

If someone asks "Why not just use CI?":

```text
CI tells you what checks ran. DoneProof tells you what the agent claims it changed, what evidence it left, and what still needs review.

They work well together.
```

If someone asks "Why no PyPI?":

```text
GitHub install is intentional for the first public pass. I want feedback on the contract before adding another package surface.
```

## Positioning Lines

- Agent summaries are not evidence.
- Make AI handoffs reviewable.
- Keep agents humble: awaiting review, not done.
- A receipt layer for coding agents.
- Local-first proof before human review.

## Manual Posting Checklist

- Confirm the repo is public.
- Confirm badges are green.
- Confirm `v0.4.0` is visible.
- Run the GitHub install command once.
- Open the README in a logged-out or private browser window.
- Post one short version first.
- Watch replies for confusion around install, PyPI, GitHub Action, or review status.
- Do not claim DoneProof verifies correctness.
- Do not mention private systems, clients, internal repo names, local paths, or operational details.
