# Failure Modes

Use this reference during review or when a migration plan feels too smooth.

## Common drift patterns

- treating exported R functions as the only contract and ignoring data, examples, or tests
- starting Python implementation before signatures, defaults, and expected outputs are frozen
- declaring everything a `native rewrite` without subsystem-level rationale
- translating testthat syntax without preserving test intent
- replacing factor semantics with plain strings
- normalizing missing values differently across modules
- changing indexing or shape conventions because they feel more Pythonic
- ignoring compiled code because the R wrapper looks simple
- claiming parity based on eyeballing instead of fixtures or tests

## Review checklist

- Is the reference surface frozen and evidenced?
- Does every subsystem have exactly one migration mode and a reason?
- Are API parity, test parity, and data-model parity explicitly called out in decisions?
- Are high-risk semantic areas covered by fixtures or dedicated tests?
- Are deviations logged with rationale and approval status?
- Does the Python package look releaseable, not script-like?

## Escalation conditions

Pause and surface the risk when:

- the requested change would skip earlier stages
- a user asks for a sweeping rewrite without parity evidence
- a proposed simplification discards categories, attributes, or missing-value distinctions
- compiled code appears performance-critical or behavior-defining
- the bridge implementation is drifting toward permanence

## Good correction pattern

1. Name the stage mismatch or parity risk.
2. State the smallest artifact or test needed to reduce uncertainty.
3. Make the focused edit.
4. Record the remaining unknowns.
