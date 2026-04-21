# Demo

The README uses `docs/assets/doneproof-demo.gif` as the primary visual demo.

- animated demo: `docs/assets/doneproof-demo.gif`
- static fallback: `docs/assets/doneproof-demo.svg`
- generator: `scripts/render_demo_gif.py`

The GIF walks through the strongest public flow:

1. initialize DoneProof in a repo;
2. create a sanitized git diff evidence artifact;
3. fail a weak receipt;
4. pass a receipt with evidence;
5. show the handoff in report form.

The same commands are listed below as a text reference.

## Passing Receipt

```bash
doneproof --version
doneproof check --receipt examples/receipts/passing.json
```

Expected:

```text
DoneProof: PASS
```

## Failing Receipt

```bash
doneproof check --receipt examples/receipts/failing.json
```

Expected:

```text
DoneProof: FAIL
error: Forbidden status: done
error: changed_files needs at least 1 item(s)
error: commands needs at least 1 item(s)
error: evidence needs at least 1 item(s)
```

## Create A Receipt Draft

```bash
doneproof new \
  --task "Add health check endpoint" \
  --changed-file app/main.py \
  --command "passed:pytest tests/test_health.py" \
  --evidence "test:pytest tests/test_health.py passed" \
  --risk "Manual browser check not performed"
```

Then:

```bash
doneproof check
doneproof report
```

## Add Git Diff Evidence

```bash
doneproof evidence git-diff
```

Expected:

```text
created: .doneproof/evidence/git-diff-summary.txt
```

The summary records changed paths and addition/deletion counts. Full diff content is intentionally omitted so receipts stay reviewable without becoming a secret sink.
