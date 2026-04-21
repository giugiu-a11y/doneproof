# Codex Integration

Use DoneProof as the final handoff gate for Codex work.

## Install

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -e .
doneproof init
```

## Add To Repo Instructions

Copy `.doneproof/templates/codex.md` into the repo's agent instructions.

Minimum final-flow instruction:

```text
Before final response, create or update .doneproof/receipts/latest.json and run doneproof check.
Use awaiting_review for successful work. Do not say the work is approved.
```

## Typical Flow

```bash
doneproof new \
  --task "Implement the requested change" \
  --changed-file "src/example.py" \
  --command "passed:python3 -m pytest" \
  --evidence "test:pytest passed" \
  --risk "No browser review needed"

doneproof check
doneproof report
```
