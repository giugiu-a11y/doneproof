# Receipt Examples

- `passing.json`: minimum valid receipt.
- `failing.json`: intentionally invalid receipt used to test failure behavior.

Use:

```bash
PYTHONPATH=src python3 -m doneproof check --root . --receipt examples/receipts/passing.json
PYTHONPATH=src python3 -m doneproof check --root . --receipt examples/receipts/failing.json
```

