# Promotion Readiness Checklist Template

## Branch Prerequisites

- [ ] Promotion branch is created from the version migration branch.
- [ ] Raw exploratory artifacts remain on the migration branch.

## Parity Evidence

- [ ] Function contract report is green.
- [ ] Parameter coverage report shows no uncovered parameters.
- [ ] Reviewer notebook is complete and version-scoped.
- [ ] Live R reference outputs exist for modified public functions.
- [ ] Plot review exists for modified plotting functions.

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
