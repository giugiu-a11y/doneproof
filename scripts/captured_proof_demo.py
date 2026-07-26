from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEMO_FRAME_DURATIONS_MS = (2200, 2800, 2600, 2800)


@dataclass(frozen=True)
class DemoResult:
    elapsed_seconds: float
    capture_output: str
    check_output: str
    schema_output: str
    report_output: str
    receipt: dict[str, Any]


def run_demo() -> DemoResult:
    """Run the complete Captured Proof flow in an isolated temporary repository."""

    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="doneproof-captured-proof-") as directory:
        root = Path(directory)
        _doneproof(root, "init", "--root", ".")
        _git(root, "init", "-b", "main")
        _git(root, "config", "user.name", "DoneProof Demo")
        _git(root, "config", "user.email", "demo@example.invalid")

        root.joinpath("README.md").write_text(
            "# Example agent change\n\nBaseline.\n",
            encoding="utf-8",
        )
        _git(root, "add", ".")
        _git(root, "-c", "commit.gpgsign=false", "commit", "-m", "baseline")

        root.joinpath("README.md").write_text(
            "# Example agent change\n\nBaseline.\n\nAgent update captured.\n",
            encoding="utf-8",
        )

        capture = _doneproof(
            root,
            "capture",
            "--root",
            ".",
            "--task",
            "Check this change",
            "--",
            "git",
            "diff",
            "--check",
        )
        check = _doneproof(root, "check", "--root", ".")
        schema = _doneproof(root, "schema-check", "--root", ".")
        report = _doneproof(root, "report", "--root", ".")
        receipt = json.loads(
            root.joinpath(".doneproof", "receipts", "latest.json").read_text(
                encoding="utf-8"
            )
        )

    return DemoResult(
        elapsed_seconds=time.monotonic() - started,
        capture_output=capture.stdout.strip(),
        check_output=check.stdout.strip(),
        schema_output=schema.stdout.strip(),
        report_output=report.stdout.strip(),
        receipt=receipt,
    )


def _doneproof(root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, "-m", "doneproof", *arguments],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"DoneProof demo command failed ({result.returncode}): "
            f"{result.stderr.strip() or result.stdout.strip()}"
        )
    return result


def _git(root: Path, *arguments: str) -> None:
    subprocess.run(
        ["git", *arguments],
        cwd=root,
        text=True,
        capture_output=True,
        check=True,
    )


def main() -> int:
    result = run_demo()
    proof = result.receipt["captured_proof"]
    output = proof["output"]
    git_scope = proof["git_scope"]

    print(result.capture_output)
    print(result.check_output)
    print(result.schema_output)
    print(result.report_output)
    print(f"captured_command={proof['command']}")
    print(f"changed_files={','.join(result.receipt['changed_files'])}")
    print(f"output_digest={output['sha256']}")
    print(f"git_scope_digest={git_scope['sha256']}")
    print(f"integrity_digest={proof['integrity_sha256']}")
    print(f"raw_output_stored={str(output['content_stored']).lower()}")
    print(f"git_diff_stored={str(git_scope['content_stored']).lower()}")
    print(f"demo_elapsed_seconds={result.elapsed_seconds:.2f}")
    print("DEMO_RESULT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
