# Cursor Integration

Use DoneProof when Cursor makes multi-file or agent-assisted changes.

## Add To Rules

Copy `.doneproof/templates/cursor.md` into your project rules.

## Recommended Rule

```text
When changing code, do not claim completion until doneproof check passes.
If no verification was run, record that as a risk.
```

## Check

```bash
doneproof check --receipt .doneproof/receipts/latest.json
```
