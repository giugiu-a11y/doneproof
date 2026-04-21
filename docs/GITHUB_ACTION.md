# GitHub Action

DoneProof includes a composite action for public use.

```yaml
name: DoneProof

on:
  pull_request:

jobs:
  receipt:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: giugiu-a11y/doneproof@v0.4.0
        with:
          receipt: .doneproof/receipts/latest.json
```

The repository also includes `.github/workflows/action-smoke.yml`, which verifies the composite action in GitHub Actions.

## Policy

The action should fail when:

- the receipt is missing;
- status uses completion language such as `done`;
- commands, changed files, or evidence are missing;
- the receipt violates the local `.doneproof/policy.yml`.

## Security

Do not paste secrets into receipts. The action treats receipts as review artifacts and they may appear in CI logs.

## Receipt Badge

DoneProof can generate a compact Markdown badge for PR descriptions or CI comments:

```bash
doneproof badge --format markdown
```

For CI adapters, use JSON output instead of parsing terminal text:

```bash
doneproof report --format json
doneproof badge --format json
```

## PR Comment Example

Copy this workflow when reviewers need the receipt summary directly on the pull request:

```text
docs/examples/github-pr-comment.yml
```

The workflow uses only GitHub Actions primitives and the default workflow token. It updates one bot comment per PR and still fails the job when the receipt is invalid.
