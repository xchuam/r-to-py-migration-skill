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

Option 1: install from chat with the Codex skill installer.

Run this in the agent chat, not in your shell:

```text
$skill-installer install https://github.com/xchuam/r-to-py-migration-skill/tree/main/skills/cran-to-native-python-migration
```

Option 2: install manually from the shell as a personal skill.

Run this in your shell, not in chat:

```bash
mkdir -p ~/.agents/skills
cp -R skills/cran-to-native-python-migration ~/.agents/skills/
```

Then restart Codex so the new skill is discovered.

### Claude

Option 1: install locally with shell commands.

Run this in your shell:

```bash
mkdir -p ~/.claude/skills
cp -R skills/cran-to-native-python-migration ~/.claude/skills/
```

Option 2: use Claude's upload flow.

Do this in the Claude UI, not in the shell:

- zip the `skills/cran-to-native-python-migration` folder
- upload that folder as a skill
- then invoke the skill from the Claude chat

### GitHub Copilot / compatible agents

For a repository-scoped skill, run this in your shell:

```bash
mkdir -p .github/skills
cp -R skills/cran-to-native-python-migration .github/skills/
```

For a personal installation, run this in your shell:

```bash
mkdir -p ~/.copilot/skills
cp -R skills/cran-to-native-python-migration ~/.copilot/skills/
```

GitHub's agent-skill docs also recognize `.claude/skills` and `.agents/skills` as supported locations in some contexts, so this same folder can be reused across ecosystems.

## Install The Required Companion Skill

This migration skill should be used together with [`github/awesome-copilot/python-pypi-package-builder`](https://github.com/github/awesome-copilot/blob/main/skills/python-pypi-package-builder/SKILL.md) for Python package scaffolding, packaging metadata, and release-readiness work.

### Codex / OpenAI agents

Run this in the agent chat:

```text
$skill-installer install https://github.com/github/awesome-copilot/tree/main/skills/python-pypi-package-builder
```

### Manual install from GitHub

Run this in your shell:

```bash
git clone https://github.com/github/awesome-copilot.git /tmp/awesome-copilot
mkdir -p ~/.agents/skills
cp -R /tmp/awesome-copilot/skills/python-pypi-package-builder ~/.agents/skills/
```

After installation, invoke both skills together from chat:

```text
Use cran-to-native-python-migration and github/awesome-copilot/python-pypi-package-builder for this migration.
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
