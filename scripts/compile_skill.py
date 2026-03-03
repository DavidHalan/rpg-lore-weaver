#!/usr/bin/env python3
"""
compile_skill.py

Compile rpg-lore-weaver into a single manual file for copy-paste usage in LLMs.

Profiles:
  full   — SKILL.md + all references + all systems (default)
  system — SKILL.md + core references + ONE system only (use --system)
  micro  — SKILL.md + system-prompts.md only (minimal context)

Usage:
  python scripts/compile_skill.py                         # full manual
  python scripts/compile_skill.py --profile system --system dnd5e
  python scripts/compile_skill.py --profile micro
  python scripts/compile_skill.py --profile system --system coc -o manual-coc.md
"""

from __future__ import annotations

import argparse
import glob
import os
from pathlib import Path


# Core references always included in 'system' profile
CORE_REFERENCES = {
    "10-pillars-deep-dive.md",
    "techniques-and-examples.md",
    "system-prompts.md",
    "formatting-templates.md",
    "character-archetypes.md",
    "npc-quick-mode.md",
    "villain-mode.md",
    "resource-index.md",
}

# System name aliases for user convenience
SYSTEM_ALIASES = {
    "dnd": "dnd5e",
    "dnd5e": "dnd5e",
    "d&d": "dnd5e",
    "d&d5e": "dnd5e",
    "pathfinder": "pathfinder2e",
    "pf2e": "pathfinder2e",
    "pathfinder2e": "pathfinder2e",
    "daggerheart": "daggerheart",
    "dh": "daggerheart",
    "coc": "coc",
    "cthulhu": "coc",
    "callofcthulhu": "coc",
    "tormenta": "tormenta20",
    "tormenta20": "tormenta20",
    "t20": "tormenta20",
    "ordem": "ordem-paranormal",
    "op": "ordem-paranormal",
    "ordemparanormal": "ordem-paranormal",
    "ordem-paranormal": "ordem-paranormal",
}


def _relpath(path: str, root_dir: str) -> str:
    return os.path.relpath(path, root_dir).replace("\\", "/")


def _estimate_tokens(text: str) -> int:
    """Rough token estimate: ~4 chars per token for English/mixed text."""
    return len(text) // 4


def _build_reference_index(paths: list[str], root_dir: str) -> str:
    lines = []
    for path in paths:
        rel = _relpath(path, root_dir)
        lines.append(f"- `{rel}` -> `## REFERENCE FILE: {rel}`")
    return "\n".join(lines)


def _build_system_index(paths: list[str], root_dir: str) -> str:
    lines = []
    for path in paths:
        rel = _relpath(path, root_dir)
        lines.append(f"- `{rel}` -> `## SYSTEM FILE: {rel}`")
    return "\n".join(lines)


def _resolve_system(system_arg: str) -> str:
    """Resolve system alias to canonical filename prefix."""
    key = system_arg.lower().replace(" ", "").replace("_", "")
    canonical = SYSTEM_ALIASES.get(key)
    if canonical is None:
        valid = sorted(set(SYSTEM_ALIASES.values()))
        raise ValueError(
            f"Unknown system '{system_arg}'. Valid systems: {', '.join(valid)}"
        )
    return canonical


def _find_system_file(systems_dir: str, system_name: str) -> str | None:
    """Find the system rules file matching the canonical name."""
    pattern = os.path.join(systems_dir, f"{system_name}-rules.md")
    matches = glob.glob(pattern)
    return matches[0] if matches else None


