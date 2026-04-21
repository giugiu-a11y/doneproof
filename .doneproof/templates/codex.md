# DoneProof for Codex

Before final response:

1. Run the relevant verification command.
2. Create or update a DoneProof receipt.
3. Use `awaiting_review`, not `done`.
4. Mention residual risks honestly.

Required command:

```bash
doneproof check --receipt .doneproof/receipts/latest.json
```

Recommended receipt command:

```bash
doneproof new \
  --task "<task>" \
  --changed-file "<path>" \
  --command "passed:<command>" \
  --evidence "test:<what passed>" \
  --risk "<known remaining risk>"
```
