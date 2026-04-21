# Policy Presets

DoneProof policies should be small enough to audit in a review.

Copy one of these examples into `.doneproof/policy.yml` and adjust it for the repository:

```text
examples/policies/solo.yml
examples/policies/team.yml
examples/policies/ci-gated.yml
```

## Solo

Use `solo.yml` when one agent or one developer is producing a receipt before human review.

It requires one changed file, one command, one evidence item, and honest residual risks.

## Team

Use `team.yml` when multiple people or agents may continue the work.

It keeps the same review language but asks for at least two evidence items so the handoff is easier to continue.

## CI-Gated

Use `ci-gated.yml` when pull requests should fail without a stronger receipt.

It asks for at least two commands and two evidence items. It is a better fit for repositories where agent-authored PRs need a review trail in CI.
