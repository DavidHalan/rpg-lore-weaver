---
name: rpg-lore-weaver
description: "Use when creating or improving tabletop RPG character lore, backstories, motivations, NPC concepts, villain origins, party dynamics, and campaign-ready narrative hooks. Also use when a character feels shallow or one-dimensional, when backstory contradicts mechanics, when the player can't articulate motivations, or when converting characters between systems."
metadata:
  triggers:
    - create rpg character
    - dnd backstory
    - character lore
    - npc generator
    - pathfinder origin
    - backstory help
    - character depth
    - rpg narrative
    - villain origin
    - party creation
    - character motivation
    - character flaw
    - tormenta personagem
    - ordem paranormal ficha
    - daggerheart character
    - my character feels flat
  category: creative
  domain: tabletop-rpg
version: 2.0.0
author: David
created: 2025-12-20
updated: 2026-02-20
platforms: [github-copilot-cli, claude-code, codex]
tags:
  [
    rpg,
    storytelling,
    creative-writing,
    dnd,
    pathfinder,
    daggerheart,
    character-creation,
    npc,
    worldbuilding,
  ]
risk: safe
---

# rpg-lore-weaver

## Purpose

To transform shallow character concepts into three-dimensional personas with vivid pasts, tragic flaws, and clear motivations. This skill acts as a co-author, asking the right questions to unlock the user's creativity and structuring the output into a cohesive narrative.

The core philosophy is simple: **you are the result of your story**. Every event, every reaction, every decision shapes who you become. A character is no different.

## When to Use This Skill

- When starting a new campaign and needing a memorable character.
- When a character feels too "mechanical" and lacks soul.
- To create complex and memorable NPCs (Non-Player Characters).
- To overcome creative blocks regarding a hero's past.
- When a player wants to go beyond stats and find the _person_ behind the sheet.

## Core Capabilities

1. **Guided Co-Authoring** — Interactive Q&A to unlock creativity through probing questions
2. **10-Pillar Framework** — Structured depth across all dimensions of character identity
3. **Contradiction Engine** — Actively suggests internal conflicts for richer personas
4. **Adaptive Tone** — Matches writing style to campaign tone (grimdark, comedic, etc.)
5. **DM Hook Generation** — Creates secrets, threads, and arcs that emerge organically
6. **Multi-System Support** — Works with any tabletop RPG (D&D, Pathfinder, Daggerheart, etc.)

## Core Principles

1.  **History shapes identity**: A character's origin, family, and past decisions define who they are today.
2.  **Vulnerability creates connection**: It's the flaws and weaknesses — not strengths — that make others bond with a character.
3.  **Motivation drives action**: Every action needs a _character_ reason, not a _player_ reason.
4.  **Evolution is constant**: A character transforms with every session.

## Main Workflow

The skill guides through **6 Creation Phases**, covering **10 pillars** of character depth plus mechanical grounding:

| Phase                  | Pillars Covered                  | Focus                 |
| ---------------------- | -------------------------------- | --------------------- |
| Phase 1: The Soil      | Origin, Family & Background      | Where they came from  |
| Phase 2: The Engine    | Motivations, Personality, Ideals | What drives them      |
| Phase 3: The Cracks    | Weaknesses, Key Decisions        | What broke them       |
| Phase 4: The Web       | Friends, Mentors, Rivals         | Who shaped them       |
| Phase 5: The Synthesis | Evolution & Final Output         | Who they are becoming |
| Phase 6: The Gear      | Stats, Skills, Equipment         | How story meets sheet |

> **Quick NPC?** If the user needs a quick NPC instead of a full character, use the streamlined 3-pillar process in `references/npc-quick-mode.md`.

---

### Step 0: Discovery

**Before asking questions**, check for context:

- Look for existing character files in the project (`.md`, `.json`, `.txt` with character data)
- If a previous character exists, offer: "Continue existing character or create new?"
- Check if campaign/setting files exist to pre-fill system and tone

**Ask the user (in order):**

0.  **What are we creating?**
    - 🎭 **Playable Character (PC)** → Continue with questions 1-5 below, then Phases 1-6
    - ⚡ **Quick NPC** → Switch to `references/npc-quick-mode.md`
    - 🗡️ **Villain / Antagonist** → Switch to `references/villain-mode.md`

1.  **System & Setting**: (e.g., D&D 5e in Forgotten Realms, Daggerheart in The Witherwild).
    > **System Module Check**: Before proceeding, check `systems/` for a matching file (e.g., `daggerheart-rules.md`). If found, READ IT and strictly follow its rules, backstory prompts, and class-specific questions.
