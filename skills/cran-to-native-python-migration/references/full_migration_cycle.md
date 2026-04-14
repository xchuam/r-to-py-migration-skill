# Full Migration Cycle

Use this reference for a standard end-to-end migration pass.

## Example workflow

1. Create or update the migration branch structure.
2. Scaffold the artifact set.
3. Freeze the public function contract.
4. Generate default parity cases and parameter links.
5. Capture fixtures and live R reference outputs.
6. Run contract and coverage checks.
7. Generate the reviewer notebook.
8. Implement and iterate until parity evidence is acceptable.
9. Prepare promotion branch artifacts.

## Example commands

Run from the migration repository root:

```bash
python3 scripts/scaffold_migration_artifacts.py --project-root . --python-package <package_name>
python3 scripts/generate_parity_case_templates.py --contract FUNCTION_CONTRACT.csv --output-cases PARITY_CASES.csv --output-links PARAMETER_CASE_LINKS.csv
python3 scripts/check_function_contracts.py --contract FUNCTION_CONTRACT.csv --output-json migration_artifacts/reference_outputs/function_contract_report.json
python3 scripts/generate_parameter_coverage_report.py --contract FUNCTION_CONTRACT.csv --cases PARITY_CASES.csv --links PARAMETER_CASE_LINKS.csv --output-csv migration_artifacts/reference_outputs/PARAMETER_COVERAGE_REPORT.csv --output-md migration_artifacts/reference_outputs/PARAMETER_COVERAGE_REPORT.md
python3 scripts/generate_manual_validation_notebook.py --package <package_name> --r-version <r_version> --contract FUNCTION_CONTRACT.csv --cases PARITY_CASES.csv --links PARAMETER_CASE_LINKS.csv --output migration_artifacts/notebooks/manual_validation_<r_version>.ipynb
```

## Required outputs before promotion

- contract check report
- parameter coverage report
- parity report
- deviation log
- reviewer notebook
- promotion readiness checklist
