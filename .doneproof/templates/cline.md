# DoneProof for Cline

Before marking a task ready:

1. Create or update `.doneproof/receipts/latest.json`.
2. Use `awaiting_review`, not a completion claim.
3. Include changed files, commands, evidence, and risks.
4. Run:

```bash
doneproof check --receipt .doneproof/receipts/latest.json
```
