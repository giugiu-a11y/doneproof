# Launch Plan

Status: release candidate in public draft review; market validation active;
release and distribution not yet approved.

## Goal

Prove that Captured Proof reduces review ambiguity for maintainers handling
AI-authored code changes. The goal is external use, not impressions.

## Primary User

A repository maintainer or senior reviewer who receives an agent-authored
change and needs to answer:

> What check actually ran against this Git change, and what still requires
> human review?

Other agent users may benefit, but they are not the launch audience until the
maintainer workflow is proven.

## Activation Event

A new user:

1. installs the candidate during validation, or the public release after
   approval;
2. runs one real check with `doneproof capture`;
3. validates the receipt with `doneproof check` and `doneproof schema-check`;
4. shares or reviews the receipt against the same Git change;
5. understands that the result is `awaiting_review`, not approval.

The public demonstration must show this loop in less than 60 seconds.

## Distribution Sequence

1. Talk directly with five maintainers who already review agent-authored
   changes.
2. Record concrete pain, objections, and workflow constraints; an invitation
   alone does not count as feedback.
3. Send at most one follow-up in the documented window.
4. Ask the maintainer to use `docs/VALIDATION_TRIAL.md` on one real change and
   report the review effect, missing evidence, and repeat intent.
5. Confirm one repeat use without coaching.
6. Repeat the privacy and release review on the exact candidate.
7. Publish `v0.6.0` only after owner approval.
8. Use one public channel first, learn from replies, then adapt the next
   channel.

## Advancement Gates

All are required before a public launch:

- at least two of five maintainers confirm the review pain with workflow-level
  detail;
- at least one external real-change receipt is produced and reviewed;
- at least one external user repeats the workflow;
- the exact release diff, assets, install path, and required checks pass;
- the owner approves the release and first distribution post.

Stars, views, clones, invitations, and friendly compliments are telemetry. They
do not count as adoption.

## Decision Rules

- If maintainers understand the pain but do not run the workflow, reduce
  activation friction before adding features.
- If two maintainers independently reject the receipt as redundant with their
  CI, revise the handoff use case or stop the release.
- If privacy concerns block sharing, improve the share boundary before adding
  richer evidence.
- If external users run it once but do not repeat, investigate the review
  moment and integration surface; do not manufacture a suite.
- Add PyPI only when public install friction is observed and the readiness gate
  is satisfied.

## Scope Discipline

- Captured Proof is the named acquisition mechanism inside DoneProof.
- DoneProof remains the existing repository name, not a proposed umbrella
  brand.
- Continuity Loop and Memory Boundary are independent products.
- Do not create another public repository, dashboard, telemetry layer, hosted
  service, or paid infrastructure to compensate for missing adoption.

## Current Public State

- Repository: https://github.com/giugiu-a11y/doneproof
- Stable release: `v0.5.0`
- Captured Proof: unreleased public draft in pull request #35
- Release truth: engineering evidence can qualify the candidate, but only
  external use can qualify the market claim.
