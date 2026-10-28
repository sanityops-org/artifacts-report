#!/usr/bin/env python3
"""
Report generation tool

Generate a structured code review report based on the results of code analysis.
Inherit the sanityops_agent.Tool base class implementation.
"""

from typing import Any, Dict, List

from sanityops_agent import Tool, ToolContext, ToolResult


class GenerateReportTool(Tool):
    """Report generation tool"""

    name = "generate_report"
    description = "Generate a structured code review report based on the results of code analysis"
    parameters = {
        "type": "object",
        "properties": {
            "findings": {
                "type": "array",
                "description": "Review the list of problems found",
                "items": {
                    "type": "object",
                    "properties": {
                        "severity": {"type": "string"},
                        "category": {"type": "string"},
                        "message": {"type": "string"},
                        "suggestion": {"type": "string"},
                        "line_number": {"type": "integer"},
                        "line_content": {"type": "string"}
                    }
                }
            },
            "include_examples": {
                "type": "boolean",
                "description": "Does it contain sample code?",
                "default": True
            }
        },
        "required": ["findings"]
    }
    tags = ["report", "documentation"]

    def __init__(self, context: ToolContext | None = None):
        super().__init__(context)

    async def execute(self, **kwargs) -> ToolResult:
        """
        Execution report generation

        Args:
            findings: Review the list of problems found
            include_examples: Does it contain sample code?

        Returns:
            ToolResult Contains the generated report
        """
        findings = kwargs.get("findings", [])
        include_examples = kwargs.get("include_examples", True)

        try:
            # The number of statistical questions
            critical_count = sum(1 for f in findings if f.get("severity") == "critical")
            high_count = sum(1 for f in findings if f.get("severity") == "high")
            medium_count = sum(1 for f in findings if f.get("severity") == "medium")
            low_count = sum(1 for f in findings if f.get("severity") == "low")

            # Generate an overall evaluation
            summary = self._generate_summary(findings, critical_count, high_count, medium_count, low_count)

            # Generate a Markdown report
            markdown = self._generate_markdown_report(
                findings, summary,
                critical_count, high_count, medium_count, low_count,
                include_examples
            )

            result_data = {
                "summary": summary,
                "markdown": markdown,
                "critical_count": critical_count,
                "high_count": high_count,
                "medium_count": medium_count,
                "low_count": low_count,
                "total_count": len(findings)
            }

            return ToolResult(
                content=summary,
                success=True,
                metadata=result_data
            )

        except Exception as e:
            import traceback
            return ToolResult(
                content=f"Error in the generation of the report: {str(e)}",
                success=False,
                error=str(e),
                metadata={"traceback": traceback.format_exc()}
            )

    def _generate_summary(self, findings: List[Dict], critical: int, high: int, medium: int, low: int) -> str:
        """Generate an overall evaluation"""
        total = len(findings)

        if total == 0:
            return "The code is of good quality, and no obvious problems were found."

        if critical > 0:
            return f"Serious problems were found: {total} total, including {critical} critical problems that require immediate repair."

        if high > 0:
            return f"{total} problems were found, of which {high} high-risk problems need to be prioritized."

        if medium > 0:
            return f"{total} problems were found, and it is recommended to improve them step by step."

        return f"{total} minor problems were found, which do not affect the function but it is recommended to optimize."

    def _generate_markdown_report(
        self,
        findings: List[Dict],
        summary: str,
        critical: int,
        high: int,
        medium: int,
        low: int,
        include_examples: bool
    ) -> str:
        """Generate Markdown format report"""
        lines = []

        # Heading
        lines.append("# Code review report")
        lines.append("")

        # Overall evaluation
        lines.append("## Overall evaluation")
        lines.append(summary)
        lines.append("")

        # Problem statistics
        lines.append("## Problem statistics")
        lines.append("")
        lines.append(f"- 🔴 Critical: {critical}")
        lines.append(f"- 🟠 High: {high}")
        lines.append(f"- 🟡 Medium: {medium}")
        lines.append(f"- 🟢 Low: {low}")
        lines.append(f"- **Amount to**: {len(findings)}")
        lines.append("")

        # List of problems grouped by severity
        if findings:
            lines.append("## Details of the problem")
            lines.append("")

            if critical > 0:
                lines.append("### 🔴 Critical")
                lines.append("")
                for finding in [f for f in findings if f.get("severity") == "critical"]:
                    lines.extend(self._format_finding(finding, include_examples))
                lines.append("")

            if high > 0:
                lines.append("### 🟠 High")
                lines.append("")
                for finding in [f for f in findings if f.get("severity") == "high"]:
                    lines.extend(self._format_finding(finding, include_examples))
                lines.append("")

            if medium > 0:
                lines.append("### 🟡 Medium")
                lines.append("")
                for finding in [f for f in findings if f.get("severity") == "medium"]:
                    lines.extend(self._format_finding(finding, include_examples))
                lines.append("")

            if low > 0:
                lines.append("### 🟢 Low")
                lines.append("")
                for finding in [f for f in findings if f.get("severity") == "low"]:
                    lines.extend(self._format_finding(finding, include_examples))
                lines.append("")

        # Positive feedback
        lines.append("## Positive feedback")
        lines.append("")
        lines.append("✓ The code structure is clear and the degree of modularity is good.")
        lines.append("✓ The function responsibilities are clear and in line with the principle of single responsibility.")
        lines.append("")

        return "\n".join(lines)

    def _format_finding(self, finding: Dict, include_examples: bool) -> List[str]:
        """Format a single question"""
        lines = []

        category = finding.get("category", "unknown")
        message = finding.get("message", "")
        suggestion = finding.get("suggestion", "")
        line_number = finding.get("line_number", 0)
        line_content = finding.get("line_content", "")

        # Title of the question
        lines.append(f"**[{category.upper()}] {message}**")
        lines.append("")

        # Location information
        if line_number > 0:
            lines.append(f"- **Location**: Line {line_number}")

        # Code snippet
        if line_content:
            lines.append(f"- **Code**: `{line_content}`")

        # Propose
        if suggestion:
            lines.append(f"- **Propose**: {suggestion}")

        lines.append("")
        return lines


# Maintain backward compatible function interface
def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Synchronous execution entrance (backward compatibility)

    Args:
        params: Tool parameters

    Returns:
        Execution result dictionary
    """
    import asyncio
    tool = GenerateReportTool()
    result = asyncio.run(tool.execute(**params))
    return {
        "status": "success" if result.success else "error",
        "data": result.metadata if result.success else None,
        "error": result.error if not result.success else None
    }


if __name__ == "__main__":
    """Local test"""
    import json

    test_findings = [
        {
            "severity": "critical",
            "category": "security",
            "message": "SQL Inject risk",
            "suggestion": "Use parametric query",
            "line_number": 10,
            "line_content": "query = 'SELECT * FROM users'"
        },
        {
            "severity": "low",
            "category": "style",
            "message": "The variable name is not clear.",
            "suggestion": "Use descriptive names",
            "line_number": 5,
            "line_content": "x = 10"
        }
    ]

    result = execute({
        "findings": test_findings,
        "include_examples": True
    })

    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("\n" + "=" * 60)
    print("Markdown Report:")
    print("=" * 60)
    print(result["data"]["markdown"])
