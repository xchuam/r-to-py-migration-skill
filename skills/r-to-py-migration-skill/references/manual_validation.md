# Manual Validation

Use this reference when generating or reviewing the mandatory reviewer notebook.

## Notebook policy

- The manual validation notebook is a required reviewer artifact for modified public functions.
- The notebook should be version-scoped, for example `migration_artifacts/notebooks/manual_validation_<r_version>.ipynb`.
- Generate the notebook from machine-readable artifacts instead of hand-writing ad hoc sections.

## Required notebook structure

The notebook must include:

- setup and fixture-loading section
- generated parity case table
- generated parameter coverage table
- one section per modified public function
- R reference snapshot for each function
- Python output for each function
- comparison output for each function
- side-by-side visual review for plotting functions
- short pass or fail status cell per function family

## Reviewer expectations

- Reviewers should be able to see which case IDs support which parameter claims.
- Plot reviews should show both default and non-default renders.
- Notebook cells should clearly separate observed differences from accepted deviations.
- If a function is incomplete, the notebook should say so explicitly rather than omitting it.

## Good notebook signals

- generated tables, not manually curated lists
- links or references back to fixture files
- explicit case IDs
- explicit deviation IDs where relevant
- compact pass or fail summary near the top
