from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "captured_proof_demo.py"
SPEC = importlib.util.spec_from_file_location("captured_proof_demo", SCRIPT_PATH)
assert SPEC is not None
assert SPEC.loader is not None
DEMO_MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = DEMO_MODULE
SPEC.loader.exec_module(DEMO_MODULE)

DEMO_FRAME_DURATIONS_MS = DEMO_MODULE.DEMO_FRAME_DURATIONS_MS
run_demo = DEMO_MODULE.run_demo


def test_captured_proof_demo_is_real_coherent_and_under_sixty_seconds() -> None:
    result = run_demo()
    proof = result.receipt["captured_proof"]

    assert result.elapsed_seconds < 60
    assert sum(DEMO_FRAME_DURATIONS_MS) < 60_000
    assert result.receipt["task"] == "Check this change"
    assert result.receipt["changed_files"] == ["README.md"]
    assert proof["command"] == "git diff --check"
    assert proof["result"] == "passed"
    assert proof["exit_code"] == 0
    assert proof["output"]["content_stored"] is False
    assert proof["git_scope"]["content_stored"] is False
    assert "Captured Proof: PASS" in result.capture_output
    assert "DoneProof: PASS" in result.check_output
    assert "DoneProof schema: PASS" in result.schema_output
    assert "Task: Check this change" in result.report_output
    assert "- README.md" in result.report_output
    assert "DoneProof: PASS" in result.report_output
