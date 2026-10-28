#!/usr/bin/env python3
"""Test the simulated data layer"""

import sys
from pathlib import Path

# Add the agent project root directory to path
# test_sim_db.py Located under data/tests/, up to level 3, that is, government hotline intelligent customer service/
agent_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(agent_root))

import unittest


class TestSimDB(unittest.TestCase):
    """Test the simulated database structure"""

    def test_departments_exist(self):
        """The data of the test department exists"""
        from data.sim_db import DEPARTMENTS
        self.assertIsInstance(DEPARTMENTS, dict)
        self.assertGreater(len(DEPARTMENTS), 0)
        # Verify the required fields
        for dept_id, dept in DEPARTMENTS.items():
            self.assertIn("name", dept)
            self.assertIn("description", dept)

    def test_keyword_mapping_exist(self):
        """Test the existence of keyword mapping"""
        from data.sim_db import KEYWORD_DEPT_MAPPING
        self.assertIsInstance(KEYWORD_DEPT_MAPPING, dict)
        self.assertGreater(len(KEYWORD_DEPT_MAPPING), 0)

    def test_urgency_keywords_exist(self):
        """Test the existence of urgent keywords"""
        from data.sim_db import URGENCY_KEYWORDS
        self.assertIsInstance(URGENCY_KEYWORDS, dict)
        self.assertIn("critical", URGENCY_KEYWORDS)
        self.assertIn("urgent", URGENCY_KEYWORDS)
        self.assertIn("normal", URGENCY_KEYWORDS)

    def test_departments_have_default_dept(self):
        """There is a default bottom department for testing."""
        from data.sim_db import DEPARTMENTS
        # There should be a "Comprehensive Coordination Office" as a cover.
        self.assertIn("default", DEPARTMENTS)


if __name__ == "__main__":
    unittest.main(verbosity=2)
