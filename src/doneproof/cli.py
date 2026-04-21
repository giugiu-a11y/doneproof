"""DoneProof command-line interface."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any
from urllib.parse import quote

from . import __version__
from .doctor import run_doctor
from .git import changed_files, git_diff_summary
from .policy import init_project, load_policy
from .receipt import ValidationResult, build_receipt, load_receipt, validate_receipt, write_receipt
from .schema import validate_receipt_schema

DEFAULT_RECEIPT = ".doneproof/receipts/latest.json"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="doneproof", description="No proof, no done.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subcommands = parser.add_subparsers(dest="command", required=True)

    init_parser = subcommands.add_parser("init", help="Create .doneproof policy and templates.")
    init_parser.add_argument(
        "--root",
        default=".",
        help="Repository root. Defaults to current directory.",
    )
    init_parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing DoneProof files.",
    )

    check_parser = subcommands.add_parser("check", help="Validate a DoneProof receipt.")
    check_parser.add_argument(
        "--root",
        default=".",
        help="Repository root. Defaults to current directory.",
    )
    check_parser.add_argument(
        "--receipt",
        default=DEFAULT_RECEIPT,
        help=f"Path to receipt JSON. Defaults to {DEFAULT_RECEIPT}.",
    )
    check_parser.add_argument("--json", action="store_true", help="Print machine-readable result.")

    report_parser = subcommands.add_parser("report", help="Print a receipt report.")
    report_parser.add_argument(
        "--root",
        default=".",
        help="Repository root. Defaults to current directory.",
    )
    report_parser.add_argument(
        "--receipt",
        default=DEFAULT_RECEIPT,
        help=f"Path to receipt JSON. Defaults to {DEFAULT_RECEIPT}.",
    )
    report_parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Report output format. Defaults to text.",
    )

    badge_parser = subcommands.add_parser("badge", help="Print a compact receipt badge.")
    badge_parser.add_argument(
        "--root",
        default=".",
        help="Repository root. Defaults to current directory.",
    )
    badge_parser.add_argument(
        "--receipt",
        default=DEFAULT_RECEIPT,
        help=f"Path to receipt JSON. Defaults to {DEFAULT_RECEIPT}.",
    )
    badge_parser.add_argument(
        "--format",
        choices=["text", "markdown", "json"],
        default="text",
        help="Badge output format. Defaults to text.",
    )

    new_parser = subcommands.add_parser("new", help="Create a receipt draft.")
    new_parser.add_argument(
        "--root",
        default=".",
        help="Repository root. Defaults to current directory.",
    )
    new_parser.add_argument("--task", required=True, help="Task this receipt covers.")
    new_parser.add_argument("--summary", default="", help="Short summary of the work.")
    new_parser.add_argument("--status", default="awaiting_review", help="Receipt status.")
    new_parser.add_argument(
        "--output",
        default=DEFAULT_RECEIPT,
        help=f"Receipt path to write. Defaults to {DEFAULT_RECEIPT}.",
    )
    new_parser.add_argument("--changed-file", action="append", default=[], help="Changed file.")
    new_parser.add_argument(
        "--command",
        dest="command_evidence",
        action="append",
        default=[],
        help='Command evidence. Use "passed:pytest" or just "pytest".',
    )
    new_parser.add_argument(
        "--evidence",
        action="append",
        default=[],
        help='Evidence item. Use "test:pytest passed" or plain text.',
    )
    new_parser.add_argument("--risk", action="append", default=[], help="Known residual risk.")

    doctor_parser = subcommands.add_parser("doctor", help="Check DoneProof setup.")
    doctor_parser.add_argument(
        "--root",
        default=".",
        help="Repository root. Defaults to current directory.",
    )
    doctor_parser.add_argument("--json", action="store_true", help="Print machine-readable result.")

    schema_check_parser = subcommands.add_parser(
        "schema-check",
        help="Validate receipt JSON against the bundled schema.",
    )
    schema_check_parser.add_argument(
        "--root",
        default=".",
        help="Repository root. Defaults to current directory.",
    )
    schema_check_parser.add_argument(
        "--receipt",
        default=DEFAULT_RECEIPT,
        help=f"Path to receipt JSON. Defaults to {DEFAULT_RECEIPT}.",
    )
    schema_check_parser.add_argument(
        "--schema",
        default="",
        help="Optional path to schema JSON. Defaults to bundled schema.",
    )
    schema_check_parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable result.",
    )

    evidence_parser = subcommands.add_parser("evidence", help="Create local evidence artifacts.")
    evidence_subcommands = evidence_parser.add_subparsers(
        dest="evidence_command",
        required=True,
    )
    git_diff_parser = evidence_subcommands.add_parser(
        "git-diff",
        help="Write a sanitized git diff summary.",
    )
    git_diff_parser.add_argument(
        "--root",
        default=".",
        help="Repository root. Defaults to current directory.",
    )
    git_diff_parser.add_argument(
        "--output",
        default=".doneproof/evidence/git-diff-summary.txt",
        help="Evidence artifact path to write.",
    )
    git_diff_parser.add_argument(
        "--path",
        action="append",
        default=[],
        help="Repo-relative path filter. Can be used more than once.",
    )
    git_diff_parser.add_argument(
        "--mode",
        choices=["all", "staged", "unstaged", "untracked"],
        default="all",
        help="Evidence scope to summarize. Defaults to all.",
    )

    args = parser.parse_args(argv)
    if args.command == "init":
        return _init(args)
    if args.command == "check":
        return _check(args)
    if args.command == "report":
        return _report(args)
    if args.command == "badge":
        return _badge(args)
    if args.command == "new":
        return _new(args)
    if args.command == "doctor":
        return _doctor(args)
    if args.command == "schema-check":
        return _schema_check(args)
    if args.command == "evidence":
        return _evidence(args)
    parser.error(f"Unknown command: {args.command}")
    return 2


def _init(args: argparse.Namespace) -> int:
    root = Path(args.root).expanduser().resolve()
    created = init_project(root, overwrite=args.overwrite)
    print(f"DoneProof initialized at {root}")
    if created:
        for path in created:
            print(f"created: {path.relative_to(root)}")
    else:
        print("no files changed")
    return 0


def _check(args: argparse.Namespace) -> int:
    root = Path(args.root).expanduser().resolve()
    receipt_path = _resolve_receipt_path(root, args.receipt)

    try:
        policy = load_policy(root)
        receipt = load_receipt(receipt_path)
        result = validate_receipt(receipt, policy, receipt_path, repo_root=root)
    except ValueError as exc:
        if args.json:
            print(json.dumps({"ok": False, "errors": [str(exc)]}, indent=2))
        else:
            print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(
            json.dumps(
                {
                    "ok": result.ok,
                    "receipt": _display_path(result.receipt_path, root),
                    "errors": [finding.message for finding in result.errors()],
                    "warnings": [finding.message for finding in result.warnings()],
                },
                indent=2,
            )
        )
    else:
        _print_validation(result.ok, result.errors(), result.warnings())
    return 0 if result.ok else 1


def _report(args: argparse.Namespace) -> int:
    root = Path(args.root).expanduser().resolve()
    receipt_path = _resolve_receipt_path(root, args.receipt)
    try:
        policy = load_policy(root)
        receipt = load_receipt(receipt_path)
        result = validate_receipt(receipt, policy, receipt_path, repo_root=root)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps(_report_payload(receipt, result, root), indent=2))
        return 0 if result.ok else 1

    print(f"Task: {receipt.get('task', 'n/a')}")
    print(f"Status: {receipt.get('status', 'n/a')}")
    print(f"Summary: {receipt.get('summary', 'n/a')}")
    print("")
    print("Changed files:")
    for path in receipt.get("changed_files", []):
        print(f"- {path}")
    print("")
    print("Commands:")
    for command in receipt.get("commands", []):
        if isinstance(command, dict):
            print(f"- [{command.get('status', 'unknown')}] {command.get('cmd', '')}")
    print("")
    print("Evidence:")
    for evidence in receipt.get("evidence", []):
        if isinstance(evidence, dict):
            print(f"- {evidence.get('type', 'evidence')}: {evidence.get('value', '')}")
        else:
            print(f"- {evidence}")
    print("")
    _print_validation(result.ok, result.errors(), result.warnings())
    return 0 if result.ok else 1


def _badge(args: argparse.Namespace) -> int:
    root = Path(args.root).expanduser().resolve()
    receipt_path = _resolve_receipt_path(root, args.receipt)
    try:
        policy = load_policy(root)
        receipt = load_receipt(receipt_path)
        result = validate_receipt(receipt, policy, receipt_path, repo_root=root)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    payload = _badge_payload(receipt, result)
    if args.format == "json":
        print(json.dumps(payload, indent=2))
    elif args.format == "markdown":
        print(payload["markdown"])
    else:
        print(payload["text"])
    return 0 if result.ok else 1


def _new(args: argparse.Namespace) -> int:
    root = Path(args.root).expanduser().resolve()
    output = _resolve_receipt_path(root, args.output)
    files = list(args.changed_file) or changed_files(root)
    receipt = build_receipt(
        task=args.task,
        status=args.status,
        summary=args.summary or "Receipt draft created by DoneProof.",
        changed_files=files,
        commands=[_parse_command(item) for item in args.command_evidence],
        evidence=[_parse_evidence(item) for item in args.evidence],
        risks=list(args.risk),
    )
    write_receipt(output, receipt)
    print(f"created: {output.relative_to(root) if output.is_relative_to(root) else output}")
    return 0


def _doctor(args: argparse.Namespace) -> int:
    root = Path(args.root).expanduser().resolve()
    result = run_doctor(root)
    if args.json:
        print(
            json.dumps(
                {
                    "ok": result.ok,
                    "checks": result.checks,
                    "errors": result.errors,
                    "warnings": result.warnings,
                },
                indent=2,
            )
        )
    else:
        print("DoneProof doctor: PASS" if result.ok else "DoneProof doctor: FAIL")
        for check in result.checks:
            print(f"check: {check}")
        for error in result.errors:
            print(f"error: {error}")
        for warning in result.warnings:
            print(f"warning: {warning}")
    return 0 if result.ok else 1


def _schema_check(args: argparse.Namespace) -> int:
    root = Path(args.root).expanduser().resolve()
    receipt_path = _resolve_receipt_path(root, args.receipt)
    schema_path = _resolve_receipt_path(root, args.schema) if args.schema else None
    try:
        receipt = load_receipt(receipt_path)
        result = validate_receipt_schema(receipt, schema_path=schema_path)
    except ValueError as exc:
        if args.json:
            print(json.dumps({"ok": False, "errors": [str(exc)]}, indent=2))
        else:
            print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(
            json.dumps(
                {
                    "ok": result.ok,
                    "receipt": _display_path(receipt_path, root),
                    "schema": _display_path(result.schema_path, root),
                    "errors": result.errors,
                },
                indent=2,
            )
        )
    else:
        state = "PASS" if result.ok else "FAIL"
        print(f"DoneProof schema: {state}")
        for error in result.errors:
            print(f"error: {error}")
    return 0 if result.ok else 1


def _evidence(args: argparse.Namespace) -> int:
    if args.evidence_command == "git-diff":
        return _evidence_git_diff(args)
    print(f"ERROR: Unknown evidence command: {args.evidence_command}", file=sys.stderr)
    return 2


def _evidence_git_diff(args: argparse.Namespace) -> int:
    root = Path(args.root).expanduser().resolve()
    output = _resolve_receipt_path(root, args.output)
    try:
        summary = git_diff_summary(root, paths=list(args.path), mode=args.mode)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(summary, encoding="utf-8")
    print(f"created: {output.relative_to(root) if output.is_relative_to(root) else output}")
    return 0


def _print_validation(ok: bool, errors: list[object], warnings: list[object]) -> None:
    if ok:
        print("DoneProof: PASS")
    else:
        print("DoneProof: FAIL")
    for error in errors:
        print(f"error: {getattr(error, 'message', error)}")
    for warning in warnings:
        print(f"warning: {getattr(warning, 'message', warning)}")


def _report_payload(
    receipt: dict[str, Any],
    result: ValidationResult,
    root: Path,
) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "ok": result.ok,
        "receipt": _display_path(result.receipt_path, root),
        "task": receipt.get("task", ""),
        "status": receipt.get("status", ""),
        "summary": receipt.get("summary", ""),
        "changed_files": receipt.get("changed_files", []),
        "commands": receipt.get("commands", []),
        "evidence": receipt.get("evidence", []),
        "risks": receipt.get("risks", []),
        "errors": [finding.message for finding in result.errors()],
        "warnings": [finding.message for finding in result.warnings()],
    }


def _badge_payload(receipt: dict[str, Any], result: ValidationResult) -> dict[str, Any]:
    ok = result.ok
    status = str(receipt.get("status", "unknown")).strip() or "unknown"
    risks = receipt.get("risks", [])
    risk_count = len(risks) if isinstance(risks, list) else 0
    error_count = len(result.errors())
    warning_count = len(result.warnings())
    color = _badge_color(status, ok, risk_count)
    state = status if ok else "failed"
    risk_text = f"risks: {risk_count}" if risk_count else "no risks listed"
    message = f"{state} | {risk_text}"
    if error_count:
        message = f"{state} | errors: {error_count}"
    elif warning_count:
        message = f"{message} | warnings: {warning_count}"
    markdown = (
        f"![DoneProof: {message}]"
        f"(https://img.shields.io/badge/"
        f"{quote('DoneProof', safe='')}-{quote(message, safe='')}-{color})"
    )
    return {
        "schema_version": "1.0",
        "ok": ok,
        "status": status,
        "state": state,
        "risks": risk_count,
        "errors": error_count,
        "warnings": warning_count,
        "color": color,
        "text": f"DoneProof: {message}",
        "markdown": markdown,
    }


def _badge_color(status: str, ok: bool, risk_count: int) -> str:
    normalized = status.strip().lower()
    if not ok or normalized == "failed":
        return "red"
    if normalized == "blocked":
        return "orange"
    if risk_count:
        return "yellow"
    return "brightgreen"


def _display_path(path: Path, root: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(root))
    except ValueError:
        return str(resolved)


def _resolve_receipt_path(root: Path, raw_path: str) -> Path:
    path = Path(raw_path).expanduser()
    if path.is_absolute():
        return path.resolve()
    return (root / path).resolve()


def _parse_command(value: str) -> dict[str, str]:
    status, _, cmd = value.partition(":")
    if cmd and status in {"passed", "failed", "skipped"}:
        return {"cmd": cmd.strip(), "status": status}
    return {"cmd": value.strip(), "status": "passed"}


def _parse_evidence(value: str) -> dict[str, str]:
    evidence_type, _, evidence_value = value.partition(":")
    if evidence_value:
        return {"type": evidence_type.strip() or "note", "value": evidence_value.strip()}
    return {"type": "note", "value": value.strip()}


if __name__ == "__main__":
    raise SystemExit(main())
