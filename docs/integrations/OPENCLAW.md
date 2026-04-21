# OpenClaw-Style Local Agent Integration

Use this guide for local agent runtimes that coordinate tools, models, and project workspaces.

DoneProof should verify the work handoff. It should not expose runtime internals.

## Rules

- Keep provider names, tokens, bridge URLs, browser cookies, and local runtime paths out of receipts.
- Keep receipts repo-relative.
- Use `awaiting_review` when the agent has produced evidence but a human has not approved it.
- Run `doneproof doctor` during setup and `doneproof check` before handoff.

## Template

Copy:

```text
.doneproof/templates/openclaw.md
```

## Handoff Flow

```bash
doneproof new \
  --task "Agent task" \
  --changed-file "README.md" \
  --command "passed:python3 -m pytest" \
  --evidence "test:pytest passed" \
  --risk "Manual review still required"

doneproof check
```
