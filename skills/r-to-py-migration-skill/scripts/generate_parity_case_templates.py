#!/usr/bin/env python3
"""Generate parity case and parameter-link scaffolds from a function contract."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path


CASE_COLUMNS = [
    "case_id",
    "function_name",
    "case_kind",
    "output_kind",
    "is_default_case",
    "is_non_default_case",
    "r_fixture_ref",
    "python_fixture_ref",
    "parameter_overrides",
    "expected_side_effects",
    "plot_review_required",
    "status",
    "notes",
]

LINK_COLUMNS = [
    "case_id",
    "function_name",
    "parameter_name",
    "coverage_kind",
    "asserts_default_behavior",
    "asserts_side_effects",
    "asserts_ordering",
    "asserts_plot_rendering",
    "notes",
]


def slugify(value: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "_" for ch in value).strip("_")


def load_contract(path: Path) -> dict[str, list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["r_function"]].append(row)
    return grouped


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_rows(grouped: dict[str, list[dict[str, str]]]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    case_rows: list[dict[str, str]] = []
    link_rows: list[dict[str, str]] = []

    for function_name, rows in grouped.items():
        ordered_rows = sorted(rows, key=lambda row: int(row["parameter_position"]))
        output_kind = ordered_rows[0]["output_kind"]
        base_case_id = slugify(function_name)

        default_case_id = f"{base_case_id}__defaults"
        case_rows.append(
            {
                "case_id": default_case_id,
                "function_name": function_name,
                "case_kind": "default",
                "output_kind": output_kind,
                "is_default_case": "TRUE",
                "is_non_default_case": "FALSE",
                "r_fixture_ref": "",
                "python_fixture_ref": "",
                "parameter_overrides": "{}",
                "expected_side_effects": "Document default warnings, ordering, and side effects",
                "plot_review_required": "TRUE" if output_kind.lower() in {"figure", "plot", "ggplot"} else "FALSE",
                "status": "draft",
                "notes": "Generated default case scaffold",
            }
        )
        for row in ordered_rows:
            link_rows.append(
                {
                    "case_id": default_case_id,
                    "function_name": function_name,
                    "parameter_name": row["parameter_name"],
                    "coverage_kind": "default_behavior",
                    "asserts_default_behavior": "TRUE",
                    "asserts_side_effects": "TRUE",
                    "asserts_ordering": "TRUE",
                    "asserts_plot_rendering": "TRUE" if output_kind.lower() in {"figure", "plot", "ggplot"} else "FALSE",
                    "notes": "Generated default-case link",
                }
            )

            parameter_case_id = f"{base_case_id}__param__{slugify(row['parameter_name'])}"
            case_rows.append(
                {
                    "case_id": parameter_case_id,
                    "function_name": function_name,
                    "case_kind": "parameter_focus",
                    "output_kind": output_kind,
                    "is_default_case": "FALSE",
                    "is_non_default_case": "TRUE",
                    "r_fixture_ref": "",
                    "python_fixture_ref": "",
                    "parameter_overrides": '{"<parameter>": "<non_default_value>"}',
                    "expected_side_effects": row["side_effect_contract"] or "Document parameter-specific side effects",
                    "plot_review_required": "TRUE" if output_kind.lower() in {"figure", "plot", "ggplot"} else "FALSE",
                    "status": "draft",
                    "notes": f"Generated explicit case for parameter {row['parameter_name']}",
                }
            )
            link_rows.append(
                {
                    "case_id": parameter_case_id,
                    "function_name": function_name,
                    "parameter_name": row["parameter_name"],
                    "coverage_kind": "explicit_parameter",
                    "asserts_default_behavior": "FALSE",
                    "asserts_side_effects": "TRUE",
                    "asserts_ordering": "TRUE",
                    "asserts_plot_rendering": "TRUE" if output_kind.lower() in {"figure", "plot", "ggplot"} else "FALSE",
                    "notes": "Generated explicit parameter coverage link",
                }
            )

        if output_kind.lower() in {"figure", "plot", "ggplot"}:
            plot_case_id = f"{base_case_id}__plot__non_default"
            case_rows.append(
                {
                    "case_id": plot_case_id,
                    "function_name": function_name,
                    "case_kind": "plot_non_default",
                    "output_kind": output_kind,
                    "is_default_case": "FALSE",
                    "is_non_default_case": "TRUE",
                    "r_fixture_ref": "",
                    "python_fixture_ref": "",
                    "parameter_overrides": '{"<plot_parameter>": "<non_default_value>"}',
                    "expected_side_effects": "Document axis, legend, facet, annotation, and ordering changes",
                    "plot_review_required": "TRUE",
                    "status": "draft",
                    "notes": "Generated mandatory non-default plot review case",
                }
            )
            for row in ordered_rows:
                link_rows.append(
                    {
                        "case_id": plot_case_id,
                        "function_name": function_name,
                        "parameter_name": row["parameter_name"],
                        "coverage_kind": "plot_render_review",
                        "asserts_default_behavior": "FALSE",
                        "asserts_side_effects": "TRUE",
                        "asserts_ordering": "TRUE",
                        "asserts_plot_rendering": "TRUE",
                        "notes": "Generated plot review link",
                    }
                )

    return case_rows, link_rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate parity case scaffolds from a function contract.")
    parser.add_argument("--contract", required=True, help="Path to FUNCTION_CONTRACT.csv")
    parser.add_argument("--output-cases", required=True, help="Path to write PARITY_CASES.csv")
    parser.add_argument("--output-links", required=True, help="Path to write PARAMETER_CASE_LINKS.csv")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    grouped = load_contract(Path(args.contract))
    case_rows, link_rows = build_rows(grouped)
    write_csv(Path(args.output_cases), CASE_COLUMNS, case_rows)
    write_csv(Path(args.output_links), LINK_COLUMNS, link_rows)


if __name__ == "__main__":
    main()
