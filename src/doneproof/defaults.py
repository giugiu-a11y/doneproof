"""Default policy and template content."""

from __future__ import annotations

DEFAULT_POLICY = {
    "schema_version": "1.0",
    "status": {
        "allowed": ["awaiting_review", "blocked", "failed"],
        "forbidden": ["done", "complete", "completed", "validated", "100%", "pronto"],
    },
    "required_fields": [
        "task",
        "status",
        "summary",
        "changed_files",
        "commands",
        "evidence",
        "risks",
    ],
    "minimums": {
        "changed_files": 1,
        "commands": 1,
        "evidence": 1,
    },
    "claims": {
        "forbidden_phrases": [
            "100%",
            "fully validated",
            "validated",
            "complete",
            "completed",
            "done",
            "pronto",
            "funcionando perfeitamente",
        ]
    },
}

TEMPLATES = {
    "codex.md": """# DoneProof for Codex

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
doneproof new \\
  --task "<task>" \\
  --changed-file "<path>" \\
  --command "passed:<command>" \\
  --evidence "test:<what passed>" \\
  --risk "<known remaining risk>"
```
""",
    "claude.md": """# DoneProof for Claude

No proof, no done.

Before final response, provide a receipt with:

- changed files;
- commands run;
- evidence;
- risks;
- status `awaiting_review`, `blocked`, or `failed`.

Run before final response:

```bash
doneproof check --receipt .doneproof/receipts/latest.json
```
""",
    "cursor.md": """# DoneProof for Cursor

When making code changes, do not mark work complete until a DoneProof receipt passes.

Use:

```bash
doneproof check --receipt .doneproof/receipts/latest.json
```
""",
    "opencode.md": """# DoneProof for OpenCode

Every task needs a delivery receipt.

Allowed final statuses:

- awaiting_review
- blocked
- failed

Avoid absolute claims unless backed by receipt evidence.
""",
    "openclaw.md": """# DoneProof for OpenClaw-Style Local Agents

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
""",
    "hermes.md": """# DoneProof for Hermes-Style Orchestrators

Use this template for orchestrator agents that delegate work to other agents.

Rules:

1. Do not collapse delegate reports into "done".
2. Require the worker receipt before summarizing the handoff.
3. Preserve runtime/provider boundaries; receipts describe work evidence,
   not secrets or model routes.
4. Final orchestrator status should be `awaiting_review`, `blocked`, or `failed`.

Required check:

```bash
doneproof check --receipt .doneproof/receipts/latest.json
```
""",
    "aider.md": """# DoneProof for Aider

Before asking for human review:

1. Ensure the changed files are listed in the receipt.
2. Record the command that verified the change.
3. Record evidence and risks.
4. Run:

```bash
doneproof check --receipt .doneproof/receipts/latest.json
```
""",
    "cline.md": """# DoneProof for Cline

Before marking a task ready:

1. Create or update `.doneproof/receipts/latest.json`.
2. Use `awaiting_review`, not a completion claim.
3. Include changed files, commands, evidence, and risks.
4. Run:

```bash
doneproof check --receipt .doneproof/receipts/latest.json
```
""",
}
