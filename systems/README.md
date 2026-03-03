---
description: "System module for rpg-lore-weaver: README."
metadata:
  tags: [rpg-lore-weaver, system, README]
---

# System Rulebooks

This directory contains system-specific rule files. The skill prioritizes content here over its general knowledge to prevent hallucinations.

## How to Add a New System

1. Create a markdown file named exactly as the system (e.g., `pathfinder2e-rules.md`).
2. Paste the official rules you want the AI to follow (Classes, Ancestries, Deities, World Lore).
3. Include these sections for full support:
   - **Key Concepts** — core terms and mechanics
   - **Backstory by Class** — class-specific narrative prompts
   - **Connections Prompts** — questions to build bonds between PCs/NPCs
   - **Mechanical Suggestions (Phase 6)** — system-specific mechanical guidance derived from backstory
   - **World Assumptions** — setting defaults, tone, and conventions
4. The skill will automatically detect and prioritize this file if the user selects that system.

## Available Systems

| System               | File                                                   | Highlights                                                                  |
| -------------------- | ------------------------------------------------------ | --------------------------------------------------------------------------- |
| **D&D 5e / 5.5e**    | [dnd5e-rules.md](dnd5e-rules.md)                       | Backstory by class category, Ideals/Bonds/Flaws, Inspiration Triggers       |
| **Pathfinder 2e**    | [pathfinder2e-rules.md](pathfinder2e-rules.md)         | Ancestries, Heritages, Edicts/Anathema, Ancestry Feats                      |
| **Daggerheart**      | [daggerheart-rules.md](daggerheart-rules.md)           | 9 classes with Background Questions & Connections (official), Experiences   |
| **Call of Cthulhu**  | [coc-rules.md](coc-rules.md)                           | 10 official backstory entries with example tables, Key Backstory Connection |
| **Tormenta 20**      | [tormenta20-rules.md](tormenta20-rules.md)             | 15 raças, Origens, Devoção, Tormenta questions, character concept examples  |
| **Ordem Paranormal** | [ordem-paranormal-rules.md](ordem-paranormal-rules.md) | 5 Elementos, NEX, O Outro Lado, recruitment/exposure/horror prompts         |

## File Format

Files should follow this structure for best results:

```markdown
# [SYSTEM NAME] Rules Summary (Backstory Focus)

## Key Concepts

(Core terms, factions, mechanics)

## Backstory by Class

(Class-specific narrative prompts and questions)

## Connections Prompts

(Questions to build bonds between PCs and NPCs)

## Mechanical Suggestions (Phase 6)

(System-specific mechanical guidance derived from backstory)

## World Assumptions

(Setting defaults, tone, and conventions)
```
