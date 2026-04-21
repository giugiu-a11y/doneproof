# Hermes-Style Orchestrator Integration

Use this guide for orchestrator agents that delegate work to other agents or workers.

DoneProof should make orchestration handoffs auditable without mixing runtime ownership.

## Rules

- The worker should produce the receipt whenever possible.
- The orchestrator should not translate a worker's `awaiting_review` into a completion claim.
- Receipts should include work evidence, not model/provider credentials or runtime routes.
- If delegation failed, use `blocked` or `failed` and explain the risk.

## Template

Copy:

```text
.doneproof/templates/hermes.md
```

## Orchestrator Handoff Checklist

- Did the worker list changed files?
- Did the worker list commands?
- Did the worker preserve evidence?
- Did the worker include risks?
- Did `doneproof check` pass?

If any answer is no, the handoff is not ready for owner review.
