from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class DemoResult:
    elapsed_seconds: float
    capture_output: str
    check_output: str
    schema_output: str
    receipt: dict[str, Any]


def run_demo() -> DemoResult:
    """Run the complete Captured Proof flow in an isolated temporary repository."""

    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="doneproof-captured-proof-") as directory:
        root = Path(directory)
        _doneproof(root, "init", "--root", ".")
        _git(root, "init", "-b", "main")
        _git(root, "config", "user.name", "DoneProof Demo")
        _git(root, "config", "user.email", "demo@doneproof.local")

        root.joinpath("README.md").write_text(
            "# Example agent change\n\nBaseline.\n",
            encoding="utf-8",
        )
        root.joinpath("verify_agent_change.py").write_text(
            "print('agent-change-check: PASS')\n",
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
            "Verify the agent change",
            "--changed-file",
            "README.md",
            "--",
            sys.executable,
            "verify_agent_change.py",
        )
        check = _doneproof(root, "check", "--root", ".")
        schema = _doneproof(root, "schema-check", "--root", ".")
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
    print(f"output_digest={output['sha256']}")
    print(f"git_scope_digest={git_scope['sha256']}")
    print(f"integrity_digest={proof['integrity_sha256']}")
    print(f"raw_output_stored={str(output['content_stored']).lower()}")
    print(f"demo_elapsed_seconds={result.elapsed_seconds:.2f}")
    print("DEMO_RESULT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
