---
description: "Operational reference for rpg-lore-weaver utility scripts."
metadata:
  tags: [rpg-lore-weaver, scripts, tooling]
---

# scripts

Executable utilities for the `rpg-lore-weaver` skill.

## Prerequisites

- Python 3.9+ (recommended)
- No external dependencies (standard library only)

## Available Scripts

### `validate_character_output.py`

Validates generated output for:

- Full character format (10 pillars)
- NPC Quick Mode format (3-pillar tiers)

**Usage:**

```bash
# Auto-detect mode
python scripts/validate_character_output.py character.md

# Force full mode
python scripts/validate_character_output.py character.md --mode full

# Force NPC quick mode
python scripts/validate_character_output.py character.md --mode npc-quick
```

### `export_character.py`

Exports character/NPC documents to multiple formats.

**Usage:**

```bash
# Export to JSON
python scripts/export_character.py character.md --format json

# Export to clean Markdown (no box-drawing characters)
python scripts/export_character.py character.md --format clean -o clean_character.md

# Export to Homebrewery/GM Binder format
python scripts/export_character.py character.md --format homebrewery -o character_brew.md

# Force mode when needed
python scripts/export_character.py character.md --format json --mode npc-quick
```

**Formats:**

- `json` - Structured JSON
- `clean` - Clean Markdown without box-drawing characters
- `homebrewery` - Homebrewery/GM Binder compatible Markdown

### `compile_skill.py`

Compiles the skill into a single manual file for copy-paste usage in LLMs.

Includes `SKILL.md`, `references/*.md`, and `systems/*.md` (except `systems/README.md`). Preserves a path map so references like `references/random-tables.md` still point to a clearly named section in the compiled file.

**Profiles:**

| Profile  | Contents                     | Estimated Tokens |
| -------- | ---------------------------- | ---------------- |
| `full`   | All references + all systems | ~112k            |
| `system` | Core references + ONE system | ~24k             |
| `micro`  | SKILL.md + system-prompts.md | ~9k              |

**Usage:**

```bash
# Full manual (default)
python scripts/compile_skill.py

# System-specific (D&D 5e only)
python scripts/compile_skill.py --profile system --system dnd5e

# Minimal context
python scripts/compile_skill.py --profile micro

# Custom output path
python scripts/compile_skill.py --profile system --system coc -o coc-manual.md
```

**System aliases**: `dnd`, `pf2e`, `dh`, `coc`, `t20`, `op`

Output includes line count, file size, and estimated token count.

### `quality_gate.py`

Runs a continuous quality gate:

- Unit tests (`test_lib_utils.py`, `test_character_tools.py`)
- SKILL.md line count enforcement (≤500 lines)
- Manual compilation
- Example validation and export

**Usage:**

```bash
python scripts/quality_gate.py
```

### `test_character_tools.py`

Regression tests for parser and validator behavior.

```bash
python -m unittest scripts/test_character_tools.py
```

### `test_lib_utils.py`

Unit tests for `lib_utils.py`.

```bash
cd scripts && python -m unittest test_lib_utils
```

### `lib_utils.py`

Shared utility library used by other scripts (DRY principle).

- **Frontmatter Parsing**: handles both legacy `tags: []` and new `triggers:` formats
- **Mojibake Scoring**: repair logic for text encoding errors
- **Text Cleaning**: regex patterns for markdown sanitization

## Notes on Emojis and Windows Consoles

Scripts keep emoji output by design. In terminals without UTF-8 support, output falls back safely without crashing.
