# Launch Plan

Status: ready for manual social posting.

## Goal

Make DoneProof easy to understand in one minute and easy to try in five minutes.

## Current Public State

- Public repo: https://github.com/giugiu-a11y/doneproof
- Current release: `v0.4.0`
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

- 10+ stars from people outside the immediate circle;
- one real issue or feature request from an external user;
- one external repo trying the GitHub Action;
- one clear request that shapes `v0.5.0`.

## Next Public Repo Candidate

Start the second piece only after external signal. The strongest candidate is a project guard extracted from the same operating lesson:

> Agents should prove they are editing the right project before they edit files.

Do not create that repo until the scope is smaller than the idea.
