#!/usr/bin/env python3
"""
Regression tests for rpg-lore-weaver utility scripts.
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import export_character as exporter  # noqa: E402
import validate_character_output as validator  # noqa: E402


class CharacterToolTests(unittest.TestCase):
    def _read_example(self, name: str) -> str:
        path = ROOT_DIR / "examples" / name
        return exporter.normalize_text(path.read_text(encoding="utf-8"))

    def test_npc_quick_parser_keeps_sections_isolated(self) -> None:
        text = self._read_example("sample-npc-quick.md")
        data = exporter.parse_npc_quick(text)

        self.assertGreaterEqual(len(data["tiers"]), 3)

        tier2 = data["tiers"][1]
        self.assertNotRegex(tier2["hook"], r"\bWANT\b|\bCRACK\b|\bDM NOTES\b")
        self.assertNotRegex(tier2["want"], r"\bCRACK\b|\bDM NOTES\b")
        self.assertNotRegex(tier2["crack"], r"\bDM NOTES\b")

        tier3 = data["tiers"][2]
        self.assertNotRegex(tier3["dm_notes"], r"\bEVOLUTION POTENTIAL\b")

    def test_validator_requires_cultural_touchstone(self) -> None:
        text = self._read_example("sample-character-dnd.md")
        results = validator.validate_full_character(text)
        check = next(item for item in results if item["check"] == "DM Hook: Cultural Touchstone")
        self.assertTrue(check["passed"], check["detail"])

    def test_elevator_pitch_must_be_exactly_one_sentence(self) -> None:
        text = (
            "📌 ELEVATOR PITCH\n"
            "First sentence. Second sentence.\n\n"
            "👤 APPEARANCE & VIBE\nLooks simple.\n\n"
            "📖 BACKSTORY\nStory text.\n\n"
            "🧠 PSYCHOLOGICAL PROFILE\n"
            "- Personality: Calm\n"
            "- Ideals: Duty\n"
            "- Bonds: Party\n"
            "- Flaws: Pride\n"
            "- Fear: Failure\n"
            "- Desire vs Need: WANTS glory, NEEDS humility\n\n"
            "🔗 CONNECTIONS\n"
            "- Ally: A\n"
            "- Mentor: B\n"
            "- Rival: C\n\n"
            "🎣 DM HOOKS\n"
            "- Secret: X\n"
            "- Unresolved Thread: Y\n"
            "- Evolution Arc: Z\n"
            "- Cultural Touchstone: Q\n"
        )
        results = validator.validate_full_character(text)
        pitch_check = next(item for item in results if item["check"] == "Elevator Pitch: ONE sentence")
        self.assertFalse(pitch_check["passed"])

        one_sentence = re.sub("First sentence. Second sentence.", "Only one sentence.", text)
        ok_results = validator.validate_full_character(one_sentence)
        ok_pitch = next(item for item in ok_results if item["check"] == "Elevator Pitch: ONE sentence")
        self.assertTrue(ok_pitch["passed"])


if __name__ == "__main__":
    unittest.main()
