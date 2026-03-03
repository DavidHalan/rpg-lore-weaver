---
description: "Documentation for rpg-lore-weaver: changelog."
metadata:
  tags: [rpg-lore-weaver, changelog]
---

# Changelog

All notable changes to the `rpg-lore-weaver` skill.

## [2.1.0] - 2026-03-03

### Added

- **Pathfinder 2e example**: `examples/sample-character-pathfinder2e.md` — Seraphine Duskwalker, Champion de Sarenrae with faith crisis, Edicts/Anathema, Heritage (22/22 validation)
- **Call of Cthulhu example**: `examples/sample-character-coc.md` — Margaret "Maggie" Calloway, widowed librarian with 10 official backstory entries, Sanity mechanics (22/22 validation)
- **Villain example**: `examples/sample-villain.md` — Verath Sunhollow, grief-corrupted druid using villain-mode V1-V6 workflow (20/20 validation)
- **Villain validation mode**: `scripts/validate_character_output.py` now auto-detects villain files and runs 20 villain-specific checks (Mirror, Plan, Cracks, Web, DM Hooks)
- **Compile skill tests**: `scripts/test_compile_skill.py` — 14 structural tests covering `full`, `system`, and `micro` profiles
- **CI/CD pipeline**: `.github/workflows/quality-gate.yml` — GitHub Actions on push (main/develop) and PRs (main)
- **Sub-workflows**: 3 dedicated workflows in `.agent/workflows/`:
  - `create-rpg-npc.md` — NPC Quick Mode (3-pillar tiered system)
  - `create-rpg-villain.md` — Villain Mode (V1-V6 process)
  - `create-rpg-party.md` — Party Mode (shared history + relationship web)
- **Frontmatter validation**: `quality_gate.py` now validates `description` and `tags` in all reference frontmatters
- **Error handling reference**: `references/error-handling.md` — Extracted error handling, recovery strategies, and technical notes from SKILL.md

### Changed

- **SKILL.md compression**: Reduced from 498 to 375 lines (25% freed) by extracting content to references:
  - Error Handling + Recovery → `references/error-handling.md` (new)
  - Output Validation → `references/formatting-templates.md` (merged)
  - Few-Shot Examples → `references/techniques-and-examples.md` (merged)
- **Quality gate**: Added `test_compile_skill.py` to test suite; frontmatter validation check; BOM-tolerant encoding (`utf-8-sig`)
- **Resource index**: Updated with 3 new examples and `error-handling.md` reference

### Fixed

- **Frontmatter**: Added YAML frontmatter (`description`, `metadata.tags`) to 6 reference files that were missing it: `reference-plot-story-structure.md`, `reference-psychology-emotions.md`, `reference-body-health-behavior.md`, `reference-character-design-backstory.md`, `reference-culture-society.md`, `reference-dialogue-language-rhetoric.md`
- **BOM encoding**: `random-tables.md` had UTF-8 BOM preventing frontmatter detection; fixed via `utf-8-sig` in validator

### Docs

- **README.md & README.pt-BR.md**: Complete rewrite — added systems table with highlights, 8 examples in table format (including PF2e, CoC, Villain), new "Workflows" section with slash command table (`/create-rpg-character`, `/create-rpg-npc`, `/create-rpg-villain`, `/create-rpg-party`), new "Quality Assurance" section documenting CI/CD and quality gate checks, updated directory tree (21 refs, 9 scripts, `.agent/workflows/`, `.github/workflows/`, `error-handling.md`), expanded architecture diagram (mermaid) with workflow and validation mode nodes

## [2.0.0] - 2026-02-20

### Added

