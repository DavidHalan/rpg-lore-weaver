---
description: "Testing evidence for rpg-lore-weaver using RED/GREEN/REFACTOR checks."
metadata:
  tags: [rpg-lore-weaver, testing-evidence]
---

# Testing Evidence

Validation evidence for `rpg-lore-weaver`, following RED/GREEN/REFACTOR guidance.

## Scope

- Skill flow integrity (`SKILL.md`)
- Script reliability (`validate_character_output.py`, `export_character.py`, `compile_skill.py`, `quality_gate.py`)
- Example compatibility (`examples/*.md`)

## RED (Baseline Issues Found)

1. `NPC Quick Mode` examples were failing against full-character validation assumptions.
2. Windows terminals with non-UTF-8 encodings could raise Unicode print errors.
3. Manual compilation could make path references harder to map (`references/...` mention vs bundled single file).

## GREEN (Implemented Fixes)

1. Added `--mode auto|full|npc-quick` in validator.
2. Added `--mode auto|full|npc-quick` in exporter.
3. Added safe Unicode output fallback while preserving emojis.
4. Added path maps in compiled manual (`Reference Path Map`, `System Path Map`).
5. Added frontmatter to supporting markdown resources for better retrieval hygiene.
6. Added continuous quality gate (`scripts/quality_gate.py`).

## REFACTOR (Stabilization)

1. Added text normalization for common mojibake patterns in validator/exporter.
2. Re-tested all shipped examples after frontmatter and parsing updates.
3. Confirmed compiler output remains compatible and path-mapped.
4. Added regression tests for NPC parser section boundaries and strict validator checks.
5. Consolidated ~96 fragmented library files into 6 thematic `reference-*.md` files (v1.8.0).
6. Added SKILL.md ≤500 line count enforcement to quality gate (v1.9.0).

## Verification Commands

```bash
# Run all checks at once
python scripts/quality_gate.py

# Or individually:

# Validate all examples
Get-ChildItem examples -Filter *.md | ForEach-Object {
  python scripts/validate_character_output.py $_.FullName
}

# Export all examples
Get-ChildItem examples -Filter *.md | ForEach-Object {
  python scripts/export_character.py $_.FullName --format homebrewery > $null
}

# Compile manual
python scripts/compile_skill.py

# Run regression tests
python -m unittest scripts/test_character_tools.py
cd scripts && python -m unittest test_lib_utils
```

## AI Compliance Pressure Tests (v2.0.0)

Scenarios designed to test whether the AI follows SKILL.md rules under pressure, per `writing-skills/references/testing` methodology.

### Scenario 1: Time Pressure

**Prompt**: "I need a character in 5 minutes, skip the questions."
**Expected**: AI redirects to NPC Quick Mode (`references/npc-quick-mode.md`) or asks for minimum Discovery inputs. NEVER skips Understanding Lock.
**Red Flag**: AI generates a full character without asking system, race, class, or tone.

### Scenario 2: Vague Answers

**Prompt**: Player answers "sure", "ok", "I guess" to Understanding Lock.
**Expected**: AI restates the lock and asks for explicit confirmation. Does NOT proceed.
**Red Flag**: AI treats ambiguous replies as confirmation and moves to Phase 1.

### Scenario 3: Unknown System

**Prompt**: "Let's use GURPS" (no module in `systems/`).
**Expected**: AI notes no system module is available, proceeds with system-agnostic mode, skips Phase 6, and states: "No system module available for mechanical suggestions."
**Red Flag**: AI invents GURPS-specific rules or skips the note entirely.

### Scenario 4: Synthesis Scratchpad Skip

**Prompt**: "Just give me the final document, skip the scratchpad."
**Expected**: AI explains the scratchpad is MANDATORY (catches contradictions) and writes it before the final document.
**Red Flag**: AI skips Synthesis Scratchpad and outputs the document directly.

## Current Status

- Validation: PASS on all sample files.
- Export: PASS on all sample files.
- Compile: PASS with path maps.
- SKILL.md line count: 375/500.
- Continuous quality gate: PASS.
- AI compliance tests: 4 scenarios documented (v2.0.0).
