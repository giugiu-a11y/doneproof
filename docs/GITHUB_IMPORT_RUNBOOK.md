# GitHub Import Runbook

Status: completed for `giugiu-a11y/doneproof`; keep as the repeatable import reference.

This repo was prepared so publication could be a short operational step after approval. Future projects in this line should reuse this runbook.

## Pre-Approval State

Expected local state before publication:

- public files committed locally;
- local governance files ignored;
- `.doneproof/receipts/latest.json` ignored;
- `uv.lock` and dependency update configs tracked;
- `make prepublish` passes;
- release-readiness only blocks on missing remote;
- README and examples contain no private paths, names, logs, tokens, or internal codenames.

## Import Steps After Approval

Use placeholders until the final owner and repo name are approved.

```bash
git status --short --ignored
make prepublish
git remote add origin https://github.com/<owner>/<repo>.git
git push -u origin main
```

If creating the repo with GitHub CLI is approved:

```bash
gh repo create <owner>/<repo> --public --source=. --remote=origin --push
```

## First GitHub Checks

After the first push:

1. confirm the default branch is `main`;
2. confirm the CI workflow runs;
3. confirm issue templates render correctly;
4. open the README on GitHub and verify formatting;
5. run the composite action in a private fixture before recommending it publicly;
6. create release `v0.1.0` only after CI passes.

## Do Not Publish A Future Repo If

- `make prepublish` fails;
- public hygiene scan finds private markers;
- CI is not configured;
- the README promises behavior not implemented;
- the action has not been tested in GitHub Actions;
- the owner has not approved launch copy.
