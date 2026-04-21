# Architecture

DoneProof is intentionally small.

## Components

- `src/doneproof/cli.py`: parses commands and prints human or JSON output.
- `src/doneproof/policy.py`: loads `.doneproof/policy.yml` and creates project defaults.
- `src/doneproof/defaults.py`: stores the default policy and agent templates.
- `src/doneproof/receipt.py`: validates evidence, status, commands, changed files, and forbidden claims.
- `src/doneproof/doctor.py`: checks local setup.
- `src/doneproof/git.py`: discovers changed files as a convenience helper.

## Stack

- Python `>=3.10`.
- `setuptools` package build with `src/` layout.
- PyYAML for local policy parsing.
- pytest for tests.
- ruff for lint.
- GitHub Actions for CI after publication.

## Design Principles

- Local-first.
- No telemetry.
- No cloud dependency.
- Evidence over confidence.
- Review language over completion language.
- Clear failure messages.

## Trust Model

DoneProof does not prove the agent is correct. It proves whether the agent produced the minimum evidence required by policy.

The human reviewer still owns approval.

## Non-Goals

- no hosted service;
- no database;
- no daemon;
- no model/provider integration;
- no token or log collection;
- no automatic approval of agent work.

## Extension Points

- policy fields in `.doneproof/policy.yml`;
- agent templates in `.doneproof/templates/`;
- receipt schema in `schemas/receipt.schema.json`;
- composite action in `action.yml`;
- integration guides in `docs/integrations/`.
