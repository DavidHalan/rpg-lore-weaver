---
description: "Reference for rpg-lore-weaver: formatting templates. Load only when needed."
metadata:
  tags: [rpg-lore-weaver, reference, formatting-templates]
---

# Formatting Templates

Templates for visual elements used throughout `rpg-lore-weaver`.

---

## Table of Contents

- [Progress Tracker Box](#progress-tracker-box)
- [Phase Recap Format](#phase-recap-format)
- [Completion Summary](#completion-summary)

---

## Progress Tracker Box

Display this box at the start of each phase. Update the status icons as phases complete.

**Status Icons:**

- `✓` — Phase complete
- `→` — Current phase (active)
- `○` — Phase not yet started

**Template (Phase 1 active):**

```
╔═══════════════════════════════════════════════════════════════╗
║     🎭 RPG LORE WEAVER — Creating Character                 ║
╠═══════════════════════════════════════════════════════════════╣
║ → Phase 1: The Soil                     [17%]               ║
║ ○ Phase 2: The Engine                                        ║
║ ○ Phase 3: The Cracks                                        ║
║ ○ Phase 4: The Web                                           ║
║ ○ Phase 5: The Synthesis                                     ║
║ ○ Phase 6: The Gear                                          ║
╠═══════════════════════════════════════════════════════════════╣
║ Progress: █████░░░░░░░░░░░░░░░░░░░░░░░░░  17%               ║
╚═══════════════════════════════════════════════════════════════╝
```

**Template (Phase 3 active):**

```
╔═══════════════════════════════════════════════════════════════╗
║     🎭 RPG LORE WEAVER — Creating Character                 ║
╠═══════════════════════════════════════════════════════════════╣
║ ✓ Phase 1: The Soil                                          ║
║ ✓ Phase 2: The Engine                                        ║
║ → Phase 3: The Cracks                   [50%]               ║
║ ○ Phase 4: The Web                                           ║
║ ○ Phase 5: The Synthesis                                     ║
║ ○ Phase 6: The Gear                                          ║
╠═══════════════════════════════════════════════════════════════╣
║ Progress: ███████████████░░░░░░░░░░░░░░░  50%               ║
╚═══════════════════════════════════════════════════════════════╝
```

**Template (All phases complete):**

```
╔═══════════════════════════════════════════════════════════════╗
║     🎭 RPG LORE WEAVER — Character Complete!                 ║
╠═══════════════════════════════════════════════════════════════╣
║ ✓ Phase 1: The Soil                                          ║
║ ✓ Phase 2: The Engine                                        ║
║ ✓ Phase 3: The Cracks                                        ║
║ ✓ Phase 4: The Web                                           ║
║ ✓ Phase 5: The Synthesis                                     ║
║ ✓ Phase 6: The Gear                                          ║
╠═══════════════════════════════════════════════════════════════╣
║ Progress: ██████████████████████████████  100%               ║
╚═══════════════════════════════════════════════════════════════╝
```

**Progress bar specifications:**

- 30 characters wide (use █ for filled, ░ for empty)
- Percentage based on current phase: Phase 1=17%, Phase 2=33%, Phase 3=50%, Phase 4=67%, Phase 5=83%, Phase 6=100%

---

## Phase Recap Format

Display after each phase is completed, before transitioning to the next:

```
✓ RECAP — Phase [N] Complete
    [Pillar Name]: [Key detail established]
    [Pillar Name]: [Key detail established]
   → Carries into Phase [N+1]: [How this connects to next phase]
```

**Example (after Phase 1):**

```
✓ RECAP — Phase 1 Complete
    Origin: Born in a war-ravaged port city, raised in salt and ash
    Family: Abandoned by father, mentored by a blind shipwright
   → Carries into Phase 2: The shipwright's lessons about "building things right"
     shape their ideals about justice and craftsmanship
```

**Rules:**

- Keep each line to one key detail — avoid long paragraphs
- The "Carries into" line should create a narrative bridge to the next phase
- Actively connect new details to previous ones (in Phases 2+)

---

## Completion Summary

Display after the final character document is generated:

```
🎉 Character created successfully!

📦 Character: [Name] — [Epithet]
📝 System: [System]
🎭 Tone: [Tone]

✓ Pillars Covered:
   ✅ Origin  ✅ Family  ✅ Motivations  ✅ Personality  ✅ Ideals
   ✅ Weaknesses  ✅ Decisions  ✅ Friends  ✅ Mentors  ✅ Rivals

🚀 Next Steps:
   1. Share with your DM for campaign integration
   2. Revisit after 3-4 sessions to update evolution arc
   3. Create companion NPCs using the same skill
   4. Export character using scripts/export_character.py
```

---

## Output Validation Checklist

Before delivering, verify the character document meets quality standards:

- [ ] Elevator Pitch is exactly ONE sentence
- [ ] Backstory weaves Origin + Family + Decisions as narrative (not a list)
- [ ] All 10 pillars are addressed in the document
- [ ] DM Hooks emerge organically from the backstory (not bolted on)
- [ ] DM Hooks include Secret, Unresolved Thread, Evolution Arc, and Cultural Touchstone
- [ ] Desire vs Need are genuinely different (not redundant)
- [ ] At least 1 internal contradiction exists
- [ ] Tone matches the campaign setting specified in Discovery
- [ ] Connections include at least 1 Ally, 1 Mentor, and 1 Rival
