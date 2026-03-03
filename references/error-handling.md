---
description: "Reference for rpg-lore-weaver: error handling, recovery strategies, and technical implementation notes. Load only when needed."
metadata:
  tags: [rpg-lore-weaver, reference, error-handling, recovery, implementation]
---

# Error Handling & Technical Notes

Strategies for handling common problems during character creation, plus technical guidance for AI behavior.

## Error Handling

### User Doesn't Know the System or Setting

Offer 4 options and ask for a choice:

1. D&D 5e — Forgotten Realms
2. Pathfinder 2e — Golarion
3. Daggerheart
4. System-agnostic

### User Gives Generic/Shallow Answers

Use probing follow-ups focused on **sensory memory**, **consequence**, and **blame**:

- How did it happen (sudden or slow)?
- What did they perceive (sound/smell/silence)?
- Who do they blame? Who _should_ they blame?

### User Is Stuck on a Phase

Offer a recovery menu:

1. 3 tailored options (A/B/C)
2. Skip and return later
3. AI proposes based on existing material
4. Borrow from a known fictional inspiration

### Conflicting Character Details

Flag the contradiction and let the player choose:

1. Keep the new version
2. Keep the original version
3. Convert into intentional internal contradiction

---

## Error Recovery

When the creative process stalls or breaks, use these recovery strategies:

**Player is stuck / gives generic answers:**

- Switch from open-ended to A/B/C multiple-choice
- Roll on a table from `references/random-tables.md`
- Offer an archetype from `references/character-archetypes.md`
- Ask a sensory question: "Describe a smell, a sound, or a texture from their past"

**Player contradicts themselves:**

- Don't correct — offer the contradiction as a character feature (see Consistency Detection)
- Ask: "Both are interesting. Which feels more TRUE to this character?"

**Player wants to restart mid-creation:**

- Save everything done so far — it might inform the new character
- Ask: "What's not working? The concept, the tone, or the direction?"
- Offer to keep specific elements they liked

**Player loses interest in the process:**

- Switch to NPC Quick Mode (`references/npc-quick-mode.md`) for a faster result
- Offer to skip to Phase 5 with what's established and fill gaps later

**Player changes system mid-creation:**

- Use `references/system-conversion.md` to port the narrative core
- Only mechanical elements need to change — the story transfers

---

## Technical Implementation Notes

**Conversational Flow:**

- Use open-ended questions in early phases to encourage creativity
- Switch to multiple-choice options (A/B/C) when the user seems stuck
- After each phase, provide a brief recap connecting new details to previous ones
- Maintain a running mental model of the character to check for consistency

**Phase Transitions & Context Optimization:**

- Display the progress bar before starting each new phase
- Summarize what was established before moving forward
- Allow the user to go back and revise previous phases at any time
- **Context Compression Trigger:** If conversation becomes very long (reaching Phase 4+ after deep exploration), silently compress older phases into this format:

```
📦 COMPRESSED CONTEXT
   Origin: [2-3 key facts]
   Family: [legacy + key figure]
   Motivations: [push/pull]
   Personality: [2 traits + speech pattern]
   Ideals: [core belief + contradiction]
   Weaknesses: [fatal flaw + hidden vulnerability]
   Decisions: [key crossroad + consequence]
```

This preserves the "Artifact Trail" while keeping the context window optimized for synthesis.

**Output Generation:**

- The final character document should weave all 10 pillars into a narrative, not a list
- DM Hooks should emerge organically from the backstory, not feel bolted on
- Keep the Elevator Pitch to exactly one sentence — this forces clarity

**Tone Adaptation:**

- Match the writing tone to the campaign's tone (grimdark → darker language, comedic → lighter)
- Adjust vocabulary complexity based on system (D&D → fantasy terms, Ordem Paranormal → urban horror)
- For character conversion between systems, see `references/system-conversion.md`
