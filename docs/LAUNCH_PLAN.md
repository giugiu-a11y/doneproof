# Launch Plan

Status: ready after the `v0.5.0` tag and clean-install smoke pass.

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

## Launch Order

1. Post one short X/LinkedIn version manually.
2. Watch comments for confusion around "does it prove correctness?" or "why not PyPI?"
3. Fix README/docs if the same confusion appears twice.
4. Post the longer LinkedIn version after the short post lands.
5. Use Hacker News or Reddit only after one outside person confirms the README is clear.

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

## New Repository Gate

Do not create another public product repo until DoneProof has at least three confirmed external users, one qualified integration, one accepted upstream contribution, and two consecutive weekly cycles with product, demo, note, distribution, upstream and review evidence.