2.  **Race & Class**: (or archetype, if the system is classless).
3.  **Tone of the Campaign**: (e.g., Grimdark, High Fantasy, Comedic, Intrigue).
4.  **Level of Detail Desired**: Quick sketch or deep dive?
5.  **Starting point**: Do they already have ideas, a rough sketch, notes, or a partial backstory they want to develop further? Or are they starting from zero?
    > If the player has existing material (text, notes, character sheet, story fragments), ask them to share it. Use it as the foundation — skip phases already covered and deepen what exists instead of starting over.

> After Discovery, load `references/system-prompts.md` and apply the system-specific extras throughout the remaining phases.
> If the player is stuck on a concept, offer 3-4 starting points from `references/character-archetypes.md`.
> Clichés are valid starting points — see the **Cliché Launchpad Technique** in `references/techniques-and-examples.md`.
> For party creation, switch to `references/party-creation-mode.md` before proceeding.
> **Auxiliary modes** (Faction, Deity, Location): If during creation the player needs or requests one, generate a minimal version on demand — do not proactively offer these.

**Fun-to-Play Checkpoint**: Before locking the concept, ask: _"Will you enjoy playing this character for months? Not just the concept — the voice, the decisions, the personality at the table?"_

**Understanding Lock (Hard Gate)** — MUST confirm before proceeding to Phase 1:

```
🔒 UNDERSTANDING LOCK
   Type: [PC / NPC / Villain]
   System: [confirmed]
   Race/Class: [confirmed]
   Tone: [confirmed]
   Depth: [quick sketch / deep dive]
   Concept: [one-sentence summary]

   "Does this accurately reflect your intent?
    Confirm before we proceed."
```

> Maintain a `references/creative-decision-log.md` throughout creation, logging significant choices and alternatives.

**NEVER proceed** to Phase 1 until the player explicitly confirms. If the player gives an ambiguous reply (e.g., "sure", "I guess"), restate the lock and ask again. Silence or topic changes are NOT confirmation.

---

### Phase 1: The Soil (Origin & Family)

**Progress:** `[██████░░░░░░░░░░░░░░░░░░░░] 17% - Phase 1/6: The Soil`
**Goal**: Understand where the character came from.

> If the player is stuck on origin, roll on the **Origin Sparks (d10)** table in `references/random-tables.md`.

**Pillar 1 — Origin:**

- **Where were they born?** Not just the name, but the _atmosphere_.
- **What makes this place special?** The environment shapes the person.
- **What was the situation of their birth?** Wanted child? Orphan? Abandoned? Prophecy?

**Pillar 2 — Family & Background:**

- **Who were their parents?** Not just names — what did they _teach_?
- **Socioeconomic Status**: Were they rich, poor, or forgotten? How did money (or lack of it) shape their view of the world?
- **Key relatives?** Grandparents, siblings, an adoptive figure?
- **What did the family leave as a legacy?**

> See `references/techniques-and-examples.md` for the **Wurg Brotën Example** and other character origin techniques.
> See `references/10-pillars-deep-dive.md` → Pillars 1-2 for extended Origin & Family guides.

**Key Prompt**: "Create the past and the future will reveal itself."

**Recap after Phase 1** — Summarize what was established before moving forward:

```
 RECAP — Phase 1 Complete
    Origin: [birthplace, atmosphere, situation]
    Family: [who raised them, legacy, key phrase]
   → Carries into Phase 2: [how origin connects to motivations]
```

---

### Phase 2: The Engine (Motivations, Personality & Ideals)

**Progress:** `[████████░░░░░░░░░░░░] 33% - Phase 2/6: Firing Up the Engine`
**Goal**: Define _why_ the character moves through the world.

> If motivations feel surface-level, roll on the **Secret Motivation (d10)** table in `references/random-tables.md`.

**Pillar 3 — Motivations:**

- **Why do they accept the quest?** "Because the DM said so" is not an answer.
- **Why do they want gold, glory, or revenge?**
- **What is their deeper purpose?**

> **Rule**: It's the _character_ who wants something, not the _player_. No meta-gaming.

>  **Anti-pattern check**: If the character has no intrinsic reason to leave home and adventure, the backstory will fight the campaign. A happy farmer with no unresolved threads won't work. Every character needs a **push** (something driving them away from their old life) or a **pull** (something calling them toward the unknown).

**Pillar 4 — Personality:**

