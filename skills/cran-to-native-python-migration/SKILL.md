---
name: cran-to-native-python-migration
description: Use when migrating a general CRAN package into a native Python package and the work must preserve API parity, test parity, and data-model parity through a staged workflow. Enforces reference freeze, per-module migration classification into native rewrite or faithful port or temporary parity bridge, semantic audit, fixture capture, Python package scaffolding, parity testing, documented deviations, and release readiness.
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
- Migration-mode rules: `references/migration_modes.md`
- Semantic and fixture rules: `references/semantic_parity.md`
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
- `DEPENDENCY_MAP.md`
- `DATA_ASSET_INVENTORY.md`
- `COMPILED_CODE_INVENTORY.md`

Do not advance if exported API, tests, packaged data, or compiled code coverage is still unclear.

### Stage 2: Migration classification

Required outputs usually include:

- `MIGRATION_MODE_MAP.md`
- `PARITY_PRIORITY_MATRIX.md`

Every module or subsystem must have a mode and reason. Do not collapse `faithful port` into `native rewrite`.

### Stage 3: Python package scaffold

The target must be a real Python package. Prefer:

- `pyproject.toml`
- `src/` layout
- `tests/`
- dev and test extras

Always use `github/awesome-copilot/python-pypi-package-builder` together with this skill for this stage when that companion skill is available.

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

### Stage 5: Interface and test parity

Freeze Python stubs and pytest parity tests before full implementation.

### Stage 6: Implementation

Implement module by module according to the migration mode map. If behavior changes, update `DEVIATION_LOG.md` and `PARITY_REPORT.md`.

For packaging-facing implementation work, continue using `github/awesome-copilot/python-pypi-package-builder` alongside this skill.

### Stage 7: Docs sync

Rewrite documentation deliberately. Preserve intent, not roxygen phrasing.

### Stage 8: Release readiness

Verify build, install, test, metadata, license handling, CI, and wheel or sdist readiness.

Always use `github/awesome-copilot/python-pypi-package-builder` together with this skill for release-readiness work when available.

## Operating heuristics

- Prefer `native rewrite` when the public behavior can be preserved with clearer Python internals.
- Prefer `faithful port` when reproducibility risk is high or semantics are fragile.
- Use `temporary parity bridge` only to generate fixtures, compare behavior, or de-risk ambiguous semantics.
- Audit compiled code separately. Do not assume pure Python is acceptable for performance-critical paths.
- Convert testthat intent into pytest intent, not just syntax.
- Use deterministic tables, decision logs, and checklists over vague prose.

## Response style for migration work

When useful, structure outputs as:

1. what you found
2. risks
3. recommended edits
4. exact file changes
5. next highest-value improvement

Keep the work product reusable for future agents. Separate policy from examples and rules from heuristics.
