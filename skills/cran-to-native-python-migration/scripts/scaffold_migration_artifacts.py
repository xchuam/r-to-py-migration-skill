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
    "PACKAGE_TREE.txt": """<package-root>/
  pyproject.toml
  src/
    <python_package>/
      __init__.py
  tests/
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
    "API_MAPPING.md": """# API Mapping

| R Symbol | Python Symbol | Status | Signature Notes | Deviation Ref |
| --- | --- | --- | --- | --- |
""",
    "PARITY_REPORT.md": """# Parity Report

## Scope Covered

## Test Evidence

## Fixture Evidence

## Known Gaps

## Status by Subsystem
""",
    "DEVIATION_LOG.md": """# Deviation Log

| ID | Scope | Description | Reason | Parity Constraint Tradeoff | User Approved | Status |
| --- | --- | --- | --- | --- | --- | --- |
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

    write_file(root / "EXPECTED_OUTPUTS" / ".gitkeep", "", args.force)

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
