#!/usr/bin/env python3
"""
Unit test

Test the components of the airworthiness decision-making assistant for aircraft maintenance.
"""

import sys
from pathlib import Path

# Calculate the root directory of the agent project
agent_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(agent_root))

import unittest
import asyncio

# Data layer test
class TestHelpers(unittest.TestCase):
    """Test auxiliary functions"""

    def test_calc_remaining_life_life_limited(self):
        """Calculation of the remaining life of test life parts"""
        from data.helpers import calc_remaining_life

        component = {
            "category": "life_limited",
            "total_life_hours": 12000,
            "total_life_cycles": 8000,
        }
        result = calc_remaining_life(component, 2000, 1000)

        self.assertEqual(result["remaining_hours"], 10000)
        self.assertEqual(result["remaining_cycles"], 7000)
        self.assertEqual(result["alert_level"], "ok")

    def test_calc_remaining_life_warning(self):
        """Test the warning level of life parts"""
        from data.helpers import calc_remaining_life

        component = {
            "category": "life_limited",
            "total_life_hours": 10000,
            "total_life_cycles": 5000,
        }
        # 85% has been used, and the remaining 15% (below the 20% threshold)
        result = calc_remaining_life(component, 8500, 4250)

        self.assertEqual(result["remaining_hours"], 1500)
        self.assertEqual(result["alert_level"], "warning")

    def test_calc_remaining_life_critical(self):
        """The critical level of the test life part"""
        from data.helpers import calc_remaining_life

        component = {
            "category": "life_limited",
            "total_life_hours": 10000,
            "total_life_cycles": 5000,
        }
        # 95% has been used, and the rest 5%
        result = calc_remaining_life(component, 9500, 4750)

        self.assertEqual(result["alert_level"], "critical")

    def test_calc_remaining_life_exceeded(self):
        """The test life piece exceeds the limit"""
        from data.helpers import calc_remaining_life

        component = {
            "category": "life_limited",
            "total_life_hours": 10000,
            "total_life_cycles": 5000,
        }
        # Exceed the limit
        result = calc_remaining_life(component, 10500, 5200)

        self.assertEqual(result["alert_level"], "exceeded")

    def test_check_time_control_limit_ok(self):
        """The control is in the normal state during the test."""
        from data.helpers import check_time_control_limit

        tci = {
            "limit_type": "hours",
            "limit_value": 3000,
            "alert_threshold": 0.8,
        }
        result = check_time_control_limit(tci, 2000)

        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["remaining"], 1000)

    def test_check_time_control_limit_warning(self):
        """Control warning during testing"""
        from data.helpers import check_time_control_limit

        tci = {
            "limit_type": "hours",
            "limit_value": 3000,
            "alert_threshold": 0.8,
        }
        result = check_time_control_limit(tci, 2600)

        self.assertEqual(result["status"], "warning")

    def test_check_time_control_limit_exceeded(self):
        """The control exceeds the limit during the test."""
        from data.helpers import check_time_control_limit

        tci = {
            "limit_type": "hours",
            "limit_value": 3000,
            "alert_threshold": 0.8,
        }
        result = check_time_control_limit(tci, 3100)

        self.assertEqual(result["status"], "exceeded")

    def test_evaluate_ad_compliance_complied(self):
        """Test AD has been executed"""
        from data.helpers import evaluate_ad_compliance

        ad = {
            "status": "open",
            "compliance": "mandatory",
        }
        compliance_record = {"status": "complied", "date": "2024-04-15"}

        result = evaluate_ad_compliance(ad, compliance_record)

        self.assertEqual(result["status"], "complied")
        self.assertEqual(result["action_required"], False)

    def test_evaluate_ad_compliance_open(self):
        """Test AD not executed"""
        from data.helpers import evaluate_ad_compliance

        ad = {
            "status": "open",
            "compliance": "mandatory",
            "effective_date": "2024-03-01",
        }
        compliance_record = None

        result = evaluate_ad_compliance(ad, compliance_record)

        self.assertEqual(result["status"], "open")
        self.assertEqual(result["action_required"], True)

    def test_evaluate_ad_compliance_superseded(self):
        """Test AD is replaced"""
        from data.helpers import evaluate_ad_compliance

        ad = {
            "status": "superseded",
            "superseded_by": "AD-2024-02-001",
        }
        compliance_record = None

        result = evaluate_ad_compliance(ad, compliance_record)

        self.assertEqual(result["status"], "superseded")

    def test_assess_defect_impact_minor(self):
        """Test for minor defects"""
        from data.helpers import assess_defect_impact

        defect = {
            "severity": "low",
            "mel_reference": None,
        }
        result = assess_defect_impact(defect)

        self.assertEqual(result["airworthy"], True)
        self.assertEqual(result["requires_action"], False)

    def test_assess_defect_impact_mel(self):
        """Test MEL control defects"""
        from data.helpers import assess_defect_impact

        defect = {
            "severity": "medium",
            "mel_reference": "MEL-79-01",
            "mel_deadline": "2026-09-10",
        }
        result = assess_defect_impact(defect)

        self.assertEqual(result["airworthy"], True)
        self.assertEqual(result["mel_controlled"], True)

    def test_assess_defect_impact_grounding(self):
        """Test the stoppage defect"""
        from data.helpers import assess_defect_impact

        defect = {
            "severity": "critical",
            "mel_reference": None,
        }
        result = assess_defect_impact(defect)

        self.assertEqual(result["airworthy"], False)
        self.assertEqual(result["requires_action"], True)


