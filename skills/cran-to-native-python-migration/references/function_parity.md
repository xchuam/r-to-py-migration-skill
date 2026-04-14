# Function Parity

Use this reference when freezing or reviewing public function contracts.

## Contract rules

- Public Python function names should match public R function names by default.
- Public parameter names should match R parameter names by default.
- Public parameter order should match R parameter order.
- Effective defaults should match even when wrappers or helper layers make the syntax differ.
- Any mismatch must be logged immediately in `DEVIATION_LOG.md` and referenced from `FUNCTION_CONTRACT.csv`.

## Required evidence

For every migrated public function, record:

- exact R export name
- exact Python public name
- parameter name mapping
- parameter order
- documented defaults
- effective defaults
- output kind
- side effects such as warnings, grouping behavior, ordering, save paths, or sizing rules

## Blocking conditions

Stop and fix the contract before implementation when:

- a Python name differs from the R name without an approved deviation
- a parameter exists in only one language surface
- parameter order differs without an approved deviation
- a default is uncertain or depends on undocumented wrapper logic
- side effects are not captured in the contract

## Machine-readable artifacts

Use these together:

- `FUNCTION_CONTRACT.csv`
- `PARITY_CASES.csv`
- `PARAMETER_CASE_LINKS.csv`
- generated parameter coverage report

The minimum standard is one explicit parity case for every public parameter plus at least one default-behavior case per public function.

## Comparison expectations

For structured outputs, compare against live R output and verify:

- row counts
- column order
- values
- metadata fields
- ordering assumptions

For figures, compare against live R renders and verify:

- axis units
- axis ranges
- labels
- facet behavior
- legend position and styling
- panel or group ordering
- colors
- annotation placement

Include both default and non-default plot cases.
