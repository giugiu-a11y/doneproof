# Captured Proof Validation Trial

This five-minute trial tests one question:

> Does a Captured Proof receipt make an AI-authored code change easier to
> review?

The goal is not to produce another passing test. The goal is to observe whether
the receipt changes a real review decision.

## Before You Start

Use a repository and change that you are allowed to inspect and discuss.
Choose one small, real change with a normal verification command such as a
targeted test, lint check, build check, or `git diff --check`.

Do not share secrets, raw diffs, private output, customer names, private
repository details, local home paths, or provider credentials. Review every
receipt before sharing it.

## Run the Trial

Requires Python 3.10+ and Git:

```bash
python3 -m pip install "doneproof @ git+https://github.com/giugiu-a11y/doneproof.git@feature/captured-proof-v0.6"
doneproof doctor
doneproof capture --task "Review this change" -- git diff --check
doneproof check
doneproof schema-check
doneproof report
```

Replace `git diff --check` with the repository's real verification command when
you want to evaluate the code itself.

## Review the Receipt

Inspect the receipt beside the same Git change and answer:

1. Did it reduce ambiguity about what actually ran and which change it covered?
2. What evidence or linkage was still missing?
3. Did it fit the review moment, or add ceremony?
4. Would you use it again without coaching?

The receipt should end in `awaiting_review`. That is intentional: Captured
Proof records observed evidence and leaves approval to the reviewer.

## Report the Outcome

Comment on
[draft pull request #35](https://github.com/giugiu-a11y/doneproof/pull/35)
with this compact report:

```text
Change type:
Check run:
Review effect: reduced ambiguity | no material difference | added ceremony
Missing evidence or friction:
Would repeat without coaching: yes | no
Optional public-safe receipt or screenshot:
```

Concrete rejection is useful evidence. Generic approval, stars, clones, and a
passing command do not count as product validation.

After release, the same outcome can be submitted through the
`Captured Proof real-change trial` issue form.
