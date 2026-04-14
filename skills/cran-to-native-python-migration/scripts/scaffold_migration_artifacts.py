#!/usr/bin/env python3
"""Scaffold standard artifacts for a CRAN-to-Python migration repository."""

from __future__ import annotations

import argparse
from pathlib import Path


TEMPLATES = {
    "R_PACKAGE_DOSSIER.md": """# R Package Dossier

## Package Identity

| Field | Value |
| --- | --- |
| Package | |
| Version | |
| Source repository | |
| License | |

## Audit Scope

| Surface | Status | Notes |
| --- | --- | --- |
| DESCRIPTION | not yet audited | |
| NAMESPACE | not yet audited | |
| R/ | not yet audited | |
| man/ | not yet audited | |
| tests/ | not yet audited | |
| vignettes/ | not yet audited | |
| data/ | not yet audited | |
| src/ | not yet audited | |

## Exported Surface Summary

## Internal Architecture Summary

## Dependency Summary

## Test Suite Summary

## Packaged Data Summary

## Compiled Code Summary

## Unresolved Questions
""",
    "EXPORTED_API.csv": """name,kind,source_file,arguments,defaults,return_contract,side_effects,examples_present,tests_present,notes
""",
    "FUNCTION_CONTRACT.csv": """r_function,python_function,output_kind,parameter_name,r_parameter_name,python_parameter_name,parameter_position,r_default,python_default,effective_default_match,documented_in_r,documented_in_python,side_effect_contract,deviation_id,notes
summary,summary,table,data,data,data,1,none,none,TRUE,TRUE,TRUE,row order and grouping behavior,,Example row: replace with real contract data
""",
    "DEPENDENCY_MAP.md": """# Dependency Map

## Imports by Package

| Dependency | Type | Used by | Notes |
| --- | --- | --- | --- |

## Suggested or Optional Dependencies

| Dependency | Why used | Migration impact |
| --- | --- | --- |

## Internal Helper Dependency Graph Summary

## Risk Notes
""",
    "DATA_ASSET_INVENTORY.md": """# Data Asset Inventory

| Asset Name | Type | Path | Shape or Length | Class or Structure | Used in Examples | Used in Tests | Migration Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
""",
    "COMPILED_CODE_INVENTORY.md": """# Compiled Code Inventory

| File | Language | Entry Points | Called From | Purpose | Performance Risk | Port Strategy Notes |
| --- | --- | --- | --- | --- | --- | --- |
""",
    "MIGRATION_MODE_MAP.md": """# Migration Mode Map

| Subsystem | Mode | Reason | Primary Parity Driver | Bridge Scope If Any | Exit Criteria |
| --- | --- | --- | --- | --- | --- |
""",
    "PARITY_PRIORITY_MATRIX.md": """# Parity Priority Matrix

| Subsystem | API Parity | Test Parity | Data-Model Parity | Risk Level | Blocking Unknowns |
| --- | --- | --- | --- | --- | --- |
""",
    "MIGRATION_BRANCH_POLICY.md": """# Migration Branch Policy

## Branches

- Core migration branch: `migration/core`
- Version migration branch: `migration/<package>/<r_version>`
- Promotion branch: `promotion/<package>/<r_version>`

## Migration Branch Artifacts

- keep fixtures, raw R renders, reference outputs, and notebooks under `migration_artifacts/`
- keep reviewer-facing promotion bundles under `promotion_artifacts/`

## Promotion Gates

- [ ] `FUNCTION_CONTRACT.csv` is complete for modified public functions.
- [ ] Every public parameter has explicit case coverage.
- [ ] Contract and coverage reports are generated.
- [ ] Reviewer notebook is generated for the current R version.
- [ ] Deviations are logged and linked to tests.
- [ ] Package build and install checks are green for the current scope.
""",
    "PACKAGE_TREE.txt": """<package-root>/
  pyproject.toml
  src/
    <python_package>/
      __init__.py
  tests/
  migration_artifacts/
    fixtures/
    notebooks/
    reference_outputs/
  promotion_artifacts/
  EXPECTED_OUTPUTS/
""",
    "DEV_ENV.md": """# Development Environment

## Supported Python Policy

## Local Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev,test,docs]
```

## Verification Commands

```bash
python3 -m pytest
python3 -m build
python3 scripts/check_function_contracts.py --contract FUNCTION_CONTRACT.csv --output-json migration_artifacts/reference_outputs/function_contract_report.json
python3 scripts/generate_parameter_coverage_report.py --contract FUNCTION_CONTRACT.csv --cases PARITY_CASES.csv --links PARAMETER_CASE_LINKS.csv --output-csv migration_artifacts/reference_outputs/PARAMETER_COVERAGE_REPORT.csv --output-md migration_artifacts/reference_outputs/PARAMETER_COVERAGE_REPORT.md
```
""",
    "SEMANTIC_RULES.md": """# Semantic Rules

## Missing-Value Rules

## Scalar Versus Vector Rules

## Categorical Handling

## Indexing Conventions

## Attribute and Class Preservation

## Formula and NSE Handling

## Matrix and Tabular Shape Rules

## Plotting Semantics
""",
    "TYPE_MAPPING.md": """# Type Mapping

| R Type or Class | Python Target | Loss Risk | Notes |
| --- | --- | --- | --- |
""",
    "FIXTURE_CATALOG.md": """# Fixture Catalog

| Fixture Name | Source | Covers Behavior | Format | Generation Method | Owner Stage |
| --- | --- | --- | --- | --- | --- |
""",
    "EDGE_CASE_MATRIX.md": """# Edge Case Matrix

| Case | Source Behavior | Python Expectation | Test Location | Status |
| --- | --- | --- | --- | --- |
""",
    "PARITY_CASES.csv": """case_id,function_name,case_kind,output_kind,is_default_case,is_non_default_case,r_fixture_ref,python_fixture_ref,parameter_overrides,expected_side_effects,plot_review_required,status,notes
summary__defaults,summary,default,table,TRUE,FALSE,,,{},row order and default grouping,FALSE,draft,Example row: replace with real cases
""",
    "PARAMETER_CASE_LINKS.csv": """case_id,function_name,parameter_name,coverage_kind,asserts_default_behavior,asserts_side_effects,asserts_ordering,asserts_plot_rendering,notes
summary__defaults,summary,data,default_behavior,TRUE,FALSE,TRUE,FALSE,Example row: replace with real links
""",
    "API_MAPPING.md": """# API Mapping

| R Symbol | Python Symbol | Status | Signature Notes | Deviation Ref |
| --- | --- | --- | --- | --- |
| summary | summary | planned | Preserve public name and parameter order | |
""",
    "PARITY_REPORT.md": """# Parity Report

## Scope Covered

## Test Evidence

## Fixture Evidence

## Live R Comparison Evidence

## Manual Notebook Evidence

## Known Gaps

## Status by Subsystem
""",
    "DEVIATION_LOG.md": """# Deviation Log

| ID | Scope | Description | Reason | Parity Constraint Tradeoff | User Approved | Status |
| --- | --- | --- | --- | --- | --- | --- |
""",
    "FUNCTION_PARAMETER_REVIEW_CHECKLIST.md": """# Function Parameter Review Checklist

## Coverage Summary

- [ ] `FUNCTION_CONTRACT.csv` is complete for modified public functions.
- [ ] `PARITY_CASES.csv` is complete for modified public functions.
- [ ] `PARAMETER_CASE_LINKS.csv` covers every public parameter.
- [ ] Generated coverage report shows no uncovered parameters.

## Per-Function Review

### `<function_name>`

- [ ] Public function name matches R export name, or deviation is logged.
- [ ] Parameter names match R, or deviations are logged.
- [ ] Parameter order matches R, or deviations are logged.
- [ ] Effective defaults match R behavior, or deviations are logged.
- [ ] Warnings and side effects are checked.
- [ ] Structured output comparisons are captured.
- [ ] Plot review is captured if the function renders figures.

## Reviewer Notes

## Unresolved Gaps
""",
    "MIGRATION_RUNBOOK.md": """# Migration Runbook

## Branch Setup

1. Create or update `migration/core` for shared migration infrastructure.
2. Create `migration/<package>/<r_version>` for the target package version.
3. Reserve `promotion/<package>/<r_version>` for reviewer-facing promotion.

## Artifact Setup

```bash
python3 scripts/scaffold_migration_artifacts.py --project-root . --python-package <package_name>
python3 scripts/generate_parity_case_templates.py --contract FUNCTION_CONTRACT.csv --output-cases PARITY_CASES.csv --output-links PARAMETER_CASE_LINKS.csv
```

## Verification Cycle

```bash
python3 scripts/check_function_contracts.py --contract FUNCTION_CONTRACT.csv --output-json migration_artifacts/reference_outputs/function_contract_report.json
python3 scripts/generate_parameter_coverage_report.py --contract FUNCTION_CONTRACT.csv --cases PARITY_CASES.csv --links PARAMETER_CASE_LINKS.csv --output-csv migration_artifacts/reference_outputs/PARAMETER_COVERAGE_REPORT.csv --output-md migration_artifacts/reference_outputs/PARAMETER_COVERAGE_REPORT.md
python3 scripts/generate_manual_validation_notebook.py --package <package_name> --r-version <r_version> --contract FUNCTION_CONTRACT.csv --cases PARITY_CASES.csv --links PARAMETER_CASE_LINKS.csv --output migration_artifacts/notebooks/manual_validation_<r_version>.ipynb
```

## Promotion Handoff

- [ ] Reviewer notebook is generated.
- [ ] Promotion readiness checklist is complete.
- [ ] Deviations are mentioned in migration notes.
""",
    "PROMOTION_READINESS_CHECKLIST.md": """# Promotion Readiness Checklist

## Branch Prerequisites

- [ ] Work is on `promotion/<package>/<r_version>`.
- [ ] Raw exploratory artifacts remain on the migration branch.

## Parity Evidence

- [ ] Function contract check report is green.
- [ ] Parameter coverage report shows no uncovered parameters.
- [ ] Live R reference outputs are captured for modified public functions.
- [ ] Plot review exists for all modified plotting functions.
- [ ] Reviewer notebook is version-scoped and complete.

## Deviations

- [ ] Every deviation has a log entry.
- [ ] Every deviation has a focused test.
- [ ] Every deviation is mentioned in migration notes.

## Package Checks

- [ ] Build and install checks pass.
- [ ] Test suite passes for migration scope.
- [ ] Packaging metadata is promotion-ready.

## Merge Decision

- [ ] Promotion bundle is reviewer-ready.
- [ ] Remaining risks are explicitly recorded.
- [ ] Branch is ready to merge to `main`.
""",
    "RELEASE_CHECKLIST.md": """# Release Checklist

## Metadata

- [ ] Name, version, and license metadata are complete.
- [ ] Python version policy is explicit.

## Build and Install

- [ ] `python3 -m build` succeeds.
- [ ] Editable install succeeds.

## Tests

- [ ] Pytest parity suite passes.
- [ ] Fixture-backed comparisons are documented.
- [ ] Parameter coverage report shows no gaps.

## Docs

- [ ] README reflects actual Python usage.
- [ ] Deviations are documented.

## CI

- [ ] CI validates build and tests.

## License

- [ ] License handling is reviewed for the source package and Python package.

## Release Notes

- [ ] Draft notes are prepared.
""",
    "pyproject.toml": """[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "<python-package>"
version = "0.1.0"
description = "Python migration target for a CRAN package"
readme = "README.md"
requires-python = ">=3.10"
dependencies = []

[project.optional-dependencies]
dev = []
test = ["pytest>=8"]
docs = []

[tool.pytest.ini_options]
testpaths = ["tests"]
""",
}


