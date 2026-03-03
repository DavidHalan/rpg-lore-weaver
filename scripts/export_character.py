#!/usr/bin/env python3
"""
export_character.py

Export rpg-lore-weaver outputs to different formats.
Supports:
1) Full character documents
2) NPC Quick Mode documents

Formats:
    - json
    - clean
    - homebrewery

Usage:
    python export_character.py <character_file.md> --format json
    python export_character.py <character_file.md> --format clean -o clean.md
    python export_character.py <character_file.md> --format homebrewery
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def safe_print(text: str = "", file=sys.stdout) -> None:
    try:
        print(text, file=file)
    except UnicodeEncodeError:
        encoding = getattr(file, "encoding", None) or "utf-8"
        fallback = text.encode(encoding, errors="replace").decode(encoding, errors="replace")
        print(fallback, file=file)


def configure_stdout() -> None:
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if callable(reconfigure):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except (ValueError, OSError):
            pass


def normalize_text(text: str) -> str:
    """Normalize common mojibake sequences into intended Unicode characters."""
    replacements = {
        "â€¢": "•",
        "â€”": "—",
        "â†’": "→",
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


def detect_mode(text: str) -> str:
    quick_markers = [
        "NPC Quick Mode",
        "Tier 1:",
        "Tier 2:",
        "Tier 3:",
        "ONE-LINE HOOK",
        "Rapid-Fire Input",
    ]
    return "npc-quick" if any(marker in text for marker in quick_markers) else "full"


def parse_full_character(text: str) -> dict:
    character: dict = {"mode": "full"}

    name_match = re.search(r"═+\s*\n\s*(.+?)(?:\s*—\s*(.+?))?\s*\n\s*═+", text)
    if name_match:
        character["name"] = name_match.group(1).strip()
        character["epithet"] = name_match.group(2).strip() if name_match.group(2) else ""

    sections = {
        "elevator_pitch": r"(?:ELEVATOR PITCH|📌)\s*\n\s*(.+?)(?=\n\s*(?:👤|🧠|📖|🔗|🎣|═))",
        "appearance": r"(?:APPEARANCE & VIBE|👤)\s*\n\s*(.+?)(?=\n\s*(?:📌|🧠|📖|🔗|🎣|═))",
        "backstory": r"(?:BACKSTORY|📖)\s*\n\s*(.+?)(?=\n\s*(?:📌|👤|🧠|🔗|🎣|═))",
    }
    for key, pattern in sections.items():
        match = re.search(pattern, text, re.DOTALL)
        if match:
            character[key] = match.group(1).strip()

    psych = {}
    for field in ["Personality", "Ideals", "Bonds", "Flaws", "Fear", "Desire vs Need"]:
        match = re.search(
            rf"(?:•|-)\s*{re.escape(field)}:\s*(.+?)(?=\n\s*(?:•|-)|\n\s*\n|\n\s*🔗)",
            text,
            re.DOTALL,
        )
        if match:
            psych[field.lower().replace(" ", "_")] = match.group(1).strip()
    character["psychological_profile"] = psych

    connections = {}
    for field in ["Ally", "Mentor", "Rival"]:
        match = re.search(
            rf"(?:•|-)\s*{field}:\s*(.+?)(?=\n\s*(?:•|-)|\n\s*\n|\n\s*🎣)",
            text,
            re.DOTALL,
        )
        if match:
            connections[field.lower()] = match.group(1).strip()
    character["connections"] = connections

    hooks = {}
    for field in ["Secret", "Unresolved Thread", "Evolution Arc", "Cultural Touchstone"]:
        match = re.search(
            rf"(?:•|-)\s*{re.escape(field)}:\s*(.+?)(?=\n\s*(?:•|-)|\n\s*\n|\n\s*═+)",
            text,
            re.DOTALL,
        )
        if match:
            hooks[field.lower().replace(" ", "_")] = match.group(1).strip()
    character["dm_hooks"] = hooks

    return character


def _extract_labeled_block(block: str, labels: list[str]) -> str:
    sections = _parse_labeled_sections(block)
    label_keys = [label.upper() for label in labels]
    for key in label_keys:
        if key in sections:
            return sections[key]
    return ""


def _parse_labeled_sections(block: str) -> dict[str, str]:
    headings = [
        "EVOLUTION POTENTIAL",
        "VOICE & MANNERISMS",
        "ONE-LINE HOOK",
        "DM NOTES",
        "DM HOOKS",
        "CONNECTIONS",
        "CRACK",
        "WANT",
        "HOOK",
    ]

    sections: dict[str, str] = {}
    current_key: str | None = None
    buffer: list[str] = []

    def parse_heading(line: str) -> tuple[str, str] | None:
        candidate = line.strip()
        if not candidate:
            return None

        upper = candidate.upper()
        for heading in headings:
            idx = upper.find(heading)
            if idx < 0:
                continue
            before_ok = idx == 0 or not upper[idx - 1].isalnum()
            end_idx = idx + len(heading)
            after_ok = end_idx >= len(upper) or not upper[end_idx].isalnum()
            if not (before_ok and after_ok):
                continue
            prefix = candidate[:idx].strip()
            # Allow short noisy prefixes (emoji / mojibake markers) before headings.
            if prefix and len(prefix) > 8:
                continue
            remainder = candidate[idx + len(heading) :].lstrip()
            if remainder.startswith(":"):
                remainder = remainder[1:].lstrip()
            return heading, remainder
        return None

    def flush() -> None:
        nonlocal current_key, buffer
        if current_key is None:
            return
        text = "\n".join(buffer).strip()
        text = re.sub(r"\n\s+", "\n", text)
        text = re.sub(r"\n?`{3,}\s*$", "", text).strip()
        text = re.sub(r"\n?_{1,2}Total creation time:.*$", "", text, flags=re.IGNORECASE).strip()
        text = re.sub(r"\n?\s*[═]{8,}\s*$", "", text).strip()
        if text:
            sections[current_key] = text
        current_key = None
        buffer = []

    for raw_line in block.splitlines():
        line = raw_line.rstrip()
        if current_key is not None and line.strip().startswith("```"):
            flush()
            continue

        parsed = parse_heading(line)
        if parsed:
            flush()
            current_key = parsed[0]
            inline = parsed[1]
            buffer = [inline] if inline else []
            continue

        if current_key is None:
            continue

        if re.match(r"^\s*[═]{8,}\s*$", line):
            continue
        buffer.append(line)

    flush()
    return sections


def parse_npc_quick(text: str) -> dict:
    data: dict = {"mode": "npc-quick", "tiers": []}

    name_match = re.search(r"🔨\s*([^\n—]+)(?:\s*—\s*([^\n]+))?", text)
    if name_match:
        data["name"] = name_match.group(1).strip()
        data["epithet"] = (name_match.group(2) or "").strip()

    tier_pattern = re.compile(
        r"##\s*Tier\s*(\d+):\s*([^\n]+)\n(.*?)(?=\n---\n|\n##\s*Tier\s*\d+:|\Z)",
        re.IGNORECASE | re.DOTALL,
    )
    for tier_num, tier_title, block in tier_pattern.findall(text):
        tier_data = {
            "tier": int(tier_num),
            "title": tier_title.strip(),
            "hook": _extract_labeled_block(block, ["ONE-LINE HOOK", "HOOK", "Hook"]),
            "want": _extract_labeled_block(block, ["WANT", "Want"]),
            "crack": _extract_labeled_block(block, ["CRACK", "Crack"]),
            "dm_notes": _extract_labeled_block(block, ["DM NOTES", "DM HOOKS"]),
        }
        data["tiers"].append(tier_data)

    if not data["tiers"]:
        data["tiers"].append(
            {
                "tier": 1,
                "title": "Quick NPC",
                "hook": _extract_labeled_block(text, ["ONE-LINE HOOK", "HOOK", "Hook"]),
                "want": _extract_labeled_block(text, ["WANT", "Want"]),
                "crack": _extract_labeled_block(text, ["CRACK", "Crack"]),
                "dm_notes": _extract_labeled_block(text, ["DM NOTES", "DM HOOKS"]),
            }
        )

    return data


def export_json(data: dict) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False)


def export_clean(text: str) -> str:
    clean = re.sub(r"[═╔╗╚╝╠╣║╬╦╩]+", "", text)
    clean = re.sub(r"\n{3,}", "\n\n", clean)
    replacements = {
        "📌 ELEVATOR PITCH": "## Elevator Pitch",
        "👤 APPEARANCE & VIBE": "## Appearance & Vibe",
        "📖 BACKSTORY": "## Backstory",
        "🧠 PSYCHOLOGICAL PROFILE": "## Psychological Profile",
        "🔗 CONNECTIONS": "## Connections",
        "🎣 DM HOOKS": "## DM Hooks",
        "🎯 WANT": "## Want",
        "💔 CRACK": "## Crack",
    }
    for old, new in replacements.items():
        clean = clean.replace(old, new)
    return clean.strip()


def export_homebrewery(data: dict) -> str:
    if data.get("mode") == "npc-quick":
        name = data.get("name", "Unknown NPC")
        epithet = data.get("epithet", "")
        title = f"{name} — {epithet}" if epithet else name
        lines = [f"# {title}", "", "## NPC Quick Mode"]
        for tier in data.get("tiers", []):
            lines.extend(
                [
                    "",
                    f"### Tier {tier.get('tier', '?')}: {tier.get('title', '')}",
                    f"- **Hook:** {tier.get('hook', '')}",
                    f"- **Want:** {tier.get('want', '')}",
                    f"- **Crack:** {tier.get('crack', '')}",
                ]
            )
            dm_notes = tier.get("dm_notes", "")
            if dm_notes:
                lines.append(f"- **DM Notes:** {dm_notes}")
        return "\n".join(lines).strip()

    name = data.get("name", "Unknown")
    epithet = data.get("epithet", "")
    title = f"{name} — {epithet}" if epithet else name
    lines = [
        f"# {title}",
        "",
        "___",
        f"***{data.get('elevator_pitch', '')}***",
        "___",
        "",
        "## Appearance & Vibe",
        data.get("appearance", ""),
        "",
        "## Backstory",
        data.get("backstory", ""),
        "",
        "## Psychological Profile",
    ]

    for key, value in data.get("psychological_profile", {}).items():
        lines.append(f"- **{key.replace('_', ' ').title()}:** {value}")

    lines.extend(["", "## Connections"])
    for key, value in data.get("connections", {}).items():
        lines.append(f"- **{key.title()}:** {value}")

    lines.extend(["", "## DM Hooks", "", "{{classNote"])
    for key, value in data.get("dm_hooks", {}).items():
        lines.append(f"##### {key.replace('_', ' ').title()}")
        lines.append(value)
        lines.append("")
    lines.append("}}")

    return "\n".join(lines).strip()


def main() -> None:
    configure_stdout()

    parser = argparse.ArgumentParser(description="Export rpg-lore-weaver output")
    parser.add_argument("file", help="Path to markdown file")
    parser.add_argument(
        "--format",
        choices=["json", "clean", "homebrewery"],
        default="json",
        help="Output format (default: json)",
    )
    parser.add_argument(
        "--mode",
        choices=["auto", "full", "npc-quick"],
        default="auto",
        help="Input mode (default: auto)",
    )
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    args = parser.parse_args()

    filepath = Path(args.file)
    if not filepath.exists():
        safe_print(f"❌ Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(2)

    text = normalize_text(filepath.read_text(encoding="utf-8"))
    mode = detect_mode(text) if args.mode == "auto" else args.mode
    parsed = parse_npc_quick(text) if mode == "npc-quick" else parse_full_character(text)

    if args.format == "json":
        output = export_json(parsed)
    elif args.format == "clean":
        output = export_clean(text)
    else:
        output = export_homebrewery(parsed)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(output, encoding="utf-8")
        safe_print(f"✅ Exported to {output_path} ({args.format} format)")
    else:
        safe_print(output)


if __name__ == "__main__":
    main()
