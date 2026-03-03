"""
Shared utilities for RPG Lore Weaver scripts.
Centralizes logic for frontmatter parsing, text cleaning, and mojibake repair.
"""

import re
from pathlib import Path
from typing import Tuple, List, Optional

# Constants
CONTROL_CHAR_RE = re.compile(r"[\u0080-\u009f]")
EMOJI_NOISE_RE = re.compile(r"[\u2600-\u27BF\U0001F300-\U0001FAFF]")

MOJIBAKE_REPLACEMENTS: dict[str, str] = {
    "\u00e2\u20ac\u2122": "'",
    "\u00e2\u20ac\u02dc": "'",
    "\u00e2\u20ac\u0153": '"',
    "\u00e2\u20ac\u009d": '"',
    "\u00e2\u20ac\u201c": "-",
    "\u00e2\u20ac\u201d": "-",
    "\u00e2\u20ac\u00a6": "...",
    "\u00e2\u20ac\u00a2": "-",
    "\u00e2\u0080\u0099": "'",
    "\u00e2\u0080\u0098": "'",
    "\u00e2\u0080\u009c": '"',
    "\u00e2\u0080\u009d": '"',
    "\u00e2\u0080\u0093": "-",
    "\u00e2\u0080\u0094": "-",
    "\u00e2\u0080\u00a6": "...",
    "\u00c2\u00a0": " ",
    "\u00c2\u00bd": "1/2",
    "\u00c3\u00a9": "e",
    "\u00c3\u00a8": "e",
    "\u00c3\u00aa": "e",
    "\u00c3\u00ad": "i",
    "\u00c3\u00ac": "i",
    "\u00c3\u00a1": "a",
    "\u00c3\u00a0": "a",
    "\u00c3\u00a3": "a",
    "\u00c3\u00b3": "o",
    "\u00c3\u00b2": "o",
    "\u00c3\u00ba": "u",
    "\u00c3\u00b9": "u",
    "\u00c3\u00b1": "n",
}

def read_text(path: Path) -> str:
    """Read text with error replacement."""
    return path.read_text(encoding="utf-8", errors="replace")

def split_frontmatter(text: str) -> Tuple[str, str]:
    """Split text into (frontmatter, body). Frontmatter includes delimiters."""
    text = text.lstrip("\ufeff")
    if not text.startswith("---\n"):
        return "", text
    end = text.find("\n---\n", 4)
    if end == -1:
        return "", text
    frontmatter = text[: end + 5]
    body = text[end + 5 :]
    return frontmatter, body

def parse_frontmatter_tags(frontmatter: str) -> List[str]:
    """Extract tags from frontmatter, supporting both old 'tags: []' and new 'triggers: - ' formats."""
    tags = []
    
    # Try new triggers format
    if "triggers:" in frontmatter:
        triggers_match = re.search(r'triggers:\s*\n((?:\s+-\s+.*\n?)+)', frontmatter)
        if triggers_match:
            content = triggers_match.group(1)
            tags = [line.strip().replace("- ", "").strip() for line in content.splitlines()]
            
    # Fallback/Additive: Try old tags format
    m_tags = re.search(r'tags:\s*\[(.*)\]', frontmatter)
    if m_tags:
        old_tags = [t.strip() for t in m_tags.group(1).split(",")]
        # Add only unique
        for t in old_tags:
            if t not in tags:
                tags.append(t)
                
    return tags

def parse_frontmatter_description(frontmatter: str) -> str:
    """Extract description from frontmatter."""
    m_desc = re.search(r'description:\s*(?:"|)(.*?)(?:"|)$', frontmatter, re.MULTILINE)
    if m_desc:
        return m_desc.group(1).strip()
    return ""

def sanitize_filename_title(path: Path) -> str:
    """Convert filename to a readable title."""
    stem = path.stem
    stem = re.sub(r"^\d+_?", "", stem)
    stem = stem.replace("_", " ").replace("-", " ")
    stem = re.sub(r"\s+", " ", stem).strip()
    return stem.title() if stem else path.stem

def mojibake_score(text: str) -> int:
    """Calculate a score for potential encoding errors."""
    marker_hits = sum(text.count(ch) for ch in ("\u00c3", "\u00e2", "\u00c2", "\u00f0", "\ufffd"))
    return marker_hits + len(CONTROL_CHAR_RE.findall(text))

def apply_mojibake_replacements(text: str) -> str:
    """Apply deterministic replacements for known mojibake artifacts."""
    fixed = text
    for source, target in MOJIBAKE_REPLACEMENTS.items():
        fixed = fixed.replace(source, target)
    fixed = fixed.replace("\ufeff", "")
    fixed = fixed.replace("\ufe0f", "")
    fixed = EMOJI_NOISE_RE.sub("", fixed)
    return fixed

def repair_mojibake(text: str) -> str:
    """Attempt to repair mojibake by guessing encoding layers."""
    current = text
    best_score = mojibake_score(current)
    for _ in range(3):
        improved = False
        for encoding in ("cp1252", "latin1"):
            try:
                candidate = current.encode(encoding, errors="ignore").decode("utf-8", errors="ignore")
            except (UnicodeEncodeError, UnicodeDecodeError, LookupError):
                continue
            candidate = apply_mojibake_replacements(candidate)
            score = mojibake_score(candidate)
            # Keep repair only when clearly better and without major shrinkage.
            if score + 3 < best_score and len(candidate) >= int(len(current) * 0.8):
                current = candidate
                best_score = score
                improved = True
        if not improved:
            break
    return apply_mojibake_replacements(current)

def detect_source_url(text: str) -> str:
    """Extract the first http/https URL from non-frontmatter text."""
    match = re.search(r"https?://\S+", text)
    return match.group(0).rstrip(").,") if match else "unknown"

def extract_readable_title(path: Path, text: str) -> str:
    """Extract a title from the first H1 or fallback to filename."""
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("# "):
            continue
        candidate = stripped[2:].strip()
        if not candidate:
            continue
        if candidate.lower().startswith("scraped content from:"):
            continue
        if mojibake_score(candidate) > 6:
            continue
        return candidate
    return sanitize_filename_title(path)
