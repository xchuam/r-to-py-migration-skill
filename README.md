# R Package to Python Package Migration Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)
[![GitHub stars](https://img.shields.io/github/stars/xchuam/r-to-py-migration-skill?style=social)](https://github.com/xchuam/r-to-py-migration-skill)

A reusable agent skill for migrating a general R CRAN package into a real Python package without losing behavioral fidelity.

This repository is for structured migration work, not blind syntax conversion. The skill treats the R package as the specification, freezes the reference surface before implementation, and enforces strict reusable parity discipline through machine-readable function contracts, parameter coverage, live R comparisons, reviewer notebooks, and explicit deviation tracking.

The skill enforces three parity constraints throughout the migration:

- API parity
- test parity
- data-model parity

## What This Skill Does

This skill guides agents through an eight-stage migration workflow:

1. Reference freeze and audit
2. Migration classification
3. Python package scaffold
4. Semantic normalization and fixture capture
5. Interface and test parity
6. Implementation
7. Documentation sync
8. Release readiness

For each module or subsystem, the skill requires an explicit migration mode:

- `native rewrite`
- `faithful port`
- `temporary parity bridge`

That distinction is core to the repo. The skill is designed to prevent silent semantic drift in areas like missing values, factors, integer-vs-float preservation, vector recycling, indexing, attributes, formulas, and compiled code.

## Strict Parity Artifacts

This skill expects these artifacts as first-class migration evidence:

- `FUNCTION_CONTRACT.csv` for public function names, parameter names, order, and effective defaults
- `PARITY_CASES.csv` and `PARAMETER_CASE_LINKS.csv` for parameter-by-parameter case coverage
- generated parameter coverage reports so every public parameter is explicitly exercised
- a version-scoped manual validation Jupyter notebook such as `migration_artifacts/notebooks/manual_validation_<r_version>.ipynb`, with R reference output, Python output, comparison output, and plot review where applicable
- promotion-readiness and deviation artifacts before merge to `main`

## Install The Skill

Recommended: install through the `skills.sh` ecosystem.

Run this in your shell:

```bash
npx skills add xchuam/r-to-py-migration-skill
```

## Install The Required Companion Skill

This migration skill should be used together with [`github/awesome-copilot/python-pypi-package-builder`](https://github.com/github/awesome-copilot/blob/main/skills/python-pypi-package-builder/SKILL.md) for Python package scaffolding, packaging metadata, and release-readiness work.

Run this in your shell:

```bash
npx skills add github/awesome-copilot --skill python-pypi-package-builder
```

## Use The Skill

Once installed, invoke the skill from the agent chat.

Type something like this in chat:

```text
Use cran-to-native-python-migration and github/awesome-copilot/python-pypi-package-builder for this migration.
```

Use shell commands only for installation or file-copy steps. Use chat messages to tell the agent which skill or companion skill to use for the actual migration work.

Good use cases:

- freezing the exported R reference surface before any implementation
- building audit artifacts such as `R_PACKAGE_DOSSIER.md`, `EXPORTED_API.csv`, and `FUNCTION_CONTRACT.csv`
- classifying modules into rewrite, faithful port, or parity bridge
- translating testthat coverage into pytest parity coverage
- generating parameter coverage reports and manual validation Jupyter notebooks
- scaffolding the Python package, parity fixtures, and promotion/release checklists

Poor use cases:

- line-by-line syntax conversion
- claiming parity without tests or fixtures
- skipping packaged data, examples, or compiled code
- collapsing faithful port and native rewrite into the same plan

## License

This repository is licensed under the MIT License. See [LICENSE](./LICENSE).
