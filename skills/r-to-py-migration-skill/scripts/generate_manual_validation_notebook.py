#!/usr/bin/env python3
"""Generate a version-scoped manual validation notebook scaffold."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


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


def to_json(value: object, indent: int = 0) -> str:
    spacer = " " * indent
    child_indent = indent + 2
    child_spacer = " " * child_indent

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
        if not value:
            return "[]"
        body = ",\n".join(f"{child_spacer}{to_json(item, child_indent)}" for item in value)
        return "[\n" + body + "\n" + spacer + "]"
    if isinstance(value, dict):
        if not value:
            return "{}"
        body = ",\n".join(
            f"{child_spacer}{to_json(str(key))}: {to_json(item, child_indent)}"
            for key, item in value.items()
        )
        return "{\n" + body + "\n" + spacer + "}"
    raise TypeError(f"Unsupported JSON value: {type(value)!r}")


def markdown_cell(text: str) -> dict[str, object]:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.splitlines()],
    }


def code_cell(code: str) -> dict[str, object]:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in code.splitlines()],
    }


def build_notebook(
    package_name: str,
    r_version: str,
    contract_rows: list[dict[str, str]],
    case_rows: list[dict[str, str]],
    link_rows: list[dict[str, str]],
) -> dict[str, object]:
    functions: dict[str, list[dict[str, str]]] = defaultdict(list)
    cases_by_function: dict[str, list[dict[str, str]]] = defaultdict(list)
    links_by_function: dict[str, list[dict[str, str]]] = defaultdict(list)

    for row in contract_rows:
        functions[row["r_function"]].append(row)
    for row in case_rows:
        cases_by_function[row["function_name"]].append(row)
    for row in link_rows:
        links_by_function[row["function_name"]].append(row)

    cells = [
        markdown_cell(
            f"# Manual Validation Notebook\n\nPackage: `{package_name}`\n\nR version scope: `{r_version}`"
        ),
        markdown_cell(
            "## Reviewer Checklist\n\n"
            "- This notebook is a mandatory reviewer artifact.\n"
            "- Every modified public function should appear below.\n"
            "- Every public parameter should map to at least one case ID.\n"
            "- Plotting functions require side-by-side visual review."
        ),
        code_cell(
            "from pathlib import Path\n"
            "import pandas as pd\n\n"
            "ROOT = Path('.')\n"
            "contract = pd.read_csv(ROOT / 'FUNCTION_CONTRACT.csv')\n"
            "cases = pd.read_csv(ROOT / 'PARITY_CASES.csv')\n"
            "links = pd.read_csv(ROOT / 'PARAMETER_CASE_LINKS.csv')\n"
            "contract.head()"
        ),
        markdown_cell("## Status Summary"),
        code_cell(
            "summary = (\n"
            "    links.groupby('function_name')['parameter_name']\n"
            "    .nunique()\n"
            "    .rename('covered_parameters')\n"
            "    .to_frame()\n"
            ")\n"
            "total = contract.groupby('r_function')['parameter_name'].nunique().rename('total_parameters')\n"
            "status = total.to_frame().join(summary, how='left').fillna(0)\n"
            "status['result'] = status.apply(\n"
            "    lambda row: 'pass' if int(row['covered_parameters']) >= int(row['total_parameters']) else 'fail',\n"
            "    axis=1,\n"
            ")\n"
            "status"
        ),
        markdown_cell("## Generated Parity Case Table"),
        code_cell("cases.sort_values(['function_name', 'case_id'])"),
        markdown_cell("## Generated Parameter Coverage Table"),
        code_cell("links.sort_values(['function_name', 'parameter_name', 'case_id'])"),
    ]

    for function_name in sorted(functions):
        output_kind = functions[function_name][0]["output_kind"]
        function_cases = sorted(cases_by_function[function_name], key=lambda row: row["case_id"])
        function_links = sorted(
            links_by_function[function_name], key=lambda row: (row["parameter_name"], row["case_id"])
        )
        cells.extend(
            [
                markdown_cell(f"## Function: `{function_name}`"),
                markdown_cell(
                    "### Function Contract\n\n"
                    f"- Output kind: `{output_kind}`\n"
                    f"- Parameters: `{', '.join(row['parameter_name'] for row in sorted(functions[function_name], key=lambda item: int(item['parameter_position'])) )}`"
                ),
                code_cell(
                    f"contract.query(\"r_function == '{function_name}'\").sort_values('parameter_position')",
                ),
                markdown_cell("### Case Coverage"),
                code_cell(
                    f"cases.query(\"function_name == '{function_name}'\").sort_values('case_id')",
                ),
                code_cell(
                    f"links.query(\"function_name == '{function_name}'\").sort_values(['parameter_name', 'case_id'])",
                ),
                markdown_cell("### R Reference Snapshot"),
                code_cell(
                    "# Replace with code or artifact loading for live R reference output\n"
                    f"r_reference_path = Path('migration_artifacts/reference_outputs/{function_name}_r_reference.json')\n"
                    "r_reference_path"
                ),
                markdown_cell("### Python Output"),
                code_cell(
                    "# Replace with code or artifact loading for Python output\n"
                    f"python_output_path = Path('migration_artifacts/reference_outputs/{function_name}_python_output.json')\n"
                    "python_output_path"
                ),
                markdown_cell("### Comparison Output"),
                code_cell(
                    "# Replace with a concrete comparison step for this function family\n"
                    "comparison_result = {\n"
                    "    'status': 'pending',\n"
                    f"    'case_ids': {[row['case_id'] for row in function_cases]},\n"
                    "}\n"
                    "comparison_result"
                ),
            ]
        )
        if output_kind.lower() in {"figure", "plot", "ggplot"}:
            cells.extend(
                [
                    markdown_cell("### Side-by-Side Plot Review"),
                    code_cell(
                        "# Replace with rendered R and Python plot display\n"
                        f"r_plot = Path('migration_artifacts/reference_outputs/{function_name}_r_plot.png')\n"
                        f"py_plot = Path('migration_artifacts/reference_outputs/{function_name}_python_plot.png')\n"
                        "r_plot, py_plot"
                    ),
                ]
            )
        cells.append(
            markdown_cell(
                "### Status\n\n- Result: `pending`\n- Reviewer notes: \n- Linked case IDs: "
                + ", ".join(row["case_id"] for row in function_cases)
            )
        )

    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3.x"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a manual validation notebook scaffold.")
    parser.add_argument("--package", required=True, help="Package name under migration")
    parser.add_argument("--r-version", required=True, help="Upstream R package version")
    parser.add_argument("--contract", required=True, help="Path to FUNCTION_CONTRACT.csv")
    parser.add_argument("--cases", required=True, help="Path to PARITY_CASES.csv")
    parser.add_argument("--links", required=True, help="Path to PARAMETER_CASE_LINKS.csv")
    parser.add_argument("--output", required=True, help="Notebook path to write")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    notebook = build_notebook(
        args.package,
        args.r_version,
        read_csv(Path(args.contract)),
        read_csv(Path(args.cases)),
        read_csv(Path(args.links)),
    )
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(to_json(notebook, indent=0) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