- **Entity Type Selection (Discovery)**: New "Step 0" asks if the user wants to create a PC, NPC, or Villain before system/race/class questions
- **Villain / Antagonist Mode**: New `references/villain-mode.md` with 6-step dedicated workflow (Seed, Mirror, Plan, Cracks, Web, Escalation)
- **Phase 6: The Gear (Mechanical Suggestions)**: After narrative creation, AI suggests stats, skills, feats, and equipment justified by the character's story
- **Auxiliary modes note**: Factions, deities, and locations can be generated minimally on demand during character creation
- **Backstory by Class**: Each `systems/*.md` now includes class-specific backstory prompts and connections
- **Connections Prompts**: Each system now includes prompts for building bonds between PCs and NPCs
- **Mechanical Suggestions per System**: Each `systems/*.md` now includes a "Phase 6" section with system-specific mechanical guidance

### Changed

- **D&D 5e module**: Expanded from 44 to ~115 lines with backstory by class category, Ideals/Bonds/Flaws derivation, Inspiration Triggers
- **Pathfinder 2e module**: Expanded from ~40 to ~145 lines with Edicts/Anathema prompts, ancestry feats guidance
- **Daggerheart module**: Expanded from 64 to ~180 lines with all 9 classes' Background Questions and Connections (from official SRD), Experiences mechanic
- **Call of Cthulhu module**: Expanded from ~40 to ~120 lines with all 10 official backstory entries, Key Backstory Connection
- **Tormenta 20 module**: Expanded from 38 to ~130 lines with 15 races, Origens list, Devoção prompts, universal Tormenta questions
- **Ordem Paranormal module**: Expanded from ~40 to ~140 lines with 5 Elementos, NEX, recruitment/exposure/horror prompts
- **Discovery flow**: Redesigned with numbered steps 0-5 and routing to appropriate modes
- **Understanding Lock**: Now includes entity Type field
- **Phase table**: Updated from 5 to 6 phases
- **Tips for the AI**: Compacted from 10 to 6 dense bullets
- **References section**: Replaced with pointer to `references/resource-index.md`

### Docs

- **README.md & README.pt-BR.md**: Updated features list (entity type, villain mode, Phase 6, 6 phases), added `villain-mode.md` to directory trees
- **CONTRIBUTING.md**: Added villain mode to project tree, new "New Entity Mode" section, updated system module required sections
- **systems/README.md**: Rewritten with table of systems + highlights, enriched file format template
- **docs/ARCHITECTURE.md**: Updated core, knowledge, and rules layer tables; "Why 6 Phases" section; added `villain-mode.md`
- **formatting-templates.md**: Added Phase 6 to tracker, updated progress percentages for 6 phases
- **Consistency fix**: Updated "5-phase" → "6-phase" across `system-prompts.md`, `npc-quick-mode.md`, `party-creation-mode.md`, `creative-decision-log.md`

### Installation & Tooling

- **compile_skill.py**: Rewritten with 3 profiles (`full` ~112k tokens, `system` ~24k, `micro` ~9k), `--system` flag with aliases (dnd, t20, coc, pf2e, dh, op), token estimation
- **README.md & README.pt-BR.md**: New installation section with agent compatibility table (6 agents, 5 free), manual compilation profiles, Google AI Studio recommendation
- **scripts/README.md**: Updated compile_skill.py documentation with profiles table
- **.gitignore**: Updated to glob `rpg-lore-weaver-manual*.md` for all profile outputs

## [1.9.0] - 2026-02-10

### Added

- **Prompt Engineering**: Expanded CSO-optimized triggers (16 triggers, including PT-BR terms and intent-based triggers like "my character feels flat")
- **Prompt Engineering**: Third few-shot example in Error Handling for "loner" character pattern
- **Anti-Rationalization**: Enforced Understanding Lock with explicit ambiguity handling ("sure"/"I guess" are NOT confirmation)
- **Chain-of-Thought**: Enriched Synthesis Scratchpad from 3 to 5 cross-verification steps with action verbs
- **Context Compression**: Added concrete `COMPRESSED CONTEXT` format template for long conversations
- **Documentation**: Created `CONTRIBUTING.md` with conventional commit conventions, checklists, and contribution guides
- **Documentation**: Completely rewritten `docs/ARCHITECTURE.md` with mermaid diagrams, design decisions, script pipeline, and reading paths

