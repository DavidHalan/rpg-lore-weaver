#!/usr/bin/env python3
"""
validate_character_output.py

Validate rpg-lore-weaver outputs for:
1) Full character document format
2) NPC Quick Mode format
3) Villain/Antagonist format

Usage:
    python validate_character_output.py <character_file.md>
    python validate_character_output.py --text "paste character text here"
    python validate_character_output.py <character_file.md> --mode full
    python validate_character_output.py <character_file.md> --mode npc-quick

Exit codes:
    0 - All validations passed
    1 - One or more validations failed
    2 - File not found or invalid input
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


FULL_REQUIRED_SECTIONS = {
    "ELEVATOR PITCH": {"emoji": "📌"},
    "APPEARANCE & VIBE": {"emoji": "👤"},
    "BACKSTORY": {"emoji": "📖"},
    "PSYCHOLOGICAL PROFILE": {"emoji": "🧠"},
    "CONNECTIONS": {"emoji": "🔗"},
    "DM HOOKS": {"emoji": "🎣"},
}

PSYCH_FIELDS = ["Personality", "Ideals", "Bonds", "Flaws", "Fear", "Desire vs Need"]
CONNECTION_FIELDS = ["Ally", "Mentor", "Rival"]
HOOK_FIELDS = ["Secret", "Unresolved Thread", "Evolution Arc", "Cultural Touchstone"]

VILLAIN_SECTIONS = {
    "ELEVATOR PITCH": {"emoji": "📌"},
    "THE MIRROR": {"emoji": "🪞"},
    "THE PLAN": {"emoji": "📋"},
    "THE CRACKS": {"emoji": "💔"},
    "WEB": {"emoji": "🔗"},
    "DM HOOKS": {"emoji": "🎣"},
}

VILLAIN_MIRROR_FIELDS = ["The Wound", "The Logic", "The Line"]
VILLAIN_PLAN_FIELDS = ["Goal", "Method", "Timeline", "Resources"]
VILLAIN_CRACK_FIELDS = ["Blind Spot", "Redemption"]
VILLAIN_HOOK_FIELDS = ["Secret", "Escalation Beat", "Moral Dilemma"]


def normalize_text(text: str) -> str:
    """Normalize common mojibake sequences into intended Unicode characters."""
    replacements = {
        "â€¢": "•",
        "â€”": "—",
        "â†’": "→",
        "âœ…": "✅",
        "âŒ": "❌",
        "âš ï¸": "⚠️",
        "â•": "═",
        "ðŸ“Œ": "📌",
        "ðŸ‘¤": "👤",
        "ðŸ“–": "📖",
        "ðŸ§ ": "🧠",
        "ðŸ”—": "🔗",
        "ðŸŽ£": "🎣",
        "ðŸ”¨": "🔨",
        "ðŸŽ¯": "🎯",
        "ðŸ’”": "💔",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def safe_print(text: str = "", file=sys.stdout) -> None:
    """Print text and fall back gracefully if terminal encoding lacks Unicode support."""
    try:
        print(text, file=file)
    except UnicodeEncodeError:
        encoding = getattr(file, "encoding", None) or "utf-8"
        fallback = text.encode(encoding, errors="replace").decode(encoding, errors="replace")
        print(fallback, file=file)


def configure_stdout() -> None:
    """Prefer UTF-8 output when supported by the Python runtime."""
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if callable(reconfigure):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except (ValueError, OSError):
            # Ignore if stream cannot be reconfigured in this environment.
            pass


def detect_mode(text: str) -> str:
    quick_markers = [
        "NPC Quick Mode",
        "Tier 1:",
        "Tier 2:",
        "Tier 3:",
        "ONE-LINE HOOK",
        "Rapid-Fire Input",
    ]
    villain_markers = [
        "VILLAIN PROFILE",
        "THE MIRROR",
        "THE PLAN",
        "THE CRACKS",
    ]
    if any(marker in text for marker in quick_markers):
        return "npc-quick"
    if any(marker in text for marker in villain_markers):
        return "villain"
    return "full"


def validate_full_character(text: str) -> list[dict]:
    results: list[dict] = []

    for section_name, info in FULL_REQUIRED_SECTIONS.items():
        found = section_name in text or info["emoji"] in text
        results.append(
            {
                "check": f"Section: {section_name}",
                "passed": found,
                "detail": "Found" if found else f"Missing section '{section_name}' ({info['emoji']})",
            }
        )

    pitch_match = re.search(
        r"(?:ELEVATOR PITCH|📌)\s*\n\s*(.+?)(?:\n\n|\n\s*(?:👤|🧠|📖|🔗|🎣))",
        text,
        re.DOTALL,
    )
    if pitch_match:
        pitch_text = pitch_match.group(1).strip()
        sentences = [s.strip() for s in re.split(r"[.!?]+", pitch_text) if s.strip()]
        is_one = len(sentences) == 1
        results.append(
            {
                "check": "Elevator Pitch: ONE sentence",
                "passed": is_one,
                "detail": f"{'Good' if is_one else 'Too many sentences'} ({len(sentences)} found)",
            }
        )
    else:
        results.append(
            {
                "check": "Elevator Pitch: ONE sentence",
                "passed": False,
                "detail": "Could not locate Elevator Pitch content",
            }
        )

    for field in PSYCH_FIELDS:
        found = re.search(rf"(?:•|-)\s*{re.escape(field)}:", text) is not None
        results.append(
            {
                "check": f"Psych Profile: {field}",
                "passed": found,
                "detail": "Found" if found else f"Missing '{field}' in Psychological Profile",
            }
        )

    for field in CONNECTION_FIELDS:
        found = re.search(rf"(?:•|-)\s*{re.escape(field)}:", text) is not None
        results.append(
            {
                "check": f"Connection: {field}",
                "passed": found,
                "detail": "Found" if found else f"Missing '{field}' in Connections",
            }
        )

    for field in HOOK_FIELDS:
        found = re.search(rf"(?:•|-)\s*{re.escape(field)}:", text) is not None
        results.append(
            {
                "check": f"DM Hook: {field}",
                "passed": found,
                "detail": "Found" if found else f"Missing '{field}' in DM Hooks",
            }
        )

    desire_match = re.search(
        r"Desire vs Need:\s*(.+?)(?=\n\s*\n|\n\s*🔗|\n\s*═+)",
        text,
        re.DOTALL,
    )
    if desire_match:
        desire_text = desire_match.group(1).strip()
        has_both = bool(re.search(r"\bWANTS?\b", desire_text, re.IGNORECASE)) and bool(
            re.search(r"\bNEEDS?\b", desire_text, re.IGNORECASE)
        )
        results.append(
            {
                "check": "Desire vs Need: Distinct",
                "passed": has_both,
                "detail": "Both WANT and NEED present"
                if has_both
                else "Should clearly separate WANT from NEED",
            }
        )

    name_match = re.search(r"═+\s*\n\s*(.+?)(?:\s*—\s*(.+?))?\s*\n\s*═+", text)
    if name_match:
        results.append(
            {
                "check": "Character Name & Epithet",
                "passed": True,
                "detail": f"Found: {name_match.group(0).strip()[:60]}...",
            }
        )
    else:
        results.append(
            {
                "check": "Character Name & Epithet",
                "passed": False,
                "detail": "Missing character name header with ═══ borders",
            }
        )

    return results


def validate_npc_quick(text: str) -> list[dict]:
    results: list[dict] = []

    tiers = re.findall(r"##\s*Tier\s*\d+:", text, re.IGNORECASE)
    has_tier = len(tiers) >= 1
    results.append(
        {
            "check": "Quick Mode: Tier section present",
            "passed": has_tier,
            "detail": f"Found {len(tiers)} tier section(s)" if has_tier else "No 'Tier X' section found",
        }
    )

    has_name = bool(re.search(r"(?:🔨\s*)?[A-Z][A-Z\s]+(?:—|$)", text))
    results.append(
        {
            "check": "Quick Mode: NPC name/title",
            "passed": has_name,
            "detail": "Found" if has_name else "Could not locate NPC name/title block",
        }
    )

    has_hook = "ONE-LINE HOOK" in text or bool(re.search(r"\bHook:\s*", text))
    results.append(
        {
            "check": "Quick Mode: Hook present",
            "passed": has_hook,
            "detail": "Found" if has_hook else "Missing 'ONE-LINE HOOK' or 'Hook:'",
        }
    )

    has_want = "WANT" in text or bool(re.search(r"\bWant:\s*", text))
    results.append(
        {
            "check": "Quick Mode: Want present",
            "passed": has_want,
            "detail": "Found" if has_want else "Missing WANT/Want field",
        }
    )

    has_crack = "CRACK" in text or bool(re.search(r"\bCrack:\s*", text))
    results.append(
        {
            "check": "Quick Mode: Crack present",
            "passed": has_crack,
            "detail": "Found" if has_crack else "Missing CRACK/Crack field",
        }
    )

    has_dm_notes = "DM NOTES" in text or "DM HOOKS" in text
    results.append(
        {
            "check": "Quick Mode: DM-facing section",
            "passed": has_dm_notes,
            "detail": "Found" if has_dm_notes else "Missing DM NOTES/DM HOOKS section",
        }
    )

    return results


def validate_villain(text: str) -> list[dict]:
    results: list[dict] = []

    for section_name, info in VILLAIN_SECTIONS.items():
        found = section_name in text or info["emoji"] in text
        results.append(
            {
                "check": f"Section: {section_name}",
                "passed": found,
                "detail": "Found" if found else f"Missing section '{section_name}' ({info['emoji']})",
            }
        )

    pitch_match = re.search(
        r"(?:ELEVATOR PITCH|📌)\s*\n\s*(.+?)(?:\n\n|\n\s*(?:🪞|📋|💔|🔗|🎣))",
        text,
        re.DOTALL,
    )
    if pitch_match:
        pitch_text = pitch_match.group(1).strip()
        sentences = [s.strip() for s in re.split(r"[.!?]+", pitch_text) if s.strip()]
        is_one = len(sentences) == 1
        results.append(
            {
                "check": "Elevator Pitch: ONE sentence",
                "passed": is_one,
                "detail": f"{'Good' if is_one else 'Too many sentences'} ({len(sentences)} found)",
            }
        )
    else:
        results.append(
            {
                "check": "Elevator Pitch: ONE sentence",
                "passed": False,
                "detail": "Could not locate Elevator Pitch content",
            }
        )

    for field in VILLAIN_MIRROR_FIELDS:
        found = re.search(rf"(?:•|-)\s*{re.escape(field)}:", text) is not None
        results.append(
            {
                "check": f"Mirror: {field}",
                "passed": found,
                "detail": "Found" if found else f"Missing '{field}' in The Mirror",
            }
        )

    for field in VILLAIN_PLAN_FIELDS:
        found = re.search(rf"(?:•|-)\s*{re.escape(field)}:", text) is not None
        results.append(
            {
                "check": f"Plan: {field}",
                "passed": found,
                "detail": "Found" if found else f"Missing '{field}' in The Plan",
            }
        )

    for field in VILLAIN_CRACK_FIELDS:
        found = re.search(rf"(?:•|-)\s*{re.escape(field)}:", text) is not None
        results.append(
            {
                "check": f"Cracks: {field}",
                "passed": found,
                "detail": "Found" if found else f"Missing '{field}' in The Cracks",
            }
        )

    for field in VILLAIN_HOOK_FIELDS:
        found = re.search(rf"(?:•|-)\s*{re.escape(field)}:", text) is not None
        results.append(
            {
                "check": f"DM Hook: {field}",
                "passed": found,
                "detail": "Found" if found else f"Missing '{field}' in DM Hooks",
            }
        )

    name_match = re.search(r"═+\s*\n\s*(.+?)(?:\s*—\s*(.+?))?\s*\n\s*═+", text)
    if name_match:
        results.append(
            {
                "check": "Villain Name & Epithet",
                "passed": True,
                "detail": f"Found: {name_match.group(0).strip()[:60]}...",
            }
        )
    else:
        results.append(
            {
                "check": "Villain Name & Epithet",
                "passed": False,
                "detail": "Missing villain name header with ═══ borders",
            }
        )

    return results


def print_results(results: list[dict], mode: str) -> bool:
    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    all_passed = passed == total

    safe_print()
    safe_print(f"🔍 rpg-lore-weaver — Validation Report ({mode})")
    safe_print("=" * 60)
    safe_print()

    for result in results:
        icon = "✅" if result["passed"] else "❌"
        safe_print(f"  {icon} {result['check']}")
        if not result["passed"]:
            safe_print(f"     └─ {result['detail']}")

    safe_print()
    safe_print("─" * 60)
    if all_passed:
        safe_print(f"  ✅ All {total} checks passed!")
    else:
        safe_print(f"  ⚠️  {passed}/{total} checks passed, {total - passed} failed")
    safe_print()

    return all_passed


def main() -> None:
    configure_stdout()

    parser = argparse.ArgumentParser(description="Validate rpg-lore-weaver output")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("file", nargs="?", help="Path to markdown file")
    group.add_argument("--text", help="Character text to validate directly")
    parser.add_argument(
        "--mode",
        choices=["auto", "full", "npc-quick", "villain"],
        default="auto",
        help="Validation mode (default: auto)",
    )

    args = parser.parse_args()

    if args.text:
        text = normalize_text(args.text)
    else:
        filepath = Path(args.file)
        if not filepath.exists():
            safe_print(f"❌ Error: File not found: {filepath}", file=sys.stderr)
            sys.exit(2)
        text = normalize_text(filepath.read_text(encoding="utf-8"))

    mode = detect_mode(text) if args.mode == "auto" else args.mode
    if mode == "npc-quick":
        results = validate_npc_quick(text)
    elif mode == "villain":
        results = validate_villain(text)
    else:
        results = validate_full_character(text)

    all_passed = print_results(results, mode)
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
