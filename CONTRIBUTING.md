# Contributing

Contributions should follow these rules:

- keep examples anonymous;
- add tests for policy or receipt behavior changes;
- avoid telemetry by default;
- never require cloud services for core checks;
- prefer explicit failure messages over clever automation.

## Local Development

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -e ".[dev]"
make check
make prepublish
```

## Pull Request Standard

Every pull request should include:

- a clear problem statement;
- tests for behavior changes;
- a sanitized DoneProof receipt when agent work was involved;
- known risks or skipped checks.

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
