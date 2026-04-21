"""Receipt schema loading and validation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


@dataclass
class SchemaValidationResult:
    ok: bool
    schema_path: Path
    errors: list[str]


def validate_receipt_schema(
    receipt: dict[str, Any],
    *,
    schema_path: Path | None = None,
) -> SchemaValidationResult:
    active_schema_path = schema_path or _default_schema_path()
    try:
        schema = json.loads(active_schema_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"Schema not found: {active_schema_path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Schema is not valid JSON: {active_schema_path}: {exc}") from exc

    validator = Draft202012Validator(schema)
    sorted_errors = sorted(
        validator.iter_errors(receipt),
        key=lambda item: list(item.absolute_path),
    )
    errors = [
        f"{_format_error_path(error.absolute_path)}: {error.message}"
        for error in sorted_errors
    ]

    return SchemaValidationResult(ok=not errors, schema_path=active_schema_path, errors=errors)


def _default_schema_path() -> Path:
    from importlib.resources import files

    repository_schema = Path(__file__).resolve().parents[2] / "schemas" / "receipt.schema.json"
    if repository_schema.exists():
        return repository_schema
    resource = files("doneproof.schemas").joinpath("receipt.schema.json")
    return Path(str(resource))


def _format_error_path(path_parts: Any) -> str:
    path = "$"
    for part in path_parts:
        if isinstance(part, int):
            path += f"[{part}]"
            continue
        text = str(part)
        if not text:
            continue
        path += f".{text}"
    return path
