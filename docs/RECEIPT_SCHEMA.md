# Receipt Schema

V0.1 receipts are JSON objects.

Machine-readable schema:

```text
schemas/receipt.schema.json
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