def compile_skill(
    output_file: str | None = None,
    profile: str = "full",
    system: str | None = None,
) -> None:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    skill_file = os.path.join(root_dir, "SKILL.md")
    references_dir = os.path.join(root_dir, "references")
    systems_dir = os.path.join(root_dir, "systems")

    # Resolve output file name
    if output_file is None:
        if profile == "full":
            output_file = os.path.join(root_dir, "rpg-lore-weaver-manual.md")
        elif profile == "system" and system:
            canonical = _resolve_system(system)
            output_file = os.path.join(root_dir, f"rpg-lore-weaver-manual-{canonical}.md")
        elif profile == "micro":
            output_file = os.path.join(root_dir, "rpg-lore-weaver-manual-micro.md")
        else:
            output_file = os.path.join(root_dir, "rpg-lore-weaver-manual.md")
    else:
        output_file = os.path.abspath(output_file)

    content: list[str] = []

    # --- SKILL.md (always included) ---
    print(f"Reading {skill_file}...")
    with open(skill_file, "r", encoding="utf-8") as file:
        content.append(file.read())

    # --- References ---
    if profile == "micro":
        # Micro: only system-prompts.md
        micro_ref = os.path.join(references_dir, "system-prompts.md")
        if os.path.exists(micro_ref):
            rel = _relpath(micro_ref, root_dir)
            print(f"Adding reference: {rel}...")
            with open(micro_ref, "r", encoding="utf-8") as file:
                ref_content = file.read()
            content.append(
                "\n\n---\n\n"
                "# REFERENCE MATERIALS (Micro Profile)\n\n"
                f"## REFERENCE FILE: {rel}\n\n{ref_content}"
            )
    else:
        # Full or System: include references
        all_ref_files = sorted(glob.glob(os.path.join(references_dir, "*.md")))

        if profile == "system":
            # Filter to core references only
            ref_files = [
                f for f in all_ref_files
                if Path(f).name in CORE_REFERENCES
            ]
        else:
            ref_files = all_ref_files

        content.append(
            "\n\n---\n\n"
            "# REFERENCE MATERIALS\n\n"
            "The following sections contain reference content mentioned in the instructions above.\n\n"
            "## Reference Path Map\n\n"
            "When the skill mentions a path like `references/random-tables.md`, use the matching\n"
            "`REFERENCE FILE` section listed below.\n\n"
            f"{_build_reference_index(ref_files, root_dir)}\n"
        )

        for ref_path in ref_files:
            rel = _relpath(ref_path, root_dir)
            print(f"Adding reference: {rel}...")
            with open(ref_path, "r", encoding="utf-8") as file:
                ref_content = file.read()
            content.append(f"\n\n## REFERENCE FILE: {rel}\n\n{ref_content}")

    # --- Systems ---
    if profile == "micro":
        # Micro: no systems included
        pass
    elif profile == "system" and system:
        # System: include only the specified system
        canonical = _resolve_system(system)
        sys_file = _find_system_file(systems_dir, canonical)
        if sys_file is None:
            print(f"WARNING: System file for '{canonical}' not found in {systems_dir}")
        else:
            rel = _relpath(sys_file, root_dir)
            print(f"Adding system rule: {rel}...")
            with open(sys_file, "r", encoding="utf-8") as file:
                sys_content = file.read()
            content.append(
                "\n\n---\n\n"
                "# SYSTEM MODULE\n\n"
                f"## SYSTEM FILE: {rel}\n\n{sys_content}"
            )
    else:
        # Full: include all systems
        sys_files = []
        if os.path.exists(systems_dir):
            sys_files = sorted(glob.glob(os.path.join(systems_dir, "*.md")))
            sys_files = [path for path in sys_files if Path(path).name.lower() != "readme.md"]

        if sys_files:
            content.append(
                "\n\n---\n\n"
                "# SYSTEM MODULES\n\n"
                "The following sections contain system-specific rules.\n\n"
                "## System Path Map\n\n"
                f"{_build_system_index(sys_files, root_dir)}\n"
            )

            for sys_path in sys_files:
                rel = _relpath(sys_path, root_dir)
                print(f"Adding system rule: {rel}...")
                with open(sys_path, "r", encoding="utf-8") as file:
                    sys_content = file.read()
                content.append(f"\n\n## SYSTEM FILE: {rel}\n\n{sys_content}")

    # --- Write output ---
    final_text = "".join(content)
    print(f"Writing to {output_file}...")
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(final_text)

    # --- Stats ---
    lines = final_text.count("\n") + 1
    size_kb = len(final_text.encode("utf-8")) / 1024
    tokens = _estimate_tokens(final_text)
    print(f"\nDone! '{os.path.basename(output_file)}' ready.")
    print(f"  Lines:  {lines:,}")
    print(f"  Size:   {size_kb:,.1f} KB")
    print(f"  Tokens: ~{tokens:,} (estimated)")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compile rpg-lore-weaver into a manual file for LLM usage",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
profiles:
  full     All references + all systems (default, ~116k tokens)
  system   Core references + ONE system only (~40k tokens)
  micro    SKILL.md + system-prompts.md only (~12k tokens)

examples:
  %(prog)s                                    # full manual
  %(prog)s --profile system --system dnd5e    # D&D 5e only
  %(prog)s --profile system --system t20      # Tormenta 20 only
  %(prog)s --profile micro                    # minimal context
  %(prog)s --profile system --system coc -o coc-manual.md

system aliases:
  dnd, dnd5e, d&d       → D&D 5e
  pf2e, pathfinder      → Pathfinder 2e
  dh, daggerheart       → Daggerheart
  coc, cthulhu          → Call of Cthulhu
  t20, tormenta         → Tormenta 20
  op, ordem             → Ordem Paranormal
""",
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file path (auto-generated if omitted)",
    )
    parser.add_argument(
        "--profile",
        choices=["full", "system", "micro"],
        default="full",
        help="Compilation profile (default: full)",
    )
    parser.add_argument(
        "--system",
        help="System to include (required for 'system' profile). See aliases above.",
    )
    args = parser.parse_args()

    if args.profile == "system" and not args.system:
        parser.error("--system is required when using --profile system")

    compile_skill(
        output_file=args.output,
        profile=args.profile,
        system=args.system,
    )


if __name__ == "__main__":
    main()
