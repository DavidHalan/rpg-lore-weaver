---
description: create an RPG character using the RPG Lore Weaver skill
---

Follow these steps strictly to create an RPG character using the RPG Lore Weaver skill. Do not skip phases or generate the final output before the user has completed the process.

1.  **Step 0: Discovery**
    - Initialize the process by reading the existing `SKILL.md` (usually `rpg-lore-weaver/SKILL.md`).
    - Check for existing context (e.g., character files, campaign settings).
    - Ask the user for the System & Setting, Race & Class, Tone, Depth, and Concept starting point.
    - Wait for the user's responses.
    - If a specific system is chosen, check if there's a reference file in `systems/` (e.g., `daggerheart-rules.md`) and load it.
    - If necessary, offer the "Quick NPC" or "Party Creation" paths from the respective `.md` files.
    - **Understanding Lock:** Present the gathered information and ask "Does this accurately reflect your intent? Confirm before we proceed."
    - **Do not proceed until explicit confirmation.**

2.  **Phase 1: The Soil (Origin & Family)**
    - Display the progress bar for Phase 1.
    - Ask questions related to Pillar 1 (Origin) and Pillar 2 (Family & Background). Use the techniques in `references/techniques-and-examples.md`.
    - Wait for the user's responses.
    - Provide a brief recap of Phase 1 before moving to Phase 2.

3.  **Phase 2: The Engine (Motivations, Personality & Ideals)**
    - Display the progress bar for Phase 2.
    - Ask questions related to Pillar 3 (Motivations), Pillar 4 (Personality), and Pillar 5 (Ideals).
    - Wait for the user's responses.
    - Provide a brief recap connecting Phase 2 to Phase 1.

4.  **Phase 3: The Cracks (Weaknesses & Decisions)**
    - Display the progress bar for Phase 3.
    - Ask questions related to Pillar 6 (Weaknesses) and Pillar 7 (Key Decisions). Force internal contradictions if possible.
    - Wait for the user's responses.
    - Provide a brief recap connecting Phase 3 to previous phases.

5.  **Phase 4: The Web (Friends, Mentors & Rivals)**
    - Display the progress bar for Phase 4.
    - Ask questions related to Pillar 8 (Friends), Pillar 9 (Mentors), and Pillar 10 (Rivals/Enemies). Tie connections to specific places.
    - Wait for the user's responses.
    - Provide a brief recap connecting Phase 4 to all previous phases.

6.  **Phase 5: The Synthesis & Final Output**
    - Display the full progress bar (100%).
    - Review the gathered information against the "Output Validation Checklist" in `SKILL.md`.
    - Generate the final structured character document using the template in `references/formatting-templates.md`.
    - Display the concise completion summary.
