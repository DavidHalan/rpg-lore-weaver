#!/usr/bin/env python3
"""
Unit tests for scripts/lib_utils.py
"""

import unittest
from pathlib import Path
import lib_utils

class TestLibUtils(unittest.TestCase):

    def test_parse_frontmatter_tags_new_format(self):
        fm = """---
name: test
metadata:
  triggers:
    - trigger1
    - trigger2
---"""
        tags = lib_utils.parse_frontmatter_tags(fm)
        self.assertEqual(tags, ["trigger1", "trigger2"])

    def test_parse_frontmatter_tags_old_format(self):
        fm = """---
tags: [tag1, tag2]
---"""
        tags = lib_utils.parse_frontmatter_tags(fm)
        self.assertEqual(tags, ["tag1", "tag2"])

    def test_parse_frontmatter_tags_mixed(self):
        fm = """---
tags: [old1]
metadata:
  triggers:
    - new1
---"""
        tags = lib_utils.parse_frontmatter_tags(fm)
        # Should contain both, order might vary depending on implementation detail but 
        # distinct list is expected.
        self.assertIn("old1", tags)
        self.assertIn("new1", tags)

    def test_parse_frontmatter_description(self):
        fm = 'description: "A test description."'
        self.assertEqual(lib_utils.parse_frontmatter_description(fm), "A test description.")
        
        fm2 = "description: Simple description"
        self.assertEqual(lib_utils.parse_frontmatter_description(fm2), "Simple description")

    def test_mojibake_score(self):
        clean = "This is clean text."
        dirty = "This is â€” definitely â€“ dirty."
        self.assertEqual(lib_utils.mojibake_score(clean), 0)
        self.assertGreater(lib_utils.mojibake_score(dirty), 0)

    def test_sanitize_filename_title(self):
        p = Path("001_some_file.md")
        self.assertEqual(lib_utils.sanitize_filename_title(p), "Some File")
        
        p2 = Path("just-a-name.md")
        self.assertEqual(lib_utils.sanitize_filename_title(p2), "Just A Name")

if __name__ == '__main__':
    unittest.main()
