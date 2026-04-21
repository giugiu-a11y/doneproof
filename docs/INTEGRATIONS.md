# Integrations

DoneProof works with any agent that can read repository instructions and run a shell command.

The integration contract is intentionally small:

1. the agent writes or updates `.doneproof/receipts/latest.json`;
2. the agent runs `doneproof check`;
3. the agent reports `awaiting_review`, `blocked`, or `failed`;
4. the agent keeps provider, token, runtime, and customer details out of the receipt.

## Quick Setup

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -e .
doneproof init
```

Then copy the matching file from:

```text
.doneproof/templates/
```

## Supported Templates

| Agent | Template | Guide |
| --- | --- | --- |
| Codex | `.doneproof/templates/codex.md` | `docs/integrations/CODEX.md` |
| Claude Code | `.doneproof/templates/claude.md` | `docs/integrations/CLAUDE.md` |
| Cursor | `.doneproof/templates/cursor.md` | `docs/integrations/CURSOR.md` |
| OpenCode | `.doneproof/templates/opencode.md` | `docs/integrations/OPENCODE.md` |
| OpenClaw-style local agents | `.doneproof/templates/openclaw.md` | `docs/integrations/OPENCLAW.md` |
| Hermes-style orchestrators | `.doneproof/templates/hermes.md` | `docs/integrations/HERMES.md` |
| Aider | `.doneproof/templates/aider.md` | `docs/integrations/AIDER.md` |
| Cline | `.doneproof/templates/cline.md` | `docs/integrations/CLINE.md` |

## Safe Integration Rules

- Receipts should describe work evidence, not secret infrastructure.
- Do not paste API keys, access tokens, model credentials, browser cookies, or local runtime URLs.
- Keep project-specific private paths out of public examples.
- For orchestrators, require the worker's receipt before summarizing the result.
- For local agent runtimes, preserve runtime boundaries; DoneProof verifies work handoff, not provider health.

## Minimal Receipt Flow

```bash
doneproof new \
  --task "Describe the task" \
  --changed-file README.md \
  --command "passed:python3 -m pytest" \
  --evidence "test:pytest passed" \
  --risk "Manual browser review not performed"

doneproof check
doneproof report
```

## CI Flow

For pull requests created by agents, add a receipt to the branch and run:

```bash
doneproof check --receipt .doneproof/receipts/latest.json
```

The included composite action is documented in `docs/GITHUB_ACTION.md`.
