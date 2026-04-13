# Migration Modes

Every module or subsystem must be classified into exactly one migration mode.

## Mode definitions

### `native rewrite`

Use when the module's public behavior can be preserved while the internals are redesigned in idiomatic Python.

Use this by default when:

- the R implementation is mostly orchestration or glue code
- the public contract is small and well-tested
- Python-native data structures can preserve semantics cleanly
- compiled performance is not the main source of behavioral risk

Risks to watch:

- "Pythonic improvements" that silently change defaults, shapes, or missing-value behavior
- replacing vectorized quirks without documenting the semantic choice

### `faithful port`

Use when semantic fragility or reproducibility risk is high enough that internal behavior must stay close to the R implementation.

Prefer this when:

- numerical or ordering behavior is tightly constrained
- test coverage reveals sensitive edge cases
- formulas, NSE, attributes, or class semantics are central
- compiled code or low-level logic defines observable behavior

Risks to watch:

- accidental drift from R control flow or coercion rules
- over-abstracting before parity is demonstrated

### `temporary parity bridge`

Use only as a short-lived bridge for fixture generation, behavior comparison, or de-risking ambiguous semantics.

Acceptable bridge uses:

- capture fixtures from the original R package
- compare R and Python outputs during migration
- isolate semantics that need direct observation before rewrite

Not acceptable:

- leaving the bridge as the production implementation without explicit user approval
- using the bridge to avoid classifying or designing a subsystem

## Decision rubric

| Question | If yes, prefer |
| --- | --- |
| Can we preserve behavior with cleaner Python internals and low semantic risk? | `native rewrite` |
| Is observable behavior tightly tied to R semantics or low-level logic? | `faithful port` |
| Do we need direct R-backed evidence before committing to either strategy? | `temporary parity bridge` |

## Required rationale

Each classification should name:

- the subsystem boundary
- the selected mode
- the reason
- the primary parity driver
- what evidence would justify reclassification later

## Reclassification triggers

Revisit the mode when:

- fixture capture exposes undocumented edge cases
- compiled code turns out to define public behavior
- Python-native internals cannot preserve missing-value or categorical semantics
- parity tests remain brittle after multiple implementation attempts
