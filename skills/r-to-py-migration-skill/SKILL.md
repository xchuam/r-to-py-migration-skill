---
name: r-to-py-migration-skill
description: Use when migrating an R or CRAN package to Python. Audits the R package first, preserves API, test, and data-model behavior, and produces a real Python package with parity checks and documented deviations.
license: MIT
---

# CRAN to Native Python Migration

Use this skill for repository work whose goal is to migrate a general CRAN package into a real Python package.

Do not use this skill for blind syntax conversion, code golf, or superficial "R to Python translation" requests that skip package audit and parity controls.

## Default stance

- Treat the R package as the behavioral specification first.
- Default migration style is `native rewrite`.
- Reclassify each module or subsystem into exactly one mode:
  - `native rewrite`
  - `faithful port`
  - `temporary parity bridge`
- Preserve external behavior unless a deviation is explicitly documented and justified.
- Prefer Pythonic internals only when API parity, test parity, and data-model parity remain intact.

## Non-negotiable constraints

- Never do blind line-by-line syntax translation.
- Never start implementation before the R package reference surface is frozen.
- Never claim parity without pytest coverage, fixtures, or both.
- Never ignore packaged data, examples, tests, or compiled code in the audit.
- Never silently change missing-value, categorical, recycling, indexing, attribute, or formula semantics.
- Never change public function naming, parameter naming, parameter order, or effective defaults without an explicit deviation entry.
- Never leave a public parameter without at least one explicit parity case.
- Never treat warnings, grouping behavior, output ordering, save paths, sizing options, or plot layout behavior as out-of-scope.
- Never promote a migration branch without a reviewer-facing manual validation notebook and parameter coverage report.

## Companion skill

Always use this skill together with the Python packaging companion skill once the migration reaches Python package construction, implementation packaging, or release-readiness work.

Required companion skill:

- `github/awesome-copilot/python-pypi-package-builder`

Use the companion skill for:

- `pyproject.toml` and packaging metadata refinement
- `src/` layout and import-package polish
- build and install verification
- CI and release-readiness packaging tasks

This skill remains the source of truth for behavioral parity and migration-stage ordering.

If the required companion skill is unavailable in the current environment, say that explicitly and then continue with the closest equivalent packaging workflow rather than silently omitting those steps.

## First move

Inspect the source package surface before proposing implementation. At minimum, inspect:

- `DESCRIPTION`
- `NAMESPACE`
- `R/`
- `man/`
- `tests/`
- `vignettes/`
- `data/`
- `src/`

If any of these are absent, record that explicitly instead of assuming they are irrelevant.

If the user asks for implementation immediately, still freeze the reference surface first unless they explicitly override that workflow.

Before implementation planning, freeze the public function contract in a machine-readable form. At minimum, capture:

- exact exported R function name
- intended Python public function name
- parameter names
- parameter order
- documented defaults
- effective defaults after wrapper behavior
- output kind
- parameter-side effects and behavioral notes

## Stage workflow

Follow the staged workflow below unless the user explicitly redirects it.

1. Stage 1: reference freeze and audit
2. Stage 2: migration classification
3. Stage 3: Python package scaffold
4. Stage 4: semantic normalization and fixture capture
5. Stage 5: interface and test parity
6. Stage 6: implementation
7. Stage 7: docs sync
8. Stage 8: release readiness

Before each substantial edit, state which stage or stages the task belongs to.

When making a decision, state which parity constraint is driving it:

- API parity
- test parity
- data-model parity

## Required artifact behavior

When artifacts are missing, create them in a structured and reusable format. When artifacts already exist, update them instead of duplicating them.

Read these references as needed:

- Artifact definitions and required sections: `references/artifact_contracts.md`
- Function contract and parameter parity rules: `references/function_parity.md`
- Migration-mode rules: `references/migration_modes.md`
- Semantic and fixture rules: `references/semantic_parity.md`
- Manual validation notebook and live parity review rules: `references/manual_validation.md`
- Branch model and promotion policy: `references/branch_policy.md`
- Full migration cycle and example commands: `references/full_migration_cycle.md`
- Common failure modes and review prompts: `references/failure_modes.md`
- Stage gates and execution order: `references/workflow.md`

If the repository needs a fresh migration artifact set, run:

