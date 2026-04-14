# Artifact Contracts

Use this reference when creating or reviewing migration artifacts. Prefer stable headings, explicit tables, and decision logs over narrative prose.

## General rules

- Update existing artifacts in place when possible.
- Record unknowns explicitly as `open question`, `not yet audited`, or `not present`.
- Include source evidence paths whenever practical.
- Separate observed behavior from proposed Python design.
- Prefer machine-readable CSV or JSON for contracts, case inventories, and coverage links.
- Keep migration evidence under `migration_artifacts/` and promotion-ready reviewer bundles under `promotion_artifacts/`.

## Stage 1 artifacts

### `R_PACKAGE_DOSSIER.md`

Required sections:

- package identity and version
- audit scope
- exported surface summary
- internal architecture summary
- dependency summary
- test suite summary
- packaged data summary
- compiled code summary
- unresolved questions

### `EXPORTED_API.csv`

Recommended columns:

- `name`
- `kind`
- `source_file`
- `arguments`
- `defaults`
- `return_contract`
- `side_effects`
- `examples_present`
- `tests_present`
- `notes`

### `FUNCTION_CONTRACT.csv`

One row per public parameter. This is the function-level parity contract and should be treated as a blocking artifact for implementation.

Recommended columns:

- `r_function`
- `python_function`
- `output_kind`
- `parameter_name`
- `r_parameter_name`
- `python_parameter_name`
- `parameter_position`
- `r_default`
- `python_default`
- `effective_default_match`
- `documented_in_r`
- `documented_in_python`
- `side_effect_contract`
- `deviation_id`
- `notes`

### `DEPENDENCY_MAP.md`

Required sections:

- Imports by package
- Suggested or optional dependencies
- Internal helper dependency graph summary
- Risk notes for heavy or semantically important dependencies

### `DATA_ASSET_INVENTORY.md`

Recommended columns:

- `asset_name`
- `type`
- `path`
- `shape_or_length`
- `class_or_structure`
- `used_in_examples`
- `used_in_tests`
- `migration_notes`

### `COMPILED_CODE_INVENTORY.md`

Recommended columns:

- `file`
- `language`
- `entry_points`
- `called_from`
- `purpose`
- `performance_risk`
- `port_strategy_notes`

## Stage 2 artifacts

### `MIGRATION_MODE_MAP.md`

Recommended columns:

- `subsystem`
- `mode`
- `reason`
- `primary_parity_driver`
- `bridge_scope_if_any`
- `exit_criteria`

### `PARITY_PRIORITY_MATRIX.md`

Recommended columns:

- `subsystem`
- `api_parity`
- `test_parity`
- `data_model_parity`
- `risk_level`
- `blocking_unknowns`

### `MIGRATION_BRANCH_POLICY.md`

Required sections:

- core migration branch naming
- version migration branch naming
- promotion branch naming
- which artifacts live on migration branches
- promotion gates before merge to `main`

## Stage 4 artifacts

### `SEMANTIC_RULES.md`

Required sections:

- missing-value rules
- scalar versus vector rules
- categorical handling
- indexing conventions
- attribute or class preservation
- formula or NSE handling
- matrix or tabular shape rules

### `TYPE_MAPPING.md`

Recommended columns:

- `r_type_or_class`
- `python_target`
- `loss_risk`
- `notes`

### `FIXTURE_CATALOG.md`

Recommended columns:

- `fixture_name`
- `source`
- `covers_behavior`
- `format`
- `generation_method`
- `owner_stage`

### `EDGE_CASE_MATRIX.md`

Recommended columns:

- `case`
- `source_behavior`
- `python_expectation`
- `test_location`
- `status`

### `PARITY_CASES.csv`

One row per explicit parity case.

Recommended columns:

- `case_id`
- `function_name`
- `case_kind`
- `output_kind`
- `is_default_case`
- `is_non_default_case`
- `r_fixture_ref`
- `python_fixture_ref`
- `parameter_overrides`
- `expected_side_effects`
- `plot_review_required`
- `status`
- `notes`

### `PARAMETER_CASE_LINKS.csv`

Recommended columns:

- `case_id`
- `function_name`
- `parameter_name`
- `coverage_kind`
- `asserts_default_behavior`
- `asserts_side_effects`
- `asserts_ordering`
- `asserts_plot_rendering`
- `notes`

## Stage 5 and later artifacts

### `API_MAPPING.md`

Recommended columns:

- `r_symbol`
- `python_symbol`
- `status`
- `signature_notes`
- `deviation_ref`

Name mapping rule:

- `python_symbol` should match `r_symbol` by default for public functions unless a deviation is logged and approved.

### `PARITY_REPORT.md`

Required sections:

- scope covered
- test evidence
- fixture evidence
- live R comparison evidence
- manual notebook evidence
- known gaps
- status by subsystem

### `DEVIATION_LOG.md`

Recommended columns:

- `id`
- `scope`
- `description`
- `reason`
- `parity_constraint_tradeoff`
- `user_approved`
- `status`

Deviation rule:

- every approximation or intentional difference must reference a focused test and reviewer-facing migration note

### `FUNCTION_PARAMETER_REVIEW_CHECKLIST.md`

Required sections:

- coverage summary
- one checklist block per public function
- one checklist item per public parameter
- reviewer sign-off notes
- unresolved parity gaps

### `PARAMETER_COVERAGE_REPORT.csv` and `PARAMETER_COVERAGE_REPORT.md`

These are generated artifacts derived from `FUNCTION_CONTRACT.csv`, `PARITY_CASES.csv`, and `PARAMETER_CASE_LINKS.csv`.

Recommended columns for the CSV:

- `r_function`
- `python_function`
- `parameter_name`
- `parameter_position`
- `required_case_count`
- `covered_case_ids`
- `side_effect_contract`
- `status`
- `gap_notes`

### Version-scoped manual validation notebook

Store under `migration_artifacts/notebooks/`.

Required contents:

- setup and fixture-loading section
- generated parity case and coverage tables
- one section per modified public function
- R reference snapshot, Python output, and comparison output for each function
- side-by-side visual review for plotting functions
- short pass/fail status cell per function family

### `MIGRATION_RUNBOOK.md`

Required sections:

- branch setup
- fixture capture workflow
- contract and coverage commands
- notebook generation
- promotion handoff

### `PROMOTION_READINESS_CHECKLIST.md`

Required sections:

- branch prerequisites
- parity evidence complete
- deviations reviewed
- package build checks
- promotion bundle ready
- merge-to-main decision

### `RELEASE_CHECKLIST.md`

Required sections:

- metadata
- build and install
- tests
- docs
- CI
- license
- release notes
