# DoneProof for OpenClaw-Style Local Agents

Use this template for local agent runtimes that can read repository instructions.

Rules:

1. Work inside the active repository only.
2. Keep runtime/provider details out of receipts.
3. Record changed files, commands, evidence, and residual risks.
4. Use `awaiting_review` for successful agent work.

Required check:

```bash
doneproof check --receipt .doneproof/receipts/latest.json
```
