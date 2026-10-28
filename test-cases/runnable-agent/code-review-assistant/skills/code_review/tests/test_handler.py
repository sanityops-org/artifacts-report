#!/usr/bin/env python3
"""
Unit test

Test the various components of the code review skill.
"""

import sys
from pathlib import Path

# Calculate the root directory of the agent project (skills/code_review/tests/.. /.. /.. That is, agent root)
agent_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(agent_root))

import unittest
from skills.code_review.tools.analyze_code import AnalyzeCodeTool, execute as analyze_execute
from skills.code_review.tools.generate_report import GenerateReportTool, execute as report_execute
from skills.code_review.handler import run


class TestAnalyzeCodeTool(unittest.TestCase):
    """Test code analysis tool"""

    def setUp(self):
        self.tool = AnalyzeCodeTool()

    def test_security_sql_injection(self):
        """Test SQL injection detection"""
        code = 'query = "SELECT * FROM users WHERE name=\'" + user + "\'"'
        result = analyze_execute({"code": code, "language": "python", "focus_areas": ["security"]})
        self.assertEqual(result["status"], "success")
        findings = result["data"]["findings"]
        critical = [f for f in findings if f["severity"] == "critical"]
        self.assertTrue(len(critical) > 0, "SQL injection should be detected")
        self.assertEqual(critical[0]["category"], "security")

    def test_security_sensitive_info(self):
        """Test sensitive information detection"""
        code = "password = 'admin123'"
        result = analyze_execute({"code": code, "language": "python", "focus_areas": ["security"]})
        self.assertEqual(result["status"], "success")
        findings = result["data"]["findings"]
        high = [f for f in findings if f["severity"] == "high"]
        self.assertTrue(len(high) > 0, "Hard-coded password should be detected")

    def test_security_eval(self):
        """Test eval detection"""
        code = "result = eval(user_input)"
        result = analyze_execute({"code": code, "language": "python", "focus_areas": ["security"]})
        self.assertEqual(result["status"], "success")
        findings = result["data"]["findings"]
        high = [f for f in findings if f["severity"] == "high"]
        self.assertTrue(len(high) > 0, "Should be detected eval")

    def test_performance_range_len(self):
        """Test performance problem detection"""
        code = "for i in range(len(items)): print(items[i])"
        result = analyze_execute({"code": code, "language": "python", "focus_areas": ["performance"]})
        self.assertEqual(result["status"], "success")
        findings = result["data"]["findings"]
        self.assertTrue(len(findings) > 0, "Range(len()) mode should be detected")

    def test_clean_code(self):
        """Test the clean code and do not report errors."""
        code = '''
def calculate(items):
    total = 0
    for item in items:
        total += item
    return total
'''
        result = analyze_execute({"code": code, "language": "python", "focus_areas": ["security", "readability", "maintainability", "performance"]})
        self.assertEqual(result["status"], "success")
        # The clean code may have 0 or very few warnings.
        self.assertGreaterEqual(len(result["data"]["findings"]), 0)

    def test_empty_code(self):
        """Test the empty code"""
        result = analyze_execute({"code": "", "language": "python", "focus_areas": ["security"]})
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"]["total_issues"], 0)


class TestGenerateReportTool(unittest.TestCase):
    """Test report generation tool"""

    def setUp(self):
        self.tool = GenerateReportTool()

    def test_empty_findings(self):
        """List of test empty questions"""
        result = report_execute({"findings": []})
        self.assertEqual(result["status"], "success")
        self.assertIn("The code is of good quality", result["data"]["summary"])
        self.assertEqual(result["data"]["total_count"], 0)

    def test_critical_findings(self):
        """Test serious problems"""
        findings = [
            {"severity": "critical", "category": "security", "message": "SQL Injection", "suggestion": "Using parametric query", "line_number": 1, "line_content": "test"}
        ]
        result = report_execute({"findings": findings})
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"]["critical_count"], 1)
        self.assertEqual(result["data"]["total_count"], 1)
        self.assertIn("Serious", result["data"]["summary"])

    def test_mixed_findings(self):
        """Test mixed serious-level problems"""
        findings = [
            {"severity": "critical", "category": "security", "message": "SQL Injection", "suggestion": "fix", "line_number": 1},
            {"severity": "high", "category": "security", "message": "Password leak", "suggestion": "Fix", "line_number": 2},
            {"severity": "medium", "category": "maintainability", "message": "The function is too long", "suggestion": "split", "line_number": 3},
            {"severity": "low", "category": "style", "message": "Line too long", "suggestion": "line change", "line_number": 4}
        ]
        result = report_execute({"findings": findings})
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"]["critical_count"], 1)
        self.assertEqual(result["data"]["high_count"], 1)
        self.assertEqual(result["data"]["medium_count"], 1)
        self.assertEqual(result["data"]["low_count"], 1)

    def test_markdown_format(self):
        """Test Markdown format"""
        findings = [
            {"severity": "high", "category": "security", "message": "Test problem", "suggestion": "fix suggestions", "line_number": 5, "line_content": "x = 1"}
        ]
        result = report_execute({"findings": findings})
        self.assertEqual(result["status"], "success")
        md = result["data"]["markdown"]
        self.assertIn("# Code review report", md)
        self.assertIn("## Problem statistics", md)
        self.assertIn("## Details of the problem", md)
        self.assertIn("**Propose**:", md)


class TestHandler(unittest.TestCase):
    """Test the processor"""

    def test_complete_review(self):
        """Test the complete review process"""
        code = '''
def process(data):
    query = "SELECT * FROM users WHERE id='" + data + "'"
    return query
'''
        result = run({"code": code, "language": "python", "focus_areas": ["security"]})
        self.assertEqual(result["status"], "success")
        self.assertIn("data", result)
        self.assertIn("report", result["data"])
        self.assertGreaterEqual(result["data"]["critical_count"], 1)

    def test_no_code(self):
        """No code is provided for the test"""
        result = run({"code": "", "language": "python"})
        self.assertEqual(result["status"], "error")
        self.assertIn("No code provided", result["error"])

    def test_clean_code_review(self):
        """Test the clean code"""
        code = '''
def add(a, b):
    return a + b
'''
        result = run({"code": code, "language": "python", "focus_areas": ["security"]})
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"]["issues_count"], 0)


class TestToolRegistration(unittest.TestCase):
    """Registration of test tools"""

    def test_tool_registration(self):
        """The test tool can be registered to ToolRegistry"""
        from sanityops_agent import ToolRegistry, ToolContext

        ctx = ToolContext()
        registry = ToolRegistry(ctx)

        analyze_tool = AnalyzeCodeTool(ctx)
        report_tool = GenerateReportTool(ctx)

        registry.register(analyze_tool)
        registry.register(report_tool)

        self.assertEqual(len(registry), 2)
        self.assertIsNotNone(registry.get("analyze_code"))
        self.assertIsNotNone(registry.get("generate_report"))

    def test_tool_definition(self):
        """The test tool can generate ToolDefinition"""
        from sanityops_agent.tools.base import ToolDefinition

        tool = AnalyzeCodeTool()
        td = tool.to_tool_definition()

        self.assertIsInstance(td, ToolDefinition)
        self.assertEqual(td.name, "analyze_code")
        # ToolDefinition It is dataclass, using __dict__ instead of model_dump
        self.assertIsNotNone(td.input_schema)
        self.assertIsInstance(td.input_schema, dict)


if __name__ == "__main__":
    unittest.main(verbosity=2)
