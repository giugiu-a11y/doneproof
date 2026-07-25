"""Machine-captured command evidence for DoneProof receipts."""

from __future__ import annotations

import hashlib
import os
import platform
import re
import shlex
import signal
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import TextIO

from .git import changed_files, git_scope_digest, is_public_candidate
from .receipt import build_receipt, captured_proof_integrity

REPRODUCE_URL = "https://github.com/giugiu-a11y/doneproof#captured-proof"
_REDACTED = "[REDACTED]"
_SENSITIVE_KEY = re.compile(
    r"(?:api[_-]?key|private[_-]?key|password|passwd|secret|token)",
    re.IGNORECASE,
)
_ASSIGNMENT = re.compile(
    r"(?i)\b([a-z_][a-z0-9_.-]*\s*[=:]\s*)([^\s,;]+)"
)
_BEARER = re.compile(r"(?i)(\bauthorization\s*:\s*bearer\s+)([^\s]+)")
_KNOWN_CREDENTIAL = re.compile(
    r"(?<![a-zA-Z0-9])(?:gh[pousr]_[a-zA-Z0-9]{20,}|"
    + r"s"
    + r"k-[a-zA-Z0-9_-]{20,})"
)
_LOCAL_HOME_PATH = re.compile(
    r"(?:/(?:Users|home)/[^/\s]+)(?:/[^\s'\";,)]*)?"
)
_WINDOWS_HOME_PATH = re.compile(
    r"(?i)(?:[a-z]:\\Users\\[^\\\s]+)(?:\\[^\s'\";,)]*)?"
)


@dataclass(frozen=True)
class CapturedRun:
    exit_code: int
    duration_ms: int
    output_sha256: str
    output_bytes: int
    output_lines: int
    redactions: int
    timed_out: bool


class _StreamDigest:
    def __init__(self, output: TextIO) -> None:
        self.output = output
        self.hasher = hashlib.sha256()
        self.byte_count = 0
        self.line_count = 0
        self.redaction_count = 0

    def consume(self, text: str) -> None:
        sanitized, count = redact_text(text)
        self.output.write(sanitized)
        self.output.flush()
        encoded = sanitized.encode("utf-8", errors="replace")
        self.byte_count += len(encoded)
        self.line_count += sanitized.count("\n")
        if sanitized and not sanitized.endswith("\n"):
            self.line_count += 1
        self.redaction_count += count
        self.hasher.update(encoded)

    @property
    def digest(self) -> str:
        return f"sha256:{self.hasher.hexdigest()}"


def redact_text(text: str) -> tuple[str, int]:
    """Mask known secret shapes before evidence is hashed or persisted."""

    count = 0

    def replace_assignment(match: re.Match[str]) -> str:
        nonlocal count
        if not _SENSITIVE_KEY.search(match.group(1)):
            return match.group(0)
        count += 1
        return f"{match.group(1)}{_REDACTED}"

    def replace_prefixed(match: re.Match[str]) -> str:
        nonlocal count
        count += 1
        return f"{match.group(1)}{_REDACTED}"

    def replace_token(_match: re.Match[str]) -> str:
        nonlocal count
        count += 1
        return _REDACTED

    def replace_local_path(_match: re.Match[str]) -> str:
        nonlocal count
        count += 1
        return "[LOCAL_PATH]"

    sanitized = _ASSIGNMENT.sub(replace_assignment, text)
    sanitized = _BEARER.sub(replace_prefixed, sanitized)
    sanitized = _KNOWN_CREDENTIAL.sub(replace_token, sanitized)
    sanitized = _LOCAL_HOME_PATH.sub(replace_local_path, sanitized)
    sanitized = _WINDOWS_HOME_PATH.sub(replace_local_path, sanitized)
    return sanitized, count


def safe_command_display(command: list[str]) -> tuple[str, int]:
    """Render an argv command while masking explicit secret-bearing arguments."""

    safe: list[str] = []
    redactions = 0
    redact_next = False
    for argument in command:
        if redact_next:
            safe.append(_REDACTED)
            redactions += 1
            redact_next = False
            continue

        if argument.startswith("-"):
            option, separator, value = argument.partition("=")
            if _SENSITIVE_KEY.search(option):
                if separator:
                    safe.append(f"{option}={_REDACTED}")
                    redactions += 1
                else:
                    safe.append(argument)
                    redact_next = True
                continue

        if "=" in argument:
            key, _, _value = argument.partition("=")
            if _SENSITIVE_KEY.search(key):
                safe.append(f"{key}={_REDACTED}")
                redactions += 1
                continue

        sanitized, count = redact_text(argument)
        safe.append(sanitized)
        redactions += count

    return shlex.join(safe), redactions


