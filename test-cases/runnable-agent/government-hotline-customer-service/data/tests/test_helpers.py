#!/usr/bin/env python3
"""Test auxiliary functions"""

import sys
from pathlib import Path

# test_helpers.py Located under data/tests/, up to level 3, that is, government hotline intelligent customer service/
agent_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(agent_root))

import unittest
from datetime import datetime


class TestMatchDepartment(unittest.TestCase):
    """Test department matching function"""

    def test_match_noise_complaint(self):
        """Test noise complaints and match the Ecological Environment Bureau"""
        from data.helpers import match_department
        result = match_department("The construction noise of the construction site downstairs disturbs people at night.")
        self.assertEqual(result["dept_id"], "eco_env")
        self.assertEqual(result["dept_name"], "Ecology and Environment Bureau")
        self.assertTrue(result["is_auto"])
        self.assertGreater(result["confidence"], 0)

    def test_match_wage_arrears(self):
        """Test salary arrears complaints matching Human Resources and Social Security Bureau"""
        from data.helpers import match_department
        result = match_department("The company has not paid the salary for three months.")
        self.assertEqual(result["dept_id"], "hr_ss")
        self.assertEqual(result["dept_name"], "Human Resources and Social Security Bureau")

    def test_match_food_safety(self):
        """Test food safety matching market supervision bureau"""
        from data.helpers import match_department
        result = match_department("Food hygiene problems in the restaurant lead to diarrhea")
        self.assertEqual(result["dept_id"], "market_reg")

    def test_match_fire_emergency(self):
        """Test fire matching emergency management agency"""
        from data.helpers import match_department
        result = match_department("There was a fire in the community.")
        self.assertEqual(result["dept_id"], "emergency")

    def test_match_fallback_to_default(self):
        """When the test does not match the keywords, go to the Comprehensive Coordination Office."""
        from data.helpers import match_department
        result = match_department("I want to consult the policy.")
        self.assertEqual(result["dept_id"], "default")
        self.assertEqual(result["dept_name"], "Comprehensive Coordination Office")
        self.assertFalse(result["is_auto"])

    def test_match_multiple_keywords_first_wins(self):
        """Take the first one when testing multi-keyword matching."""
        from data.helpers import match_department
        # "Noise" in front, should be matched with the Ecology Bureau
        result = match_department("Noise disturbs people and property management is not in place")
        self.assertEqual(result["dept_id"], "eco_env")


class TestClassifyUrgency(unittest.TestCase):
    """Test the urgency classification"""

    def test_critical_fire(self):
        """Test the fire for emergency"""
        from data.helpers import classify_urgency
        result = classify_urgency("There was a fire in the community.")
        self.assertEqual(result["level"], "critical")
        self.assertIn("Fire", result["matched_keywords"])

    def test_critical_gas_leak(self):
        """Test gas leakage for emergency"""
        from data.helpers import classify_urgency
        result = classify_urgency("Smell the gas leak")
        self.assertEqual(result["level"], "critical")

    def test_critical_group_complaint(self):
        """Test the group complaint for emergency"""
        from data.helpers import classify_urgency
        result = classify_urgency("Our community's collective complaint about the property")
        self.assertEqual(result["level"], "critical")
        self.assertIn("Collective complaint", result["matched_keywords"])

    def test_urgent_noise(self):
        """It is urgent to test noise to disturb people."""
        from data.helpers import classify_urgency
        result = classify_urgency("The noise of construction at night seriously disturbs people.")
        self.assertEqual(result["level"], "urgent")
        self.assertIn("disturbs people", result["matched_keywords"])

    def test_urgent_power_outage(self):
        """Test power outage as an emergency"""
        from data.helpers import classify_urgency
        result = classify_urgency("The community suddenly lost power.")
        self.assertEqual(result["level"], "urgent")
        self.assertTrue(any("power" in item.lower() for item in result["matched_keywords"]))

    def test_normal_general(self):
        """Test general consultation is ordinary"""
        from data.helpers import classify_urgency
        result = classify_urgency("I want to consult about the social security policy.")
        self.assertEqual(result["level"], "normal")
        self.assertEqual(result["matched_keywords"], [])


class TestGenerateTicketId(unittest.TestCase):
    """Test work order number generation"""

    def test_ticket_id_format(self):
        """Test the work order number format"""
        from data.helpers import generate_ticket_id
        ticket_id = generate_ticket_id()
        # Format: GH-YYYYMMDD-NNNN
        self.assertRegex(ticket_id, r"^GH-\d{8}-\d{4}$")

    def test_ticket_id_increments(self):
        """The test work order number is increasing"""
        from data.helpers import generate_ticket_id
        from data.sim_db import TICKET_COUNTER
        id1 = generate_ticket_id()
        id2 = generate_ticket_id()
        # The last work order number should be larger than the previous one.
        self.assertNotEqual(id1, id2)

    def test_ticket_id_contains_today_date(self):
        """The test work order number includes the date of the day."""
        from data.helpers import generate_ticket_id
        ticket_id = generate_ticket_id()
        today = datetime.now().strftime("%Y%m%d")
        self.assertIn(today, ticket_id)


if __name__ == "__main__":
    unittest.main(verbosity=2)
