#!/usr/bin/env python3
"""
Continuous quality gate for rpg-lore-weaver.

Runs core checks required before considering the repository healthy.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path
import re


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
EXAMPLES_DIR = ROOT_DIR / "examples"
REFERENCES_DIR = ROOT_DIR / "references"
SKILL_FILE = ROOT_DIR / "SKILL.md"
MAX_SKILL_LINES = 500


def _run(cmd: list[str], suppress_output: bool = False, cwd: Path | None = None) -> None:
    printable = " ".join(cmd)
    print(f"\n[quality-gate] RUN  {printable}")
    kwargs: dict[str, object] = {}
    if suppress_output:
        kwargs.update(
            {
                "capture_output": True,
                "text": True,
                "encoding": "utf-8",
                "errors": "replace",
            }
        )
    completed = subprocess.run(cmd, cwd=cwd or ROOT_DIR, **kwargs)
    if completed.returncode != 0:
        print(f"[quality-gate] FAIL {printable}")
        if suppress_output:
            if completed.stdout:
                print("\n[quality-gate] stdout:")
                print(completed.stdout)
            if completed.stderr:
                print("\n[quality-gate] stderr:")
                print(completed.stderr)
        sys.exit(completed.returncode)
    print(f"[quality-gate] OK   {printable}")


def _assert_skill_line_count() -> None:
    """Enforce the 500-line rule for SKILL.md."""
    if not SKILL_FILE.exists():
        print("[quality-gate] WARN SKILL.md not found")
        return
    line_count = len(SKILL_FILE.read_text(encoding="utf-8").splitlines())
    if line_count > MAX_SKILL_LINES:
        print(
            f"\n[quality-gate] FAIL SKILL.md has {line_count} lines "
            f"(max {MAX_SKILL_LINES})"
        )
        sys.exit(1)
    print(
        f"[quality-gate] OK   SKILL.md line count: {line_count}/{MAX_SKILL_LINES}"
    )


def _validate_examples() -> None:
    examples = sorted(EXAMPLES_DIR.glob("*.md"))
    if not examples:
        print("[quality-gate] WARN no example files found")
        return
    temp_export = Path(tempfile.gettempdir()) / "rpg-lore-weaver-quality-gate-export.json"
    for example in examples:
        _run(
            [
                sys.executable,
                "scripts/validate_character_output.py",
                str(example.relative_to(ROOT_DIR)),
            ],
            suppress_output=True,
        )
        _run(
            [
                sys.executable,
                "scripts/export_character.py",
                str(example.relative_to(ROOT_DIR)),
                "--format",
                "json",
                "-o",
                str(temp_export),
            ],
            suppress_output=True,
        )
    try:
        temp_export.unlink(missing_ok=True)
    except OSError:
        pass


def _validate_reference_frontmatter() -> None:
    """Check that all .md files in references/ have proper frontmatter."""
    refs = sorted(REFERENCES_DIR.glob("*.md"))
    if not refs:
        print("[quality-gate] WARN no reference files found")
        return
    failures = []
    for ref in refs:
        content = ref.read_text(encoding="utf-8-sig")
        if not content.startswith("---"):
            failures.append(f"{ref.name}: missing frontmatter")
            continue
        if "description:" not in content.split("---", 2)[1]:
            failures.append(f"{ref.name}: missing description")
        if "tags:" not in content.split("---", 2)[1]:
            failures.append(f"{ref.name}: missing metadata.tags")
    if failures:
        for f in failures:
            print(f"[quality-gate] FAIL frontmatter: {f}")
        sys.exit(1)
    print(f"[quality-gate] OK   frontmatter valid in {len(refs)} references")


def main() -> None:
    # Unit tests
    _run([sys.executable, "-m", "unittest", "test_lib_utils"], cwd=SCRIPT_DIR)
    _run([sys.executable, "-m", "unittest", "scripts/test_character_tools.py"])
    _run([sys.executable, "-m", "unittest", "scripts/test_compile_skill.py"], suppress_output=True)

    # Structural checks
    _assert_skill_line_count()

    # Compile manual
    _run([sys.executable, "scripts/compile_skill.py"])

    # Validate all examples (validate + export)
    _validate_examples()

    # Frontmatter hygiene
    _validate_reference_frontmatter()

    print("\n[quality-gate] PASS all checks")


if __name__ == "__main__":
    main()
