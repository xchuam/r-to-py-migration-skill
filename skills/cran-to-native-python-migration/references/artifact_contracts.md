# Artifact Contracts

Use this reference when creating or reviewing migration artifacts. Prefer stable headings, explicit tables, and decision logs over narrative prose.

## General rules

- Update existing artifacts in place when possible.
- Record unknowns explicitly as `open question`, `not yet audited`, or `not present`.
- Include source evidence paths whenever practical.
- Separate observed behavior from proposed Python design.

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

## Stage 5 and later artifacts

### `API_MAPPING.md`

Recommended columns:

- `r_symbol`
- `python_symbol`
- `status`
- `signature_notes`
- `deviation_ref`

### `PARITY_REPORT.md`

Required sections:

- scope covered
- test evidence
- fixture evidence
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

### `RELEASE_CHECKLIST.md`

Required sections:

- metadata
- build and install
- tests
- docs
- CI
- license
- release notes