class TestQueryAirworthinessTool(unittest.TestCase):
    """Test airworthiness status query tool"""

    def setUp(self):
        from skills.airworthiness_advisor.tools.query_airworthiness import QueryAirworthinessTool
        self.tool = QueryAirworthinessTool()

    def test_query_ad_complied(self):
        """The test has performed AD query."""
        import asyncio
        result = asyncio.run(self.tool.execute(reg_no="B-1234", ad_id="AD-2024-01-001"))

        self.assertTrue(result.success)
        self.assertEqual(result.metadata["status"], "complied")

    def test_query_ad_open(self):
        """The test did not perform AD query."""
        import asyncio
        result = asyncio.run(self.tool.execute(reg_no="B-1234", ad_id="AD-2024-02-001"))

        self.assertTrue(result.success)
        self.assertEqual(result.metadata["status"], "open")
        self.assertTrue(result.metadata["action_required"])

    def test_query_ad_superseded(self):
        """The test has replaced the AD query."""
        import asyncio
        result = asyncio.run(self.tool.execute(reg_no="B-1234", ad_id="AD-2023-05-001"))

        self.assertTrue(result.success)
        self.assertEqual(result.metadata["status"], "superseded")

    def test_query_unknown_ad(self):
        """Test unknown AD"""
        import asyncio
        result = asyncio.run(self.tool.execute(reg_no="B-1234", ad_id="AD-9999-99-999"))

        self.assertFalse(result.success)
        self.assertIn("does not exist", result.error)

    def test_query_unknown_aircraft(self):
        """Test unknown aircraft"""
        import asyncio
        result = asyncio.run(self.tool.execute(reg_no="B-9999", ad_id="AD-2024-01-001"))

        self.assertFalse(result.success)
        self.assertIn("does not exist", result.error)

    def test_query_all_ads(self):
        """Test query all AD"""
        import asyncio
        result = asyncio.run(self.tool.execute(reg_no="B-1234"))

        self.assertTrue(result.success)
        self.assertIn("ad_list", result.metadata)


class TestQueryComponentStatusTool(unittest.TestCase):
    """Test parts status query tool"""

    def setUp(self):
        from skills.airworthiness_advisor.tools.query_component_status import QueryComponentStatusTool
        self.tool = QueryComponentStatusTool()

    def test_query_life_limited_component(self):
        """Test life parts inquiry"""
        import asyncio
        result = asyncio.run(self.tool.execute(reg_no="B-1234", part_no="PN-12345"))

        self.assertTrue(result.success)
        self.assertEqual(result.metadata["category"], "life_limited")
        self.assertIn("remaining_hours", result.metadata)
        self.assertIn("alert_level", result.metadata)

    def test_query_time_controlled_component(self):
        """Control query during testing"""
        import asyncio
        result = asyncio.run(self.tool.execute(reg_no="B-1234", part_no="PN-67890"))

        self.assertTrue(result.success)
        self.assertEqual(result.metadata["category"], "time_controlled")
        self.assertIn("tci_status", result.metadata)

    def test_query_unknown_part(self):
        """Test unknown parts"""
        import asyncio
        result = asyncio.run(self.tool.execute(reg_no="B-1234", part_no="PN-99999"))

        self.assertFalse(result.success)
        self.assertIn("does not exist", result.error)

    def test_query_not_installed(self):
        """Test uninstalled parts"""
        import asyncio
        result = asyncio.run(self.tool.execute(reg_no="B-5678", part_no="PN-11111"))

        self.assertFalse(result.success)
        self.assertIn("not installed", result.error)