### Changed

- **SKILL.md**: Version bumped to 1.9.0; metadata expanded with `domain: tabletop-rpg` and additional tags
- **SKILL.md**: Compacted Bundled Resources section from 20 lines to 5 lines
- **Quality Gate**: Removed obsolete `normalize_library.py` and `library_curate.py` calls from `quality_gate.py`
- **Quality Gate**: Added `test_lib_utils.py` execution and SKILL.md ≤500 line count enforcement

### Fixed

- **Quality Gate**: Removed dead `references/library` directory reference that would cause failures
- **Cleanup**: Deleted `scripts/__pycache__/` (9 cache files) and `rpg-lore-weaver-manual.md` (443 KB compiled artifact)
- **Cleanup**: Deleted obsolete `references/README.md` (had ghost refs to removed `library/` directory)
- **Cleanup**: Removed ghost entries `library-curation.md` and `library-index.md` from `resource-index.md`
- **Cleanup**: Purged all references to `normalize_library.py`, `library_curate.py`, and `references/library/` from `scripts/README.md`, `testing-evidence.md`, and `compile_skill.py`
- **Cleanup**: Created `.gitignore` to prevent `__pycache__/` and compiled manual from being versioned
- **Bugfix**: Fixed encoding mojibake (corrupted characters like `ðŸŽ` and `â•`) across 17 markdown files, restoring proper emojis and ASCII borders

## [1.8.0] - 2026-02-04

### Added

- **Compliance**: New `references/resource-index.md` to offload resource listing from main file.
- **Documentation**: Added `docs/ARCHITECTURE.md` to document the project's script ecosystem and data flow.

### Changed

- **Library Optimization**: Consolidated ~96 fragmented library files into 6 thematic reference files in `references/`.
- **Skill Definition**: Reduced `SKILL.md` size to < 500 lines for compliance with developer standards.
- **Manual**: Standardized on a single `rpg-lore-weaver-manual.md` (removed 'lite' vs 'full' profiles).

### Fixed

- **Global Encoding Repairs**: Fixed "mojibake" (encoding errors) across all Markdown files.
- **Script Refactoring**: Centralized common logic into `scripts/lib_utils.py` and removed obsolete scripts (`library_curate.py`, `generate_content_map.py`, `normalize_library.py`).
- **Cleanup**: Removed `scraps/` directory and redundant files.

## [1.7.0] - 2026-01-30

### Added

- **System Modules**: Added `systems/` directory for injecting specific RPG rules (Context Injection)
- **Module Support**: Added `systems/daggerheart-rules.md` template
- **Core Update**: Updated `SKILL.md` Phase 1 to check for system modules
- **Compiler**: Updated `compile_skill.py` to bundle system rules into the manual file

## [1.6.2] - 2026-01-24

### Changed

- Updated `SKILL.md` metadata to include `triggers` and compliant description ("Use when...")
- Added Prerequisites, Architecture Diagram, and Troubleshooting sections to `README.md` and `README.pt-BR.md`

## [1.6.1] - 2026-01-22

### Added

- `rpg-lore-weaver-manual.md` — Auto-compiled single file for manual copy-pasting into LLMs
- `scripts/compile_skill.py` — Script to generate the manual file
- Updated READMEs with simplified manual installation instructions

## [1.6.0] - 2026-01-20

### Added

- 4 new techniques in `techniques-and-examples.md`: Trait-Flaw Grid, Situational Testing, Character Journal Entry, Relationship Web Diagram
- Socioeconomic Background prompt in Phase 1 (Pillar 2)
- Cultural Touchstones prompt in Phase 5 (connecting to setting legends)
- Flashback Moments section in `session-evolution.md` for intra-session depth

## [1.5.1] - 2026-01-15

