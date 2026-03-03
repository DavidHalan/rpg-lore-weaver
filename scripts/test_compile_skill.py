#!/usr/bin/env python3
"""
test_compile_skill.py

Structural tests for compile_skill.py. Validates:
1) Output file is created and non-empty
2) SKILL.md content is present (frontmatter stripped)
3) References are included with correct headers
4) System modules are included with correct headers
5) Path maps are present
6) Profiles (full, system, micro) produce expected structure

Run: python -m unittest scripts/test_compile_skill.py
"""

from __future__ import annotations

import io
import os
import sys
import tempfile
import unittest
from pathlib import Path

# Ensure the scripts directory is on sys.path so we can import compile_skill
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from compile_skill import compile_skill


class TestCompileSkillFull(unittest.TestCase):
    """Test the 'full' profile compilation."""

    @classmethod
    def setUpClass(cls):
        cls.tmpfile = tempfile.NamedTemporaryFile(
            suffix=".md", delete=False, dir=tempfile.gettempdir()
        )
        cls.tmpfile.close()
        _old = sys.stdout
        sys.stdout = io.StringIO()
        compile_skill(output_file=cls.tmpfile.name, profile="full")
        sys.stdout = _old
        cls.content = Path(cls.tmpfile.name).read_text(encoding="utf-8")

    @classmethod
    def tearDownClass(cls):
        os.unlink(cls.tmpfile.name)

    def test_output_is_nonempty(self):
        self.assertGreater(len(self.content), 1000, "Compiled output is too small")

    def test_skill_content_present(self):
        self.assertIn("rpg-lore-weaver", self.content)
        self.assertIn("## Purpose", self.content)

    def test_reference_headers_present(self):
        # Each reference should be wrapped with a REFERENCE FILE header
        # The compile_skill includes references with '## REFERENCE FILE: references/...'
        ref_headers = [l for l in self.content.split("\n") if "REFERENCE FILE:" in l]
        self.assertGreaterEqual(len(ref_headers), 10, f"Only {len(ref_headers)} reference headers")

    def test_reference_path_map_present(self):
        self.assertIn("Reference Path Map", self.content)

    def test_system_path_map_present(self):
        self.assertIn("System Path Map", self.content)

    def test_references_included(self):
        self.assertIn("REFERENCE FILE: references/", self.content)
        # At least 10 reference files should be included
        ref_count = self.content.count("REFERENCE FILE: references/")
        self.assertGreaterEqual(ref_count, 10, f"Only {ref_count} references found")

    def test_systems_included(self):
        self.assertIn("SYSTEM FILE: systems/", self.content)
        # At least 5 system files should be included
        sys_count = self.content.count("SYSTEM FILE: systems/")
        self.assertGreaterEqual(sys_count, 5, f"Only {sys_count} systems found")

    def test_line_count_reasonable(self):
        lines = self.content.count("\n") + 1
        self.assertGreater(lines, 5000, f"Too few lines: {lines}")
        self.assertLess(lines, 20000, f"Too many lines: {lines}")


class TestCompileSkillMicro(unittest.TestCase):
    """Test the 'micro' profile compilation."""

    @classmethod
    def setUpClass(cls):
        cls.tmpfile = tempfile.NamedTemporaryFile(
            suffix=".md", delete=False, dir=tempfile.gettempdir()
        )
        cls.tmpfile.close()
        _old = sys.stdout
        sys.stdout = io.StringIO()
        compile_skill(output_file=cls.tmpfile.name, profile="micro")
        sys.stdout = _old
        cls.content = Path(cls.tmpfile.name).read_text(encoding="utf-8")

    @classmethod
    def tearDownClass(cls):
        os.unlink(cls.tmpfile.name)

    def test_micro_is_smaller_than_full(self):
        self.assertLess(
            len(self.content), 50000, "Micro profile should be much smaller"
        )

    def test_micro_has_system_prompts(self):
        self.assertIn("system-prompts", self.content)

    def test_micro_has_no_system_modules(self):
        self.assertNotIn("SYSTEM FILE:", self.content)


class TestCompileSkillSystem(unittest.TestCase):
    """Test the 'system' profile compilation."""

    @classmethod
    def setUpClass(cls):
        cls.tmpfile = tempfile.NamedTemporaryFile(
            suffix=".md", delete=False, dir=tempfile.gettempdir()
        )
        cls.tmpfile.close()
        _old = sys.stdout
        sys.stdout = io.StringIO()
        compile_skill(output_file=cls.tmpfile.name, profile="system", system="dnd5e")
        sys.stdout = _old
        cls.content = Path(cls.tmpfile.name).read_text(encoding="utf-8")

    @classmethod
    def tearDownClass(cls):
        os.unlink(cls.tmpfile.name)

    def test_system_includes_specified_system(self):
        self.assertIn("dnd5e-rules", self.content)

    def test_system_excludes_other_systems(self):
        # System profile should not include SYSTEM FILE sections for other systems
        self.assertNotIn("SYSTEM FILE: systems/tormenta20-rules", self.content)

    def test_system_includes_core_references(self):
        self.assertIn("REFERENCE FILE:", self.content)


if __name__ == "__main__":
    unittest.main()