def run_command(
    command: list[str],
    *,
    root: Path,
    timeout_seconds: float,
    output: TextIO | None = None,
) -> CapturedRun:
    """Execute argv without a shell and stream output while hashing a redacted view."""

    stream = _StreamDigest(output or sys.stdout)
    started = time.monotonic()
    timed_out = False

    try:
        process = subprocess.Popen(
            command,
            cwd=root,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
            start_new_session=os.name == "posix",
        )
    except FileNotFoundError:
        stream.consume(f"doneproof: executable not found: {command[0]}\n")
        return _captured_run(stream, started, exit_code=127, timed_out=False)
    except OSError as exc:
        stream.consume(f"doneproof: command could not start: {type(exc).__name__}\n")
        return _captured_run(stream, started, exit_code=126, timed_out=False)

    assert process.stdout is not None

    def consume_output() -> None:
        for line in process.stdout:
            stream.consume(line)
        process.stdout.close()

    reader = threading.Thread(target=consume_output, name="doneproof-output", daemon=True)
    reader.start()
    try:
        process.wait(timeout=timeout_seconds)
    except subprocess.TimeoutExpired:
        timed_out = True
        _stop_process(process)
    except KeyboardInterrupt:
        _stop_process(process)
        reader.join(timeout=2)
        raise

    reader.join()
    exit_code = 124 if timed_out else int(process.returncode)
    return _captured_run(stream, started, exit_code=exit_code, timed_out=timed_out)


def _stop_process(process: subprocess.Popen[str]) -> None:
    """Stop the command and its children when the platform supports process groups."""

    if process.poll() is not None:
        return
    try:
        if os.name == "posix":
            os.killpg(process.pid, signal.SIGTERM)
        else:
            process.terminate()
        process.wait(timeout=2)
    except (ProcessLookupError, subprocess.TimeoutExpired):
        if process.poll() is None:
            if os.name == "posix":
                os.killpg(process.pid, signal.SIGKILL)
            else:
                process.kill()
            process.wait()


def build_captured_receipt(
    *,
    root: Path,
    task: str,
    summary: str,
    command: list[str],
    run: CapturedRun,
    requested_files: list[str],
    git_mode: str,
    risks: list[str],
) -> dict[str, object]:
    files = resolve_changed_files(root, requested_files)
    git_sha256 = git_scope_digest(root, paths=files, mode=git_mode)
    display_command, command_redactions = safe_command_display(command)
    result = "passed" if run.exit_code == 0 else "failed"
    captured_at = datetime.now(timezone.utc).isoformat()

    proof: dict[str, object] = {
        "version": "1.0",
        "captured_at": captured_at,
        "command": display_command,
        "result": result,
        "exit_code": run.exit_code,
        "duration_ms": run.duration_ms,
        "timed_out": run.timed_out,
        "output": {
            "sha256": run.output_sha256,
            "bytes": run.output_bytes,
            "lines": run.output_lines,
            "content_stored": False,
            "redactions": run.redactions,
            "redaction_status": (
                "known_patterns_masked" if run.redactions else "not_detected"
            ),
        },
        "command_redactions": command_redactions,
        "git_scope": {
            "mode": git_mode,
            "sha256": git_sha256,
            "changed_files": files,
            "content_stored": False,
        },
        "environment": {
            "os": platform.system(),
            "architecture": platform.machine(),
            "python": platform.python_version(),
        },
    }
    proof["integrity_sha256"] = captured_proof_integrity(proof)

    receipt = build_receipt(
        task=task,
        status="awaiting_review" if run.exit_code == 0 else "failed",
        summary=summary
        or (
            "Machine-captured command passed; receipt awaits human review."
            if run.exit_code == 0
            else "Machine-captured command failed; receipt records the failure."
        ),
        changed_files=files,
        commands=[
            {
                "cmd": display_command,
                "status": result,
                "captured": True,
                "exit_code": run.exit_code,
                "duration_ms": run.duration_ms,
                "output_sha256": run.output_sha256,
            }
        ],
        evidence=[
            {
                "type": "captured_output",
                "value": (
                    f"{run.output_sha256}; content not stored; redactions={run.redactions}"
                ),
            },
            {
                "type": "git_scope",
                "value": f"{git_sha256}; mode={git_mode}; files={len(files)}",
            },
            {"type": "reproduce", "value": REPRODUCE_URL},
        ],
        risks=risks,
        captured_proof=proof,
    )
    return receipt


def _captured_run(
    stream: _StreamDigest,
    started: float,
    *,
    exit_code: int,
    timed_out: bool,
) -> CapturedRun:
    elapsed_ms = max(0, round((time.monotonic() - started) * 1000))
    return CapturedRun(
        exit_code=exit_code,
        duration_ms=elapsed_ms,
        output_sha256=stream.digest,
        output_bytes=stream.byte_count,
        output_lines=stream.line_count,
        redactions=stream.redaction_count,
        timed_out=timed_out,
    )


def resolve_changed_files(root: Path, requested_files: list[str]) -> list[str]:
    """Return a privacy-safe, repo-relative file scope for a captured receipt."""

    active_files = changed_files(root)
    if not requested_files:
        if not active_files:
            raise ValueError("No privacy-safe changed files were detected in Git")
        return active_files

    resolved: list[str] = []
    for raw_path in requested_files:
        path = validate_requested_file(raw_path)
        if path not in active_files:
            raise ValueError(f"Changed file is not currently changed in Git: {path}")
        resolved.append(path)
    return sorted(dict.fromkeys(resolved))


def validate_requested_file(raw_path: str) -> str:
    """Validate a requested path without inspecting its contents."""

    path = raw_path.strip()
    path_obj = Path(path)
    if (
        not path
        or path_obj.is_absolute()
        or "\\" in path
        or ".." in path_obj.parts
        or not is_public_candidate(path)
    ):
        raise ValueError(f"Changed file must be repo-relative and privacy-safe: {raw_path}")
    return path
