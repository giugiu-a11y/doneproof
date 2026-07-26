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

## Positioning

Category: local check evidence for AI code changes.

Core promise:

> Run the check you already trust. Review what actually ran and which current
> Git change it covered.

The entry wedge is deliberately narrow: one existing command becomes a
reviewable receipt without requiring an account, agent integration, policy
file, CI change, hosted control plane, or cryptographic claim.

This is not an AI code reviewer, agent runtime, policy engine, signed
attestation system, CI replacement, or proof that code is correct. Broader
products already serve those categories. Market validation must prove that the
smaller activation surface is valuable on its own.

## Activation Event

A design partner brings one authorized, public-safe, agent-authored change and
one real repository check. The maintainer runs the command in a repository they
control; the first trial may be guided and requires no product integration.

The maintainer:

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
4. Offer a guided five-minute trial using `docs/VALIDATION_TRIAL.md`; keep a
   self-serve path for maintainers who prefer it.
5. Ask the maintainer to run it on one real change and report the review
   effect, missing evidence, competitive alternative, and repeat intent.
6. Confirm one repeat use without coaching.
7. Repeat the privacy and release review on the exact candidate.
8. Keep the approved naming architecture frozen: `DoneProof` as the current
   compatibility identifier, `Captured Proof` as the mechanism, and no
   umbrella brand.
9. Publish `v0.6.0` only after owner approval.
10. Use one public channel first, learn from replies, then adapt the next
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
- If two maintainers independently prefer CI or an existing proof/review tool,
  treat that as competitive rejection: revise the handoff use case or stop the
  release instead of adding features blindly.
- If privacy concerns block sharing, improve the share boundary before adding
  richer evidence.
- If external users run it once but do not repeat, investigate the review
  moment and integration surface; do not manufacture a suite.
- Add PyPI only when public install friction is observed and the readiness gate
  is satisfied.

## Naming Decision

`DoneProof` has an active exact-name collision outside developer tools and a
same-category public repository collision. It therefore remains the current
repository, package, and CLI compatibility identifier, not a future master
brand.

- Keep the current identifiers stable through validation so the public
  candidate remains reproducible.
- Lead with the category `Local check evidence for AI code changes` and the
  mechanism `Captured Proof`, not the repository name.
- Do not create an umbrella brand or reopen a rename before external repeat
  use proves that a broader architecture is needed.
- If evidence later justifies a replacement, it must pass exact-name searches
  across developer repositories, package registries, current web products, and
  relevant domains before an atomic migration is planned.
- Availability screening is not trademark or legal clearance.

## Scope Discipline

- Captured Proof is the named acquisition mechanism inside DoneProof.
- Do not partially rename the repository, package, CLI, documentation, or
  release artifacts before the owner approves one atomic migration.
- Continuity Loop and Memory Boundary are independent products.
- Do not create another public repository, dashboard, telemetry layer, hosted
  service, or paid infrastructure to compensate for missing adoption.

## Current Public State

- Repository: https://github.com/giugiu-a11y/doneproof
- Stable release: `v0.5.0`
- Captured Proof: unreleased public draft in pull request #35
- Release truth: engineering evidence can qualify the candidate, but only
  external use can qualify the market claim.
