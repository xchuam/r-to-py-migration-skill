# R Package to Python Package Migration Skill

A reusable agent skill for migrating a general R CRAN package into a real Python package without losing behavioral fidelity.

This repository is for structured migration work, not blind syntax conversion. The skill treats the R package as the specification, freezes the reference surface before implementation, and enforces three parity constraints throughout the migration:

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

## Install The Skill

### Codex / OpenAI agents

Install directly from GitHub with the Codex skill installer:

```text
$skill-installer install https://github.com/xchuam/r-to-py-migration-skill/tree/main/skills/cran-to-native-python-migration
```

You can also install it manually as a personal skill:

```bash
mkdir -p ~/.agents/skills
cp -R skills/cran-to-native-python-migration ~/.agents/skills/
```

Then restart Codex so the new skill is discovered.

### Claude

For local Claude-compatible skill folders:

```bash
mkdir -p ~/.claude/skills
cp -R skills/cran-to-native-python-migration ~/.claude/skills/
```

If you are using Claude's skill upload flow, zip the `cran-to-native-python-migration` folder and upload that folder as a skill.

### GitHub Copilot / compatible agents

For a repository-scoped skill:

```bash
mkdir -p .github/skills
cp -R skills/cran-to-native-python-migration .github/skills/
```

For a personal installation:

```bash
mkdir -p ~/.copilot/skills
cp -R skills/cran-to-native-python-migration ~/.copilot/skills/
```

GitHub's agent-skill docs also recognize `.claude/skills` and `.agents/skills` as supported locations in some contexts, so this same folder can be reused across ecosystems.

## Use The Skill

Once installed, ask the agent to use `cran-to-native-python-migration` when auditing or migrating a CRAN package.

Good use cases:

- freezing the exported R reference surface before any implementation
- building audit artifacts such as `R_PACKAGE_DOSSIER.md` and `EXPORTED_API.csv`
- classifying modules into rewrite, faithful port, or parity bridge
- translating testthat coverage into pytest parity coverage
- scaffolding the Python package, parity fixtures, and release checklist

Poor use cases:

- line-by-line syntax conversion
- claiming parity without tests or fixtures
- skipping packaged data, examples, or compiled code
- collapsing faithful port and native rewrite into the same plan

## License

This repository is licensed under the MIT License. See [LICENSE](./LICENSE).