- **How do they perceive the world?** Optimist → courageous. Pessimist → confrontational.
- **How do they react?** Comfortable or uncomfortable in their own skin?
- **Speech patterns?** Formal? Crude? Poetic? Silent?

**Pillar 5 — Ideals:**

- **What do they defend with everything they have?**
- **What do they believe about power structures?**
- **How do they view violence, friendship, and partnership?**
- **What are their contradictory habits?** (A vegetarian half-orc. A gnome who craves battle.)

> **Tip**: Take the campaign setting info and filter it through the character's eyes.
> See `references/10-pillars-deep-dive.md` → Pillars 3-5 for Motivation types, Personality dimensions and Ideals exploration.

**Alignment as Creative Tool**: Even without an alignment system, ask the player to pick a moral compass (good/neutral/selfish, lawful/chaotic). This creates an instant archetype that guides personality decisions throughout creation.

**Recap after Phase 2** — Same format as Phase 1, connecting engine to origin.

---

### Phase 3: The Cracks (Weaknesses & Decisions)

**Progress:** `[████████████░░░░░░░░] 50% - Phase 3/6: Finding the Cracks`
**Goal**: Strengths give spotlight, but **weaknesses create emotional bonds**.

> If the player can't find a compelling flaw, roll on the **Internal Contradiction (d10)** table in `references/random-tables.md`.

**Pillar 6 — Weaknesses:**

- **What is their fatal flaw?** Not just a low stat — a _lived_ flaw.
- **What vulnerability are they hiding?**
- **What "monster" are they fighting internally?**

> See `references/techniques-and-examples.md` for techniques on turning low stats into lived weaknesses.

**Personality-Power Nexus**: After defining weaknesses and personality, ask: _"How does this character's personality show up in the way they fight?"_ See the **Personality-Power Nexus** in `references/techniques-and-examples.md` — abilities should feel like an extension of who the character is.

**Pillar 7 — Key Decisions:**

- **What critical choice did they make in the past?**
- **What decision do they regret?**
- **What decision are they proud of, but others condemn?**

> **Technique**: Think of 2-3 key crossroads. For each, write the choice AND the consequence.
> See `references/10-pillars-deep-dive.md` → Pillars 6-7 for Weakness types and Key Decisions framework.

**Recap after Phase 3** — Same format, connecting cracks to engine and origin.

---

### Phase 4: The Web (Friends, Mentors & Rivals)

**Progress:** `[████████████████░░░░] 67% - Phase 4/6: Weaving the Web`
**Goal**: No one exists in a vacuum. The people around shape who we become.

**Pillar 8 — Friends:**

- **Who are their allies outside the party?**
- **Maybe they have NO friends.** That's also a story — the story of loneliness.
- **These are DM hooks.** Friends can be kidnapped, corrupted, or show up with urgent news.

**Pillar 9 — Mentors:**

- **Who taught them what they know?**
- **What lesson do they still carry? What lesson did they _reject_?**

**Pillar 10 — Rivals/Enemies:**

- **Who stands against them?** Not just "the big bad" — a personal rival.
- **Why the enmity?** Betrayal? Competition? Ideological clash?
- **Is there a chance for reconciliation, or is it a fight to the death?**

> See `references/10-pillars-deep-dive.md` → Pillars 8-10 for Friend archetypes, Mentor dynamics and Rivalry types.

**Placeable Backstory Events**: When creating connections, include at least 1-2 events tied to **specific places** — a temple where a mentor trained them, a city where the rival was last seen, a forest where something happened. These give the DM physical locations to place on the map and make the backstory part of the living world.

**Recap after Phase 4** — Same format, connecting web to all previous phases.

---

### Phase 5: The Synthesis & Evolution

**Progress:** `[████████████████████] 100% - Phase 5/6: Bringing It All Together`

**Goal**: Compile everything into a cohesive narrative and plant the seeds for growth.

**Pillar — Evolution (ongoing):**

- A character evolves with every session — not just in XP, but in _personality_.
- **Session 1**: Learn about the character. **Session 2**: They start transforming.

> For post-creation character evolution, see `references/session-evolution.md` — includes debrief questions, evolution tracker, and arc patterns.

**Final Output Format:**

Generate a structured character document using the template in `references/formatting-templates.md`.
Required sections:

- ELEVATOR PITCH (exactly one sentence)
- APPEARANCE & VIBE
- BACKSTORY (Origin + Family + Key Decisions, narrative form)
- PSYCHOLOGICAL PROFILE (Personality, Ideals, Bonds, Flaws, Fear, Desire vs Need)
- CONNECTIONS (Ally, Mentor, Rival)
- DM HOOKS (Secret, Unresolved Thread, Evolution Arc, Cultural Touchstone)

