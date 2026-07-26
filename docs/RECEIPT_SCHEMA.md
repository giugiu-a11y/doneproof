# Receipt Schema

DoneProof receipts are JSON objects. The stable schema identifier remains
`urn:doneproof:schema:receipt:1.0`; Captured Proof is an optional, additive
object with its own `version: "1.0"`.

Machine-readable schema:

```text
schemas/receipt.schema.json
```

The bundled schema uses the stable identifier `urn:doneproof:schema:receipt:1.0` and does not depend on a hosted schema endpoint.

Validate a receipt against the schema:

```bash
doneproof schema-check --receipt .doneproof/receipts/latest.json
```

For automation output:

```bash
doneproof schema-check --receipt .doneproof/receipts/latest.json --json
```

## Required Fields

```json
{
  "task": "Short task description",
  "status": "awaiting_review",
  "summary": "What changed and what was verified.",
  "changed_files": ["README.md"],
  "commands": [
    {
      "cmd": "python3 -m pytest",
      "status": "passed"
    }
  ],
  "evidence": [
    {
      "type": "test",
      "value": "python3 -m pytest passed"
    }
  ],
  "risks": ["Manual browser verification not performed"]
}
```

`changed_files`, `commands`, and `evidence` must each contain at least one item.
`task`, `summary`, command `cmd`, evidence `type`, and evidence `value` must not be empty.

## Captured Proof Object

Receipts created by the unreleased `doneproof capture` candidate also contain:

```json
{
  "captured_proof": {
    "version": "1.0",
    "captured_at": "2026-07-25T15:30:00+00:00",
    "command": "python3 verify_agent_change.py",
    "result": "passed",
    "exit_code": 0,
    "duration_ms": 20,
    "timed_out": false,
    "output": {
      "sha256": "sha256:<64 lowercase hexadecimal characters>",
      "bytes": 25,
      "lines": 1,
      "content_stored": false,
      "redactions": 0,
      "redaction_status": "not_detected"
    },
    "command_redactions": 0,
    "git_scope": {
      "mode": "all",
      "sha256": "sha256:<64 lowercase hexadecimal characters>",
      "changed_files": ["README.md"],
      "content_stored": false
    },
    "environment": {
      "os": "Darwin",
      "architecture": "arm64",
      "python": "3.12.10"
    },
    "integrity_sha256": "sha256:<64 lowercase hexadecimal characters>"
  }
}
```

The validator binds the proof to exactly one command marked
`"captured": true`. Command text, result, exit code, duration, and output digest
must match across both structures. The receipt status must be
`awaiting_review` for exit code `0` and `failed` for a nonzero exit code.

`integrity_sha256` is calculated over a canonical JSON encoding of the Captured
Proof object without the integrity field itself. It detects internal mutation;
it is not a digital signature or remote attestation.

Raw output and raw Git content are forbidden in this object. `content_stored`
must be `false` for both output and Git scope. The only allowed environment
fields are `os`, `architecture`, and `python`.

## Status Values

Allowed by default:

- `awaiting_review`
- `blocked`
- `failed`

Forbidden by default:

- `done`
- `complete`
- `completed`
- `validated`
- `100%`
- `pronto`

## Command Status Values

- `passed`
- `failed`
- `skipped`

Skipped commands should include a `reason`.

## Path Safety

`changed_files` must use repo-relative paths.

Rejected examples:

- absolute paths;
- `..` parent traversal;
- Windows-style backslash traversal;
- home-directory paths starting with `~`.

## Create A Draft

```bash
doneproof new \
  --task "Add health check endpoint" \
  --changed-file app/main.py \
  --command "passed:pytest tests/test_health.py" \
  --evidence "test:pytest tests/test_health.py passed" \
  --risk "Manual browser check not performed"
```