### Added

- Intrinsic motivation anti-pattern warning in Phase 2 (push/pull framework)
- Placeable backstory events prompt in Phase 4 (location-anchored connections)

## [1.5.0] - 2026-01-14

### Added

- 4 new techniques in `techniques-and-examples.md`: Real-World Inspiration, Cliché Launchpad, Personality-Power Nexus, Simplicity Principle
- Fun-to-Play Checkpoint in Discovery phase
- Cliché validation prompt in Discovery phase
- Alignment as universal creative tool in Phase 2
- Personality-Power Nexus cross-reference in Phase 3
- 3 new AI tips: Simplicity Over Complexity, Draw from Real Life, Organic Revelation

## [1.4.0] - 2026-01-09

### Added

- Understanding Lock checkpoint between Discovery and Phase 1 (hard gate requiring player confirmation)
- Error Recovery section in SKILL.md with strategies for stalled/broken creative processes
- `references/creative-decision-log.md` — Template for tracking "why we chose X over Y" during creation
- `references/party-creation-mode.md` — Guide for creating interconnected character groups
- `references/system-conversion.md` — Converting characters between RPG systems
- Party Creation and System Conversion listed as core features in READMEs

### Changed

- Discovery section now references party-creation-mode.md and creative-decision-log.md
- Technical Implementation Notes updated (Cyberpunk reference → Ordem Paranormal)

## [1.3.0] - 2026-01-04

### Added

- `references/session-evolution.md` — Guide for evolving characters across multiple sessions
- `references/character-archetypes.md` — 20 universal narrative archetypes with combination system
- `references/random-tables.md` — 8 random inspiration tables for all creation phases
- `examples/sample-character-tormenta20.md` — Tormenta 20 example character (Ynara Solqueimada)
- `examples/sample-npc-quick.md` — NPC Quick Mode example (Dorin Halfhammer at 3 tiers)
- Cross-references in SKILL.md workflow to archetypes, random-tables, and session evolution

### Changed

- README.md and README.pt-BR.md updated with all new files

## [1.2.0] - 2025-12-29

### Added

- `references/system-prompts.md` — System-specific prompts for D&D, Pathfinder, Daggerheart, CoC, Tormenta 20, Ordem Paranormal
- `references/npc-quick-mode.md` — Streamlined 3-pillar NPC creation with tier system

### Changed

- Replaced Cyberpunk Red and Vampire: The Masquerade with Tormenta 20 and Ordem Paranormal as supported systems
- Standardized all reference files to English with native game terms preserved

### Removed

- `examples/sample-character-cyberpunk.md` — Replaced by Ordem Paranormal example

## [1.1.0] - 2025-12-23

### Added

- Core Capabilities section in SKILL.md
- Rich visual progress tracker (box format)
- Structured phase recap templates
- Discovery automation hints (check existing files, pre-fill system/tone)
- Completion summary block
- Output validation checklist
- Cross-references to `10-pillars-deep-dive.md`
- Table of Contents for `10-pillars-deep-dive.md`
- `references/formatting-templates.md` — Templates for progress tracker, recaps, and completion
- `scripts/validate_character_output.py` — Validates character documents (21 checks)
- `scripts/export_character.py` — Exports to JSON, Markdown, or Homebrewery format
- `scripts/README.md` — Documentation for utility scripts
- `examples/sample-character-daggerheart.md` — Daggerheart example character (Ren Ashveil)

### Changed

- README.pt-BR.md fully synchronized with English README

## [1.0.0] - 2025-12-20

### Added

- Initial release
- SKILL.md with 5-phase workflow and 10 pillars
- `references/techniques-and-examples.md`
- `references/10-pillars-deep-dive.md`
- `examples/sample-character-dnd.md` — D&D 5e example character (Kael Thornwood)
- `examples/sample-character-cyberpunk.md` — Cyberpunk Red example character
- README.md and README.pt-BR.md
