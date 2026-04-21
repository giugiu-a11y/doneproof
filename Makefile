.PHONY: lint test compile smoke check prepublish

PYTHON ?= $(shell command -v python3.12 || command -v python3.11 || command -v python3.10 || command -v python3)
UV_RUN = uv run --extra dev --python $(PYTHON)

lint:
	$(UV_RUN) ruff check .

test:
	$(UV_RUN) pytest

compile:
	$(UV_RUN) python -m compileall -q src tests

smoke:
	rm -rf /tmp/doneproof-smoke
	$(UV_RUN) doneproof init --root /tmp/doneproof-smoke
	git -C /tmp/doneproof-smoke init -b main
	touch /tmp/doneproof-smoke/README.md
	$(UV_RUN) doneproof doctor --root /tmp/doneproof-smoke
	$(UV_RUN) doneproof evidence git-diff --root /tmp/doneproof-smoke
	$(UV_RUN) doneproof check --root . --receipt examples/receipts/passing.json
	$(UV_RUN) doneproof report --root . --receipt examples/receipts/passing.json
	$(UV_RUN) doneproof new --root /tmp/doneproof-smoke --task "Smoke task" --changed-file README.md --command "passed:echo ok" --evidence "smoke:echo ok" --risk "Example only"
	$(UV_RUN) doneproof check --root /tmp/doneproof-smoke
	! $(UV_RUN) doneproof check --root . --receipt examples/receipts/failing.json

check: lint test compile smoke

prepublish:
	bash scripts/prepublish_check.sh
