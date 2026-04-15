#!/usr/bin/env python3
"""Generate a parameter coverage report from contract and parity case links."""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path


OUTPUT_COLUMNS = [
    "r_function",
    "python_function",
    "parameter_name",
    "parameter_position",
    "required_case_count",
    "covered_case_ids",
    "side_effect_contract",
    "status",
    "gap_notes",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def truthy(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y"}


def build_report(
    contract_rows: list[dict[str, str]],
    case_rows: list[dict[str, str]],
    link_rows: list[dict[str, str]],
) -> tuple[list[dict[str, str]], dict[str, dict[str, int]]]:
    case_ids = {row["case_id"] for row in case_rows}
    link_index: dict[tuple[str, str], list[str]] = defaultdict(list)
    for row in link_rows:
        if row["case_id"] in case_ids:
            link_index[(row["function_name"], row["parameter_name"])].append(row["case_id"])

    report_rows: list[dict[str, str]] = []
    summary: dict[str, dict[str, int]] = defaultdict(lambda: {"covered": 0, "missing": 0})

    for row in sorted(contract_rows, key=lambda item: (item["r_function"], int(item["parameter_position"]))):
        covered_case_ids = sorted(set(link_index[(row["r_function"], row["parameter_name"])]))
        covered = bool(covered_case_ids)
        status = "covered" if covered else "missing_explicit_case"
        summary[row["r_function"]]["covered" if covered else "missing"] += 1
        report_rows.append(
            {
                "r_function": row["r_function"],
                "python_function": row["python_function"],
                "parameter_name": row["parameter_name"],
                "parameter_position": row["parameter_position"],
                "required_case_count": "1",
                "covered_case_ids": ";".join(covered_case_ids),
                "side_effect_contract": row["side_effect_contract"],
                "status": status,
                "gap_notes": "" if covered else "No explicit parity case linked to this public parameter",
            }
        )

    return report_rows, summary


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, str]], summary: dict[str, dict[str, int]]) -> None:
    lines = [
        "# Parameter Coverage Report",
        "",
        "## Function Summary",
        "",
        "| Function | Covered Parameters | Missing Parameters |",
        "| --- | --- | --- |",
    ]
    for function_name in sorted(summary):
        lines.append(
            f"| {function_name} | {summary[function_name]['covered']} | {summary[function_name]['missing']} |"
        )

    lines.extend(
        [
            "",
            "## Parameter Detail",
            "",
            "| R Function | Python Function | Parameter | Position | Case IDs | Status | Gap Notes |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in rows:
        lines.append(
            "| {r_function} | {python_function} | {parameter_name} | {parameter_position} | {covered_case_ids} | {status} | {gap_notes} |".format(
                **row
            )
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a parameter coverage report.")
    parser.add_argument("--contract", required=True, help="Path to FUNCTION_CONTRACT.csv")
    parser.add_argument("--cases", required=True, help="Path to PARITY_CASES.csv")
    parser.add_argument("--links", required=True, help="Path to PARAMETER_CASE_LINKS.csv")
    parser.add_argument("--output-csv", required=True, help="Path to write the coverage CSV")
    parser.add_argument("--output-md", required=True, help="Path to write the coverage Markdown report")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report_rows, summary = build_report(
        read_csv(Path(args.contract)),
        read_csv(Path(args.cases)),
        read_csv(Path(args.links)),
    )
    write_csv(Path(args.output_csv), report_rows)
    write_markdown(Path(args.output_md), report_rows, summary)
    missing = sum(item["missing"] for item in summary.values())
    print(f"Generated coverage report with {missing} uncovered parameters.")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
