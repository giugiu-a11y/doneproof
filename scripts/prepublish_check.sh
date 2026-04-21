#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
RM_BIN="${RM_BIN:-rm}"
PYTHON_BIN="${PYTHON_BIN:-$(command -v python3.12 || command -v python3.11 || command -v python3.10 || command -v python3)}"

"$PYTHON_BIN" - <<'PY'
import sys

if sys.version_info < (3, 10):
    raise SystemExit("DoneProof prepublish checks require Python 3.10+.")
PY

UV_RUN=(uv run --extra dev --python "$PYTHON_BIN")

"$RM_BIN" -rf \
  /tmp/doneproof-smoke \
  /tmp/doneproof-installed-smoke \
  /tmp/doneproof-install-venv \
  /tmp/doneproof-dev-venv \
  /tmp/doneproof-build-check \
  /tmp/doneproof-wheel \
  /tmp/doneproof-wheel-venv
"$RM_BIN" -rf build src/doneproof.egg-info .pytest_cache .ruff_cache
find src tests -type d -name __pycache__ -prune -exec "$RM_BIN" -rf {} +

"${UV_RUN[@]}" ruff check .
"${UV_RUN[@]}" pytest
"${UV_RUN[@]}" python -m compileall -q src tests

"${UV_RUN[@]}" doneproof init --root /tmp/doneproof-smoke
git -C /tmp/doneproof-smoke init -b main >/dev/null
printf '# Smoke\n' > /tmp/doneproof-smoke/README.md
"${UV_RUN[@]}" doneproof doctor --root /tmp/doneproof-smoke
"${UV_RUN[@]}" doneproof evidence git-diff --root /tmp/doneproof-smoke
"${UV_RUN[@]}" doneproof new \
  --root /tmp/doneproof-smoke \
  --task "Smoke task" \
  --changed-file README.md \
  --command "passed:echo ok" \
  --evidence "smoke:echo ok" \
  --risk "Example only"
"${UV_RUN[@]}" doneproof check --root /tmp/doneproof-smoke

"${UV_RUN[@]}" doneproof check --root . --receipt examples/receipts/passing.json
"${UV_RUN[@]}" doneproof schema-check --root . --receipt examples/receipts/passing.json
if "${UV_RUN[@]}" doneproof check --root . --receipt examples/receipts/failing.json >/tmp/doneproof-failing-check.log 2>&1; then
  echo "Expected failing fixture to fail" >&2
  exit 1
fi
if "${UV_RUN[@]}" doneproof schema-check --root . --receipt examples/receipts/failing.json >/tmp/doneproof-failing-schema-check.log 2>&1; then
  echo "Expected failing fixture to fail schema check" >&2
  exit 1
fi
if [[ -f .doneproof/receipts/latest.json ]]; then
  "${UV_RUN[@]}" doneproof check --root . --receipt .doneproof/receipts/latest.json
fi

"$PYTHON_BIN" -m venv /tmp/doneproof-install-venv
/tmp/doneproof-install-venv/bin/python -m pip install --upgrade pip >/tmp/doneproof-install-pip-upgrade.log
/tmp/doneproof-install-venv/bin/python -m pip install -e . >/tmp/doneproof-editable-install.log
/tmp/doneproof-install-venv/bin/doneproof --help >/tmp/doneproof-editable-help.log

"$PYTHON_BIN" -m venv /tmp/doneproof-dev-venv
/tmp/doneproof-dev-venv/bin/python -m pip install --upgrade pip >/tmp/doneproof-dev-pip-upgrade.log
/tmp/doneproof-dev-venv/bin/python -m pip install -e ".[dev]" >/tmp/doneproof-dev-install.log
/tmp/doneproof-dev-venv/bin/python -m build --wheel --outdir /tmp/doneproof-build-check

"$PYTHON_BIN" -m pip wheel . -w /tmp/doneproof-wheel --no-deps
"$PYTHON_BIN" -m venv /tmp/doneproof-wheel-venv
/tmp/doneproof-wheel-venv/bin/python -m pip install --upgrade pip >/tmp/doneproof-wheel-pip-upgrade.log
/tmp/doneproof-wheel-venv/bin/python -m pip install /tmp/doneproof-wheel/*.whl >/tmp/doneproof-wheel-install.log
/tmp/doneproof-wheel-venv/bin/doneproof --help >/tmp/doneproof-help.log
/tmp/doneproof-wheel-venv/bin/doneproof init --root /tmp/doneproof-installed-smoke
git -C /tmp/doneproof-installed-smoke init -b main >/dev/null
printf '# Installed Smoke\n' > /tmp/doneproof-installed-smoke/README.md
/tmp/doneproof-wheel-venv/bin/doneproof doctor --root /tmp/doneproof-installed-smoke

"$RM_BIN" -rf build src/doneproof.egg-info .pytest_cache .ruff_cache
find src tests -type d -name __pycache__ -prune -exec "$RM_BIN" -rf {} +

echo "DoneProof prepublish checks passed."
