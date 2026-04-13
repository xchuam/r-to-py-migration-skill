# Workflow

This reference expands the staged workflow used by the skill. Use it when planning work, reviewing repository state, or deciding whether a stage is complete enough to advance.

## Stage map

| Stage | Goal | Minimum inputs | Typical outputs | Advance only when |
| --- | --- | --- | --- | --- |
| 1 | Freeze source-package behavior | `DESCRIPTION`, `NAMESPACE`, `R/`, `man/`, `tests/`, `data/`, `src/`, `vignettes/` | dossier, exported API, dependency and data inventories | Public surface, data assets, and compiled code are explicitly accounted for |
| 2 | Classify migration strategy per subsystem | Stage 1 outputs | mode map, parity priority matrix | Every subsystem has a mode and rationale |
| 3 | Build Python package skeleton | Stage 1 and 2 outputs | `pyproject.toml`, `src/`, `tests/`, env docs | Package layout matches the frozen contract |
| 4 | Normalize semantics and capture fixtures | tests, examples, data assets | semantic rules, type mapping, fixture catalog, edge-case matrix | Ambiguous behaviors have explicit fixture or rules coverage |
| 5 | Freeze interface and test parity | Stage 1 through 4 outputs | API mapping, Python stubs, pytest parity tests | Public contract and expected behaviors are executable |
| 6 | Implement modules | prior stages complete enough for target module | Python code, parity report, deviation log | Parity tests pass for implemented scope |
| 7 | Sync documentation | implemented scope | docstrings, README changes, migration notes | Docs reflect actual Python behavior and deviations |
| 8 | Prepare release | package and tests are runnable | release checklist, CI, metadata adjustments | Build, install, and test flow is credible for distribution |

## Stage ordering rules

- Do not enter Stage 6 for a module until Stage 2 classified it and Stage 5 froze its public interface and tests.
- Allow partial progress by module, but keep stage evidence explicit. Example: one subsystem can be at Stage 6 while another remains at Stage 2.
- If ambiguity appears during implementation, move backward to the earlier stage that resolves it instead of guessing forward.

## Parity checkpoints

At each stage, note which parity constraint is primary:

| Stage | Primary driver | Why |
| --- | --- | --- |
| 1 | API parity | The source-package contract must be frozen before translation decisions |
| 2 | API parity and data-model parity | Mode choice depends on public behavior risk and semantic fragility |
| 3 | API parity | The Python package layout must support the frozen external surface |
| 4 | data-model parity | Missing values, factors, shapes, and attributes require explicit rules |
| 5 | test parity | Executable parity checks prevent silent drift |
| 6 | all three | Implementation must satisfy the contract, semantics, and tests together |
| 7 | API parity | Docs must reflect the public contract, not internal convenience |
| 8 | test parity | Release confidence depends on reproducible verification |

## When to stop and document instead of coding

Stop and write artifacts first when:

- exported signatures or defaults are still unclear
- a subsystem mixes compiled code with R wrappers and no boundary map exists
- tests cover behaviors not described in docs and no fixture plan exists
- factors, attributes, formulas, or recycling rules are still implicit
- the package relies on dynamic registration or non-obvious namespace behavior

## Review prompts

- Which source behaviors are still undocumented?
- Which module classifications are provisional?
- Which parity claims are backed by tests or fixtures versus inference?
- Which packaged datasets or examples have not yet been exercised?
- Which deviations are intentional, and where are they logged?
