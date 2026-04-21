# Editor Tasks

Run the receipt loop from the editor instead of remembering commands.

## VS Code

Copy:

```text
docs/examples/vscode-tasks.json
```

Into:

```text
.vscode/tasks.json
```

Tasks included:

- `DoneProof: check receipt`
- `DoneProof: report receipt`
- `DoneProof: create receipt draft`

## Cursor

Cursor can run the same VS Code task file.

For agent behavior, copy:

```text
docs/examples/cursor-doneproof-rule.mdc
```

Into:

```text
.cursor/rules/doneproof.mdc
```

Keep the rule focused: create the receipt, run the check, report `awaiting_review`, and leave approval to the reviewer.