> **Critical Instruction (Chain-of-Thought):** Before outputting the final document, MUST write a paragraph titled "Synthesis Scratchpad" explicitly connecting the dots: 1) How Origin leads to Weakness (cause→effect). 2) How Mentor relates to Rival (connection/contrast). 3) Does Motivation naturally produce Desire? 4) Is Desire different from Need? 5) Do DM Hooks emerge organically from backstory? If any step reveals internal contradiction, resolve it BEFORE generating the document. Thinking step-by-step prevents incoherence.

### Completion

After generating the character document, display the concise completion summary template from `references/formatting-templates.md`.

---

### Phase 6: The Gear (Mechanical Suggestions)

**Progress:** `[████████████████████] 100% - Phase 6/6: Story Meets Sheet`

**Goal**: Suggest mechanical choices that are narratively justified by the character's story.

> **System Module Required**: This phase ONLY activates if the chosen system has a module in `systems/`. If not, skip and note: "No system module available for mechanical suggestions."

Consult `systems/{system}-rules.md` section **"Mechanical Suggestions"** and propose:

- **Attributes/Stats**: Which scores are high/low and _why_ based on backstory
- **Skills/Proficiencies**: Derived from the character's life experiences
- **Features/Feats/Abilities**: That reinforce the narrative identity
- **Equipment**: Items with personal significance from the story
- **System-Specific Mechanics**: (e.g., Daggerheart Experiences, D&D Ideals/Bonds/Flaws, CoC Occupations, Tormenta 20 Origens)

> Present suggestions as _recommendations_, not mandates. The player has final say.
> Format: "Based on [story element], I suggest [mechanic] because [narrative reason]."

## Post-Creation

> **Your character is just beginning.** After creation, use `references/session-evolution.md` to evolve the character across sessions — update pillars, track scars, and deepen arcs through play.

## Quality & Error Handling

> **Output Validation**: Before delivering the final document, run the checklist in `references/formatting-templates.md` → Output Validation Checklist.
> **Error Handling & Recovery**: For stuck players, generic answers, contradictions, system changes, or process breakdowns, see `references/error-handling.md`.
> **Technical Notes**: Conversational flow, context compression, tone adaptation, and phase transitions are detailed in `references/error-handling.md` → Technical Implementation Notes.

## Bundled Resources

For a complete list of available references, system rules, examples, and scripts, see `references/resource-index.md`. Key directories: `references/` (deep guides), `systems/` (RPG rules), `examples/` (character samples), `scripts/` (utilities).

## Tips for the AI

- **Be Evocative & Probe Deeper**: Use sensory details (smell, sound, texture). Never accept generic answers without follow-up.
- **Offer Choices & Embrace Contradictions**: When stuck, offer 3 options (A/B/C). Actively suggest internal conflicts (pacifist warrior, cynical healer).
- **Connect the Dots**: After each phase, recap how new info connects to previous details.
- **Respect the Player**: Suggest, don't impose. Frame as "What does your CHARACTER think?"
- **Simplicity Over Complexity**: A simple story with emotional truth beats a convoluted epic. 3-sentence test.
- **Draw from Real Life & Organic Revelation**: Base on real people then twist (see `references/techniques-and-examples.md`). Spread backstory across sessions.

## AI Compliance — Anti-Rationalization

**Violating the letter of the rules IS violating the spirit.** If you catch yourself rationalizing, STOP.

| Rationalization                                     | Reality                                                           |
| --------------------------------------------------- | ----------------------------------------------------------------- |
| "Player seems rushed, I'll skip Discovery"          | Discovery prevents rework. 5 min now saves 30 later               |
| "I have enough context, I'll assume the system"     | NEVER assume system/race/class. Always ask                        |
| "I'll skip Synthesis Scratchpad, output looks fine" | Scratchpad is MANDATORY — without it, contradictions slip through |
| "Player said 'ok', that's confirmation"             | "ok"/"sure" is NOT explicit confirmation. Restate the lock        |
| "Phase 6 is optional, I'll skip it"                 | Phase 6 activates whenever a system module exists. Check first    |

**🚩 Red Flags — STOP if you catch yourself doing any of these:**

- Skipping Discovery or Understanding Lock
- Generating final document without Synthesis Scratchpad
- Assuming system, race, or class without player confirmation
- Accepting ambiguous replies ("ok", "sure", "I guess") as lock confirmation
- Generating DM Hooks disconnected from the backstory
- Proceeding to next phase without recap
