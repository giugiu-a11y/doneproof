# Contributing

Thanks for helping make AI coding work easier to verify. You do not need to know the whole project to contribute.

## Start Here

1. Check the [open issues](https://github.com/giugiu-a11y/doneproof/issues) for a small problem you understand.
2. Leave a short comment on the issue before starting a large change. This helps avoid duplicate work.
3. Fork the repository and create a focused branch.
4. Make the smallest change that solves the problem.
5. Run the checks below and open a pull request explaining what changed and what still needs review.

Good first contributions include clearer examples, better error messages, documentation fixes, and focused test cases. If your idea adds telemetry, a required cloud service, or broad agent orchestration, it is outside the current project direction.

## Project Rules

Contributions should follow these rules:

- keep examples anonymous;
- add tests for policy or receipt behavior changes;
- avoid telemetry by default;
- never require cloud services for core checks;
- prefer explicit failure messages over clever automation.

## Local Development

```bash
git clone https://github.com/YOUR-USERNAME/doneproof.git
cd doneproof
python3 -m pip install --upgrade pip
python3 -m pip install -e ".[dev]"
make check
make prepublish
```

Use `make check` while working. Run `make prepublish` before a release-facing pull request; it also builds and validates the installable package.

## Pull Request Standard

Every pull request should include:

- a clear problem statement;
- tests for behavior changes;
- a sanitized DoneProof receipt when agent work was involved;
- known risks or skipped checks.

Small pull requests are easier to review. Keep unrelated cleanup in a separate change.

## Scope

Good contributions improve:

- receipt validation;
- policy clarity;
- agent handoffs;
- local-first setup;
- documentation and examples.

Avoid adding:

- telemetry;
- cloud-only workflows;
- provider-specific secrets;
- dashboards before the CLI is solid;
- broad agent orchestration inside the core package.
