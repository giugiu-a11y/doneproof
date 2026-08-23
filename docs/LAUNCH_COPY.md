# Launch Copy

Status: ready to copy, not posted.

Use one post first. Pair it with `docs/assets/doneproof-social-preview.png`. Watch replies for confusion around install, PyPI, GitHub Actions, or whether DoneProof claims to verify correctness.

## X Short

AI can say “done” before the work is ready.

DoneProof asks coding AIs to leave a receipt:

- what changed
- what it checked
- what still needs attention

Free, open source, and local.

No proof, no done.

https://github.com/giugiu-a11y/doneproof

## X Builder Version

I kept seeing the same problem with coding AI: it sounded finished before the work was actually ready to trust.

The agent says "done", but the handoff does not clearly answer:

- what changed?
- what did it check?
- what proof did it leave?
- what could still go wrong?
- has a person reviewed it yet?

So I built DoneProof.

It gives each AI coding job a small receipt you can inspect:

```bash
doneproof init
doneproof new
doneproof check
doneproof report
doneproof badge
doneproof evidence git-diff
```

It works with Codex, Claude Code, Cursor and other coding tools.

The AI leaves the receipt. A person still makes the final decision.

Repo: https://github.com/giugiu-a11y/doneproof

## LinkedIn

I like using AI to write code. I do not like having to guess whether its confident “done” is real.

The painful problems are often simple:

- the summary sounds finished;
- the tests were not actually run;
- nobody can quickly see what changed;
- remaining risks are hidden behind confident language;
- the next AI trusts the previous answer instead of checking the work.

DoneProof is my small answer to that.

It asks the AI to leave a receipt:

- changed files;
- checks it says it ran;
- proof it saved;
- things that still need attention;
- whether a person has reviewed it.

The default successful status is `awaiting_review`, not `done`.

It does not replace tests or people. It replaces a vague “trust me” with something you can inspect.

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

I made a small open-source tool for a problem I kept hitting with coding AI: it can sound finished before it leaves enough proof to check the work.

DoneProof creates and checks a receipt showing what changed, what the AI says it checked, what proof it left, and what still needs attention.

It runs locally. It is not another AI and does not send your project to a hosted dashboard.

The default successful status is `awaiting_review`, not `done`.

Repo: https://github.com/giugiu-a11y/doneproof

## Reddit / Community

I made a small open-source tool for a problem I kept hitting with coding AI: it can sound finished before it leaves enough proof to check the work.

DoneProof creates and checks a local receipt with:

- changed files;
- checks the AI says it ran;
- proof it saved;
- things that still need attention;
- whether a person has reviewed it.

It runs locally. It is not another AI and not another hosted dashboard.

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

- When AI says “done,” ask for the receipt.
- Make AI handoffs reviewable.
- Replace “trust me” with something you can inspect.
- No proof, no done.

## Manual Posting Checklist

- Confirm the repo is public.
- Confirm badges are green.
- Confirm `v0.5.0` is visible.
- Attach `docs/assets/doneproof-social-preview.png` and check the preview before posting.
- Run the GitHub install command once.
- Open the README in a logged-out or private browser window.
- Post one short version first.
- Watch replies for confusion around install, PyPI, GitHub Action, or review status.
- Do not claim DoneProof verifies correctness.
- Do not mention private systems, clients, internal repo names, local paths, or operational details.