```bash
python3 scripts/scaffold_migration_artifacts.py --project-root . --python-package <package_name>
```

## Stage gates

### Stage 1: Reference freeze and audit

Required outputs usually include:

- `R_PACKAGE_DOSSIER.md`
- `EXPORTED_API.csv`
- `FUNCTION_CONTRACT.csv`
- `DEPENDENCY_MAP.md`
- `DATA_ASSET_INVENTORY.md`
- `COMPILED_CODE_INVENTORY.md`

Do not advance if exported API, tests, packaged data, compiled code coverage, or public parameter contracts are still unclear.

### Stage 2: Migration classification

Required outputs usually include:

- `MIGRATION_MODE_MAP.md`
- `PARITY_PRIORITY_MATRIX.md`
- `MIGRATION_BRANCH_POLICY.md`

Every module or subsystem must have a mode and reason. Do not collapse `faithful port` into `native rewrite`.

### Stage 3: Python package scaffold

The target must be a real Python package. Prefer:

- `pyproject.toml`
- `src/` layout
- `tests/`
- dev and test extras

Always use `github/awesome-copilot/python-pypi-package-builder` together with this skill for this stage when that companion skill is available.

Keep migration evidence separate from promotion-ready package artifacts. Prefer:

- `migration_artifacts/` for fixtures, notebooks, reference outputs, and parity reports
- `promotion_artifacts/` for reviewer-facing promotion bundles and merge-ready summaries

### Stage 4: Semantic normalization and fixture capture

Make the data model explicit before implementation. Cover at least:

- vectors
- `data.frame` or tibble equivalents
- factors
- lists and named lists
- attributes and class semantics
- formulas or NSE
- missing-value handling
- matrix orientation and shapes

Required outputs usually include:

- `PARITY_CASES.csv`
- `PARAMETER_CASE_LINKS.csv`
- `FIXTURE_CATALOG.md`
- `EDGE_CASE_MATRIX.md`

For plotting functions, include both default and non-default parity cases and capture render references from live R output.

### Stage 5: Interface and test parity

Freeze Python stubs and pytest parity tests before full implementation.

Required outputs usually include:

- `FUNCTION_PARAMETER_REVIEW_CHECKLIST.md`
- machine-readable parameter coverage report
- version-scoped manual validation notebook under `migration_artifacts/notebooks/`

Every public parameter must be linked to at least one explicit parity case. Treat uncovered parameters as blockers.

### Stage 6: Implementation

Implement module by module according to the migration mode map. If behavior changes, update `DEVIATION_LOG.md` and `PARITY_REPORT.md`.

For packaging-facing implementation work, continue using `github/awesome-copilot/python-pypi-package-builder` alongside this skill.

Result parity is broader than return values alone:

- compare row counts, column order, values, metadata fields, and ordering assumptions for structured outputs
- compare warnings and side effects where they are public behavior
- compare plot units, labels, ranges, facets, legends, colors, annotation placement, and panel ordering for figures

### Stage 7: Docs sync

Rewrite documentation deliberately. Preserve intent, not roxygen phrasing.

### Stage 8: Release readiness

Verify build, install, test, metadata, license handling, CI, and wheel or sdist readiness.

Always use `github/awesome-copilot/python-pypi-package-builder` together with this skill for release-readiness work when available.

Do not merge directly from a migration branch to `main`. Follow the branch policy and promotion gates in `references/branch_policy.md`.

## Operating heuristics

- Prefer `native rewrite` when the public behavior can be preserved with clearer Python internals.
- Prefer `faithful port` when reproducibility risk is high or semantics are fragile.
- Use `temporary parity bridge` only to generate fixtures, compare behavior, or de-risk ambiguous semantics.
- Audit compiled code separately. Do not assume pure Python is acceptable for performance-critical paths.
- Convert testthat intent into pytest intent, not just syntax.
- Use deterministic tables, decision logs, and checklists over vague prose.
- Treat automated checks as first-class evidence and manual notebook review as required secondary evidence.
- If parity cannot be exact, require explicit deviation documentation, a focused test that encodes the expected difference, and reviewer-facing mention in migration notes.

## Response style for migration work

When useful, structure outputs as:

1. what you found
2. risks
3. recommended edits
4. exact file changes
5. next highest-value improvement

Keep the work product reusable for future agents. Separate policy from examples and rules from heuristics.
