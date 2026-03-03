---
description: "Contribution guide for rpg-lore-weaver."
metadata:
  tags: [rpg-lore-weaver, contributing]
---

# Contributing to rpg-lore-weaver

Thank you for your interest in improving this skill! Here's how to contribute effectively.

---

## Commit Conventions

We follow **Conventional Commits** to keep the changelog clean and automatable.

### Format

```
<type>(<scope>): <short description>
```

### Types

| Type       | When to Use                            | Example                                              |
| ---------- | -------------------------------------- | ---------------------------------------------------- |
| `feat`     | New feature or content                 | `feat(systems): add call-of-cthulhu module`          |
| `fix`      | Bug fix or correction                  | `fix(validator): handle missing Cultural Touchstone` |
| `docs`     | Documentation only                     | `docs(readme): update installation instructions`     |
| `refactor` | Code restructuring, no behavior change | `refactor(scripts): centralize text normalization`   |
| `test`     | Adding or fixing tests                 | `test(export): add JSON export regression test`      |
| `chore`    | Maintenance tasks                      | `chore: update version to 2.0.0`                     |
| `style`    | Formatting, encoding fixes             | `style: fix mojibake in reference files`             |

### Scopes (optional)

`skill`, `references`, `systems`, `scripts`, `examples`, `docs`, `readme`, `changelog`

### Examples

```
feat(references): add 3 new archetypes to character-archetypes.md
fix(skill): enforce Understanding Lock gate for ambiguous replies
docs(architecture): expand data flow diagrams
test(validator): add elevator pitch multi-sentence detection
refactor(scripts): remove obsolete normalize_library.py calls
```

---

## Project Structure

```
rpg-lore-weaver/
├── SKILL.md              ← Main AI instructions (≤500 lines!)
├── references/           ← Knowledge base loaded on demand
│   └── villain-mode.md   ← Dedicated villain/antagonist workflow
├── systems/              ← RPG system rules with Backstory by Class + Mechanical Suggestions
├── examples/             ← Complete character samples
├── scripts/              ← Python utilities and tests
├── docs/                 ← Architecture and technical docs
├── CHANGELOG.md          ← Release history
├── README.md             ← English documentation
└── README.pt-BR.md       ← Portuguese documentation
```

---

## Before Submitting

### Checklist

- [ ] **SKILL.md ≤ 500 lines** — Run: `(Get-Content SKILL.md | Measure-Object -Line).Lines`
- [ ] **Tests pass** — Run: `python -m unittest scripts/test_lib_utils.py scripts/test_character_tools.py -v`
- [ ] **Examples validate** — Run: `python scripts/validate_character_output.py examples/<file>.md`
- [ ] **Manual compiles** — Run: `python scripts/compile_skill.py`
- [ ] **Quality gate passes** — Run: `python scripts/quality_gate.py`
- [ ] **CHANGELOG.md updated** — Add entry under `[Unreleased]` or next version
- [ ] **Commit message follows convention** — See format above

### Quick Verification

```bash
# Run everything at once
python scripts/quality_gate.py
```

---

## Adding Content

### New Reference File

1. Create `references/your-new-reference.md` with frontmatter
2. Add entry to `references/resource-index.md`
3. Reference from `SKILL.md` where needed (keep SKILL.md under 500 lines!)
4. Run quality gate

### New System Module

1. Create `systems/systemname-rules.md` following existing format
2. Include these sections: **Key Concepts**, **Backstory by Class**, **Connections Prompts**, **Mechanical Suggestions (Phase 6)**, **World Assumptions**
3. Add entry to `systems/README.md` and `references/resource-index.md`
4. Consider adding a sample character in `examples/`
5. Add system-specific prompts to `references/system-prompts.md`

### New Entity Mode (Villain, Faction, etc.)

1. Create `references/your-mode.md` following `villain-mode.md` as template
2. Add entry to `references/resource-index.md`
3. Add routing in SKILL.md Discovery Step 0 (keep SKILL.md under 500 lines!)
4. Run quality gate

### New Example Character

1. Create `examples/sample-character-<system>.md` following existing format
2. Validate: `python scripts/validate_character_output.py examples/your-file.md`
3. Test export: `python scripts/export_character.py examples/your-file.md --format json`

---

## Key Rules

1. **SKILL.md must stay ≤500 lines** — Move detailed content to `references/`
2. **Progressive disclosure** — SKILL.md references, doesn't embed
3. **Test before committing** — Always run the quality gate
4. **Keep examples valid** — All examples must pass the validator
5. **English for code and content** — READMEs are bilingual (EN + PT-BR)
