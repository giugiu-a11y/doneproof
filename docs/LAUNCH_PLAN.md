# Launch Plan

Status: technical launch prerequisites are present; external distribution has not been executed.

## Goal

Make DoneProof easy to understand in one minute and easy to try in five minutes.

## Current Public State

- Public repo: https://github.com/giugiu-a11y/doneproof
- Current release: `v0.5.0`
- GitHub install path works from the public tag.
- CI and Action Smoke are required on `main`.
- Secret scanning and push protection are enabled.
- Open issue backlog is intentionally small and public.

## Audience

- developers using Codex, Claude Code, Cursor, Aider, Cline, or OpenCode;
- teams using OpenClaw-style local agents or Hermes-style orchestrators;
- founders letting agents touch multiple repos;
- maintainers reviewing agent-authored pull requests;
- small teams that need lightweight handoff discipline.

## GitHub-Native Launch Order

1. Keep DoneProof and the profile README pinned; do not pin empty or private placeholders.
2. Confirm the social preview, description, topics, release, badges, and install command in a logged-out browser.
3. Record the baseline: views, unique visitors, clones, stars, issues, discussions, and external repositories using the Action.
4. Publish one short post manually using `docs/LAUNCH_COPY.md`.
5. Watch replies for confusion around "does it prove correctness?" or "why not PyPI?"
6. Fix README/docs if the same confusion appears twice.
7. Publish the longer version only after one outside person completes the install path.
8. Compare the same metrics after 24 hours and 7 days; count confirmed use separately from traffic.

## What To Watch

- Do people understand the problem without a call?
- Can they install it from GitHub?
- Do they ask for PyPI?
- Do they ask for richer command evidence?
- Do they use the GitHub Action?
- Do they star it because the idea is sharp, or only because they know us?

## Do Not Do Yet

- Do not publish to PyPI before install feedback.
- Do not turn it into a dashboard.
- Do not add telemetry.
- Do not claim it verifies correctness.
- Do not post private system details as origin story.
- Do not launch a second repo before DoneProof gets at least one real external signal.

## Success Signals

- one confirmed external user completes the clean-install path;
- one real issue or feature request comes from an external workflow;
- one external repository tries the GitHub Action;
- one clear request shapes the next release.

Stars, views and clones are useful telemetry, but they do not count as confirmed adoption.

## Baseline Before Distribution

Capture exact values immediately before the first post. Keep the distinction explicit:

- `traffic`: views, unique visitors, clones, stars;
- `interest`: a substantive issue, discussion, or reply from someone outside the project;
- `adoption`: a confirmed clean install or an external repository using the Action;
- `retention`: the same user returns or uses DoneProof on a second change.

Never describe clones or stars as users unless a person or repository confirms actual use.

## New Repository Gate

Do not create another public product repo until DoneProof has at least three confirmed external users, one qualified integration, one accepted upstream contribution, and two consecutive weekly cycles with product, demo, note, distribution, upstream and review evidence.