DIRS = [
    "EXPECTED_OUTPUTS",
    "src",
    "tests",
    "migration_artifacts/fixtures",
    "migration_artifacts/notebooks",
    "migration_artifacts/reference_outputs",
    "promotion_artifacts",
]


def build_init(package_name: str) -> str:
    return '"""Python migration target package."""\n'


def materialize(template: str, package_name: str) -> str:
    return template.replace("<python_package>", package_name).replace(
        "<python-package>", package_name.replace("_", "-")
    )


def write_file(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scaffold standard artifacts for a CRAN-to-Python migration."
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="Directory where the migration artifacts should be created.",
    )
    parser.add_argument(
        "--python-package",
        required=True,
        help="Import package name for the Python target package.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.project_root).resolve()
    package_name = args.python_package

    for relative_dir in DIRS:
        (root / relative_dir).mkdir(parents=True, exist_ok=True)
        write_file(root / relative_dir / ".gitkeep", "", args.force)

    for filename, template in TEMPLATES.items():
        write_file(root / filename, materialize(template, package_name), args.force)

    write_file(
        root / "src" / package_name / "__init__.py",
        build_init(package_name),
        args.force,
    )
    write_file(root / "tests" / ".gitkeep", "", args.force)


if __name__ == "__main__":
    main()
