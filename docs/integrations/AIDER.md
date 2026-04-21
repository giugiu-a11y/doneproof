# Aider Integration

Use DoneProof after Aider changes files.

## Recommended Flow

```bash
doneproof new \
  --task "Aider task" \
  --changed-file "path/to/file.py" \
  --command "passed:python3 -m pytest" \
  --evidence "test:pytest passed" \
  --risk "Manual review still required"

doneproof check
```

Keep the final status as `awaiting_review`.
