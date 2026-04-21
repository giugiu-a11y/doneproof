# Claude Code Integration

Use DoneProof to keep Claude Code handoffs explicit and reviewable.

## Add To Instructions

Copy `.doneproof/templates/claude.md` into `CLAUDE.md` or your project-specific Claude instructions.

## Required Final Gate

```bash
doneproof check --receipt .doneproof/receipts/latest.json
```

Claude should summarize:

- changed files;
- commands run;
- evidence;
- residual risks;
- receipt status.

The status should stay `awaiting_review` until a human approves the work.
