#!/usr/bin/env python3
"""Validate the machine-readable public function contract."""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path


REQUIRED_COLUMNS = [
    "r_function",
    "python_function",
    "output_kind",
    "parameter_name",
    "r_parameter_name",
    "python_parameter_name",
    "parameter_position",
    "r_default",
    "python_default",
    "effective_default_match",
    "documented_in_r",
    "documented_in_python",
    "side_effect_contract",
    "deviation_id",
    "notes",
]


def truthy(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y"}


def json_escape(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\b", "\\b")
        .replace("\f", "\\f")
        .replace("\n", "\\n")
        .replace("\r", "\\r")
        .replace("\t", "\\t")
    )


def to_json(value: object) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return f'"{json_escape(value)}"'
    if isinstance(value, list):
        return "[" + ", ".join(to_json(item) for item in value) + "]"
    if isinstance(value, dict):
        return (
            "{"
            + ", ".join(f"{to_json(str(key))}: {to_json(item)}" for key, item in value.items())
            + "}"
        )
    raise TypeError(f"Unsupported JSON value: {type(value)!r}")


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = [column for column in REQUIRED_COLUMNS if column not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"Missing required columns: {', '.join(missing)}")
        return list(reader)


def validate(rows: list[dict[str, str]]) -> dict[str, object]:
    issues: list[dict[str, str]] = []
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)

    for row in rows:
        grouped[row["r_function"]].append(row)

        if not row["r_function"] or not row["python_function"]:
            issues.append({"type": "missing_function_name", "row": repr(row)})
        if row["r_function"] != row["python_function"] and not row["deviation_id"].strip():
            issues.append(
                {
                    "type": "function_name_mismatch",
                    "function": row["r_function"],
                    "python_function": row["python_function"],
                }
            )
        if row["r_parameter_name"] != row["python_parameter_name"] and not row["deviation_id"].strip():
            issues.append(
                {
                    "type": "parameter_name_mismatch",
                    "function": row["r_function"],
                    "parameter": row["parameter_name"],
                    "r_parameter_name": row["r_parameter_name"],
                    "python_parameter_name": row["python_parameter_name"],
                }
            )
        if not truthy(row["effective_default_match"]) and not row["deviation_id"].strip():
            issues.append(
                {
                    "type": "default_mismatch",
                    "function": row["r_function"],
                    "parameter": row["parameter_name"],
                    "r_default": row["r_default"],
                    "python_default": row["python_default"],
                }
            )
        if not truthy(row["documented_in_r"]):
            issues.append(
                {
                    "type": "undocumented_in_r",
                    "function": row["r_function"],
                    "parameter": row["parameter_name"],
                }
            )
        if not truthy(row["documented_in_python"]):
            issues.append(
                {
                    "type": "undocumented_in_python",
                    "function": row["r_function"],
                    "parameter": row["parameter_name"],
                }
            )
        if not row["side_effect_contract"].strip():
            issues.append(
                {
                    "type": "missing_side_effect_contract",
                    "function": row["r_function"],
                    "parameter": row["parameter_name"],
                }
            )

    for function_name, function_rows in grouped.items():
        positions: list[int] = []
        seen_parameters: set[str] = set()
        for row in function_rows:
            try:
                position = int(row["parameter_position"])
            except ValueError:
                issues.append(
                    {
                        "type": "invalid_parameter_position",
                        "function": function_name,
                        "parameter": row["parameter_name"],
                        "value": row["parameter_position"],
                    }
                )
                continue
            positions.append(position)
            if row["parameter_name"] in seen_parameters:
                issues.append(
                    {
                        "type": "duplicate_parameter",
                        "function": function_name,
                        "parameter": row["parameter_name"],
                    }
                )
            seen_parameters.add(row["parameter_name"])

        if positions:
            ordered = sorted(positions)
            expected = list(range(1, len(ordered) + 1))
            if ordered != expected:
                issues.append(
                    {
                        "type": "parameter_order_gap",
                        "function": function_name,
                        "positions": ",".join(str(item) for item in ordered),
                    }
                )

    return {
        "summary": {
            "functions": len(grouped),
            "parameters": len(rows),
            "issue_count": len(issues),
        },
        "issues": issues,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a function parity contract CSV.")
    parser.add_argument("--contract", required=True, help="Path to FUNCTION_CONTRACT.csv")
    parser.add_argument("--output-json", help="Write the validation report to this JSON file.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = validate(load_rows(Path(args.contract)))
    if args.output_json:
        path = Path(args.output_json)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(to_json(report) + "\n", encoding="utf-8")
    print(to_json(report["summary"]))
    return 1 if report["issues"] else 0


if __name__ == "__main__":
    sys.exit(main())
