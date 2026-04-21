# OpenCode Integration

Use DoneProof as a delivery receipt for OpenCode tasks.

## Add To Agent Instructions

Copy `.doneproof/templates/opencode.md` into your OpenCode project instructions.

## Expected Handoff

OpenCode should leave:

- changed file list;
- verification commands;
- evidence;
- risks;
- `awaiting_review` status.

Run:

```bash
doneproof check
```
