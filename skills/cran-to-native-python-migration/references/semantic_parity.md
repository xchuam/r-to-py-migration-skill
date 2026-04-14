# Semantic Parity

Use this reference before implementation whenever data-model behavior could drift.

## Mandatory audit topics

- missing-value behavior: `NA`, typed missing values, `NaN`, `NULL`, and Python `None`
- integer versus float preservation
- vector recycling and scalar broadcasting assumptions
- factor and categorical semantics
- indexing conventions and slice endpoints
- attributes, classes, and metadata retention
- `data.frame` or tibble column typing and row-shape expectations
- list and named-list behavior
- formulas, NSE, and metaprogramming usage
- matrix orientation, storage order, and shape expectations

## Rules of thumb

- Do not collapse all missing values into a single Python sentinel without documenting the loss.
- Do not assume pandas categories are a drop-in replacement for factors.
- Do not assume one-based user-facing conventions can be silently rewritten as zero-based interfaces.
- Do not treat attributes as disposable unless the audit proves they are internal only.
- Do not skip example data; examples often reveal shape and coercion expectations not obvious from tests.

## Fixture capture expectations

Prefer reusable parity fixtures derived from:

- packaged data
- documented examples
- testthat inputs and expected outputs
- direct source-package execution when behavior is ambiguous

Capture enough metadata to explain:

- input types and shapes
- output types and shapes
- ordering guarantees
- missing-value placement
- categorical levels
- attribute preservation

For plotting functions, capture enough evidence to compare:

- axis labels and units
- axis ranges
- legend position and style
- facet layout
- group and panel ordering
- color assignment
- annotation placement

## High-risk signals

Prefer extra fixture coverage when the source package uses:

- `factor`, `ordered`, or custom classes
- `model.frame`, `formula`, or NSE helpers
- `UseMethod`, S3 dispatch, S4 classes, or R6 objects
- `attr`, `structure`, or class-tagged return values
- compiled code in `src/`
- plotting helpers that combine statistical summaries with rendering defaults

## Suggested test prompts

- What happens with empty input?
- What happens with mixed integer and double input?
- What happens when missing values are present in keys, labels, or grouping columns?
- What happens when factor levels exist but are unused?
- What happens when vectors have incompatible lengths?
- What happens when attribute-bearing objects are subset or transformed?
