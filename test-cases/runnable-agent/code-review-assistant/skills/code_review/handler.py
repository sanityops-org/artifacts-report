#!/usr/bin/env python3
"""
Code review skill processing script

The script implements the core logic of code review and runs using the sanityops_agent framework.
"""

import sys
import asyncio
from pathlib import Path
from typing import Dict, Any, List

from sanityops_agent import Tool, ToolContext, ToolResult

# Handle the module import at direct runtime
if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))

# Import tools
from skills.code_review.tools.analyze_code import AnalyzeCodeTool
from skills.code_review.tools.generate_report import GenerateReportTool


class CodeReviewHandler:
    """Code review skill processor"""

    def __init__(self):
        self.analyze_tool = AnalyzeCodeTool()
        self.report_tool = GenerateReportTool()

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execution code review

        Args:
            params: Parameter dictionary containing code, language, focus_areas

        Returns:
            Dictionary of examination results
        """
        code = params.get("code", "")
        language = params.get("language", "python")
        focus_areas = params.get("focus_areas", ["security", "readability", "maintainability"])

        if not code:
            return {
                "status": "error",
                "error": "No code provided",
                "message": "Please provide the code to be reviewed."
            }

        # Step 1: Analyze the code
        analysis_result = await self.analyze_tool.execute(
            code=code,
            language=language,
            focus_areas=focus_areas
        )

        if not analysis_result.success:
            return {
                "status": "error",
                "error": "Code analysis failed",
                "details": analysis_result.error or "Unknown error"
            }

        findings = analysis_result.metadata.get("findings", [])

        # Step 2: Generate a report
        report_result = await self.report_tool.execute(
            findings=findings,
            include_examples=True
        )

        if not report_result.success:
            return {
                "status": "error",
                "error": "Failed to generate the report",
                "details": report_result.error or "Unknown error"
            }

        report = report_result.metadata

        return {
            "status": "success",
            "data": {
                "summary": report.get("summary", ""),
                "issues_count": len(findings),
                "critical_count": report.get("critical_count", 0),
                "high_count": report.get("high_count", 0),
                "medium_count": report.get("medium_count", 0),
                "low_count": report.get("low_count", 0),
                "report": report.get("markdown", ""),
                "findings": findings
            },
            "message": f"The code review has been completed, and a total of {len(findings)} problems were found."
        }


# Create a global processor instance
_handler = CodeReviewHandler()


async def main(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Skill main entrance (asynchronous)

    Args:
        params: Input parameter dictionary

    Returns:
        Execution result dictionary
    """
    return await _handler.execute(params)


def run(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Synchronized entrance function

    Args:
        params: Input parameter dictionary

    Returns:
        Execution result dictionary
    """
    return asyncio.run(main(params))


if __name__ == "__main__":
    """Local test"""
    import json

    test_code = '''
def process_user_data(user_input):
    query = "SELECT * FROM users WHERE name = '" + user_input + "'"
    return query

def calculate_sum(numbers):
    total = 0
    for i in range(len(numbers)):
        total = total + numbers[i]
    return total
'''

    result = run({
        "code": test_code,
        "language": "python",
        "focus_areas": ["security", "readability", "maintainability", "performance"]
    })

    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("\n" + "=" * 60)
    print("Markdown Report:")
    print("=" * 60)
    if result.get("status") == "success":
        print(result["data"]["report"])
