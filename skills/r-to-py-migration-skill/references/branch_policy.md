# Branch Policy

Use this reference when planning migration work and deciding whether a branch is ready for promotion.

## Required branch model

- core migration branch: long-lived branch for shared migration scaffolding and reusable infrastructure
- version migration branch: branch for a specific upstream package version migration
- promotion branch: short-lived branch used to curate reviewer evidence before merge to `main`

## Suggested naming

- core migration branch: `migration/core`
- version migration branch: `migration/<package>/<r_version>`
- promotion branch: `promotion/<package>/<r_version>`

## Artifact placement policy

- Keep fixture capture, notebook outputs, raw R reference renders, and parity exploration files on migration branches.
- Keep merge-ready summaries, approved deviation notes, and curated promotion bundles on promotion branches.
- Do not mix raw exploratory migration artifacts with package-facing release notes or public package docs.

## Promotion gates

Move from version migration branch to promotion branch only when:

- `FUNCTION_CONTRACT.csv` is complete for modified public functions
- every public parameter has explicit case coverage
- parity report and coverage report are generated
- reviewer notebook is generated and readable
- deviations are logged and linked to tests
- package build and install checks are passing for the current scope

Move from promotion branch to `main` only when:

- promotion readiness checklist is complete
- reviewer-facing migration notes mention deviations
- branch contains curated evidence rather than raw exploratory clutter
- unresolved gaps are explicitly accepted and tracked
