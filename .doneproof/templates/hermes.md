# DoneProof for Hermes-Style Orchestrators

Use this template for orchestrator agents that delegate work to other agents.

Rules:

1. Do not collapse delegate reports into "done".
2. Require the worker receipt before summarizing the handoff.
3. Preserve runtime/provider boundaries; receipts describe work evidence, not secrets or model routes.
4. Final orchestrator status should be `awaiting_review`, `blocked`, or `failed`.

Required check:

```bash
doneproof check --receipt .doneproof/receipts/latest.json
```