class TestQueryMaintenanceHistoryTool(unittest.TestCase):
    """Test history query tool"""

    def setUp(self):
        from skills.airworthiness_advisor.tools.query_maintenance_history import QueryMaintenanceHistoryTool
        self.tool = QueryMaintenanceHistoryTool()

    def test_query_aircraft_history(self):
        """Test aircraft resume inquiry"""
        import asyncio
        result = asyncio.run(self.tool.execute(reg_no="B-1234"))

        self.assertTrue(result.success)
        self.assertEqual(result.metadata["model"], "A320")
        self.assertIn("total_hours", result.metadata)
        self.assertIn("open_defects", result.metadata)

    def test_query_with_component(self):
        """Test the history inquiry with parts"""
        import asyncio
        result = asyncio.run(self.tool.execute(reg_no="B-1234", part_no="PN-12345"))

        self.assertTrue(result.success)
        self.assertIn("component_history", result.metadata)

    def test_query_open_defects(self):
        """Test residual defect query"""
        import asyncio
        result = asyncio.run(self.tool.execute(reg_no="B-1234"))

        self.assertTrue(result.success)
        defects = result.metadata["open_defects"]
        self.assertTrue(len(defects) > 0)
        # Check the impact assessment of defects
        self.assertIn("impact", defects[0])

    def test_query_unknown_aircraft(self):
        """Test unknown aircraft"""
        import asyncio
        result = asyncio.run(self.tool.execute(reg_no="B-9999"))

        self.assertFalse(result.success)


class TestGenerateDecisionTool(unittest.TestCase):
    """Test maintenance decision generation tool"""

    def setUp(self):
        from skills.airworthiness_advisor.tools.generate_decision import GenerateDecisionTool
        self.tool = GenerateDecisionTool()

    def test_generate_decision_airworthy(self):
        """Testing can release decision-making"""
        import asyncio

        assessment_data = {
            "ad_status": {"status": "complied"},
            "component_status": {"alert_level": "ok"},
            "defects": [],
        }
        result = asyncio.run(self.tool.execute(reg_no="B-5678", assessment_data=assessment_data))

        self.assertTrue(result.success)
        self.assertEqual(result.metadata["assessment"], "airworthy")
        self.assertEqual(len(result.metadata["open_actions"]), 0)

    def test_generate_decision_grounding(self):
        """Test the decision of stopping the field"""
        import asyncio

        assessment_data = {
            "ad_status": {"status": "open", "action_required": True},
            "component_status": {"alert_level": "exceeded"},
            "defects": [{"severity": "critical", "impact": "grounding"}],
        }
        result = asyncio.run(self.tool.execute(reg_no="B-1234", assessment_data=assessment_data))

        self.assertTrue(result.success)
        self.assertEqual(result.metadata["assessment"], "grounding")
        self.assertTrue(len(result.metadata["open_actions"]) > 0)

    def test_generate_decision_mel_controlled(self):
        """Test MEL control decision-making"""
        import asyncio

        assessment_data = {
            "ad_status": {"status": "complied"},
            "component_status": {"alert_level": "ok"},
            "defects": [
                {"severity": "medium", "impact": "mel", "mel_reference": "MEL-79-01", "mel_deadline": "2026-09-10"}
            ],
        }
        result = asyncio.run(self.tool.execute(reg_no="B-1234", assessment_data=assessment_data))

        self.assertTrue(result.success)
        self.assertEqual(result.metadata["assessment"], "restricted")
        self.assertTrue(len(result.metadata["deferred_items"]) > 0)


class TestHandler(unittest.TestCase):
    """Test processor arrangement"""

    def test_execute_handler_full_flow(self):
        """Test the complete decision-making process"""
        from skills.airworthiness_advisor.handler import run

        result = run({"reg_no": "B-1234", "part_no": "PN-12345"})

        self.assertEqual(result["status"], "success")
        self.assertIn("assessment", result["data"])
        self.assertIn("open_actions", result["data"])
        self.assertIn("rationale", result["data"])

    def test_handler_unknown_aircraft(self):
        """Test unknown aircraft"""
        from skills.airworthiness_advisor.handler import run

        result = run({"reg_no": "B-9999", "part_no": "PN-12345"})

        self.assertEqual(result["status"], "error")

    def test_handler_airworthy_case(self):
        """Test releaseable cases"""
        from skills.airworthiness_advisor.handler import run

        result = run({"reg_no": "B-5678", "part_no": "PN-12345"})

        self.assertEqual(result["status"], "success")
        # B-5678 The parts are relatively new, and it should be able to be released.
        self.assertIn(result["data"]["assessment"], ["airworthy", "restricted"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
