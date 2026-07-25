# Captured Proof Demo

This demo is generated from the product's real execution path. It is not a
concept animation with invented terminal output.

- animated demo: `docs/assets/doneproof-demo.gif`
- static poster: `docs/assets/doneproof-demo-poster.png`
- accessible SVG fallback: `docs/assets/doneproof-demo.svg`
- real isolated flow: `scripts/captured_proof_demo.py`
- real-run renderer: `scripts/render_demo_gif.py`

## What The Demo Proves

The script:

1. creates an isolated Git repository;
2. initializes DoneProof and commits a clean baseline;
3. changes `README.md`;
4. executes a real check through `doneproof capture`;
5. writes a receipt with exit code, duration, sanitized output digest, and
   content-derived Git-scope digest;
6. runs `doneproof check` and `doneproof schema-check`;
7. fails unless every step succeeds.

On 2026-07-25, the run embedded in the demo completed the entire flow in `0.42`
seconds on the development machine. Treat that as a receipt for this run, not a
universal benchmark.

## Reproduce It

Requires Python 3.10+ and `uv`.

```bash
uv sync --extra dev --frozen
uv run --frozen --extra dev python scripts/captured_proof_demo.py
```

The final line must be:

```text
DEMO_RESULT=PASS
```

Regenerate the visual assets from a fresh real run:

```bash
uv run --frozen --extra dev python scripts/render_demo_gif.py
```

The renderer prints the generated paths and measured execution time. Review the
GIF and poster visually after regeneration; file creation alone does not prove
legibility.

## What Is Stored

The receipt stores:

- sanitized command text;
- result, exit code, timeout state, and duration;
- SHA-256 of the sanitized output plus byte and line counts;
- SHA-256 of the selected Git patch and untracked file bytes;
- privacy-safe changed paths;
- operating system, architecture, and Python version;
- an integrity digest over the complete Captured Proof object.

It does not store raw command output or Git diff content.

## Trust And Privacy Boundary

Known credential shapes and local home paths are masked before command output is
shown or hashed. Redaction is defense in depth, not a mathematical guarantee
against every possible secret format.

The integrity digest makes internal mutations detectable, but it is not a
signature or remote attestation. Someone who can edit the receipt can also
recompute an unsigned digest. DoneProof still requires review of the real code,
diff, and repository controls.

Captured Proof is an unreleased `v0.6` candidate. The public release remains
`v0.5.0` until privacy, external maintainer feedback, and release gates close.
