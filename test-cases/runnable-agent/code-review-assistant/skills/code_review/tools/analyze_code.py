#!/usr/bin/env python3
"""
Code analysis tools

Analyze code files and identify potential problems, including security vulnerabilities, performance problems, readability problems, etc.
Inherit the sanityops_agent.Tool base class implementation.
"""

import ast
import re
from typing import Any, Dict, List

from sanityops_agent import Tool, ToolContext, ToolResult


class AnalyzeCodeTool(Tool):
    """Code analysis tools"""

    name = "analyze_code"
    description = "Analyze code files and identify potential problems, including security vulnerabilities, performance problems, readability problems, etc."
    parameters = {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "The content of the code to be analyzed"
            },
            "language": {
                "type": "string",
                "description": "Programming language",
                "enum": ["python", "javascript", "typescript", "java", "go", "rust", "cpp", "csharp", "ruby", "php"]
            },
            "focus_areas": {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": ["security", "performance", "readability", "maintainability"]
                },
                "description": "List of areas of concern"
            }
        },
        "required": ["code", "language"]
    }
    tags = ["analysis", "code-quality"]

    def __init__(self, context: ToolContext | None = None):
        super().__init__(context)

    async def execute(self, **kwargs) -> ToolResult:
        """
        Execute code analysis

        Args:
            code: The content of the code to be analyzed
            language: Programming language
            focus_areas: List of areas of concern

        Returns:
            ToolResult Including the analysis results
        """
        code = kwargs.get("code", "")
        language = kwargs.get("language", "python")
        focus_areas = kwargs.get("focus_areas", ["security", "readability", "maintainability"])

        # The empty code is valid and returns the empty result.
        if code is None:
            return ToolResult(
                content="Error: No code provided",
                success=False,
                error="Parameter verification failed, and code parameters need to be provided."
            )

        try:
            findings = []

            if language == "python":
                findings = self._analyze_python_code(code, focus_areas)
            else:
                findings = self._analyze_generic_code(code, language, focus_areas)

            result_data = {
                "findings": findings,
                "total_issues": len(findings),
                "language": language
            }

            return ToolResult(
                content=f"The code analysis was completed, and {len(findings)} problems were found.",
                success=True,
                metadata=result_data
            )

        except Exception as e:
            import traceback
            return ToolResult(
                content=f"There is an error in the analysis: {str(e)}",
                success=False,
                error=str(e),
                metadata={"traceback": traceback.format_exc()}
            )

    def _analyze_python_code(self, code: str, focus_areas: List[str]) -> List[Dict[str, Any]]:
        """Analyze Python code"""
        findings = []
        lines = code.split("\n")

        if "security" in focus_areas:
            findings.extend(self._check_security_issues(code, lines, "python"))
        if "readability" in focus_areas:
            findings.extend(self._check_readability_issues(code, lines, "python"))
        if "maintainability" in focus_areas:
            findings.extend(self._check_maintainability_issues(code, lines, "python"))
        if "performance" in focus_areas:
            findings.extend(self._check_performance_issues(code, lines, "python"))

        return findings

    def _analyze_generic_code(self, code: str, language: str, focus_areas: List[str]) -> List[Dict[str, Any]]:
        """General code analysis"""
        findings = []
        lines = code.split("\n")

        if "security" in focus_areas:
            findings.extend(self._check_security_issues(code, lines, language))

        return findings

    def _check_security_issues(self, code: str, lines: List[str], language: str) -> List[Dict[str, Any]]:
        """Check the safety issues"""
        findings = []

        # SQL Injection check
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            # Exclude comment lines
            if stripped.startswith("#") or stripped.startswith("//"):
                continue
            # Check the dynamic SQL splicing mode: SQL keywords are spliced with + in the string
            upper_line = line.upper()
            if ("SELECT" in upper_line or "INSERT" in upper_line or "UPDATE" in upper_line or "DELETE" in upper_line):
                if self._is_sql_concatenation(line):
                    findings.append({
                        "severity": "critical",
                        "category": "security",
                        "message": "SQL Injection risk: dynamic splicing of SQL statements",
                        "suggestion": "Use parametric query or ORM framework, such as SQLAlchemy、Django ORM",
                        "line_number": i,
                        "line_content": line.strip()
                    })

        # Sensitive information check
        sensitive_keywords = ["password", "api_key", "secret", "token"]
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            # Exclude comments and string literals
            if stripped.startswith("#") or stripped.startswith("//"):
                continue
            for keyword in sensitive_keywords:
                lower_line = line.lower()
                # Check the hard coding assignment mode:keyword = literal_value
                if keyword in lower_line and "=" in line:
                    parts = line.split("=", 1)
                    if len(parts) == 2:
                        left_side = parts[0].lower().strip()
                        right_side = parts[1].strip()
                        # Confirm that the keyword is on the left side of the assignment (in the variable name)
                        if keyword in left_side and self._is_literal_value(right_side):
                            findings.append({
                                "severity": "high",
                                "category": "security",
                                "message": f"Risk of sensitive information leakage: may contain hard coding {keyword}",
                                "suggestion": "Use environment variables or key management services to store sensitive information",
                                "line_number": i,
                                "line_content": line.strip()[:80] + "..." if len(line.strip()) > 80 else line.strip()
                            })
                            break  # Report only once

        # eval/exec Examine
        for i, line in enumerate(lines, 1):
            # Exclude in the comment line eval/exec
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith("//"):
                continue
            # Check the actual eval()/exec() call
            if re.search(r'\beval\s*\(', line) or re.search(r'\bexec\s*\(', line):
                findings.append({
                    "severity": "high",
                    "category": "security",
                    "message": "There are security risks in executing dynamic code using eval/exec",
                    "suggestion": "Use ast.literal_eval to replace eval, or refactor the code to avoid dynamic execution",
                    "line_number": i,
                    "line_content": line.strip()
                })

        return findings

    def _is_sql_concatenation(self, line: str) -> bool:
        """Check whether the line contains SQL splicing mode (SQL statement + variable splicing)"""
        # Use regular matching SQL string + splicing operator + variable pattern
        # Take for example: "SELECT ... " + user + " ..."
        # Someone 'SELECT ...' + user
        patterns = [
            # Python: "SQL" + variable Someone 'SQL' + variable
            r'["\']\s*(?:SELECT|INSERT|UPDATE|DELETE).*["\']\s*\+\s*\w+',
            # Python: variable + "SQL" Someone variable + 'SQL'
            r'\w+\s*\+\s*["\']\s*(?:SELECT|INSERT|UPDATE|DELETE)',
            # Python Format string: f"...{var}..." There are SQL keywords in it.
            r'f["\'].*(?:SELECT|INSERT|UPDATE|DELETE).*[{}\{]',
            # String formatting: "...%s..." % var has SQL
            r'["\'].*(?:SELECT|INSERT|UPDATE|DELETE).*["\']\s*%(?:\w+|\()',
            # .format() Method: "...{}...".format(var) has SQL
            r'["\'].*(?:SELECT|INSERT|UPDATE|DELETE).*["\']\.format\s*\(',
        ]
        for pattern in patterns:
            if re.search(pattern, line, re.IGNORECASE):
                return True
        return False

    def _is_in_string(self, line: str, keyword: str) -> bool:
        """Check whether the keyword is in the string literal (tracking quotation mark pair)"""
        parts = re.split(r'(["\'])', line)
        in_string = False
        quote_char = None
        for part in parts:
            if part in ('"', "'"):
                if not in_string:
                    in_string = True
                    quote_char = part
                elif part == quote_char:
                    in_string = False
                    quote_char = None
            elif in_string and keyword.upper() in part.upper():
                return True
        return False

    def _is_literal_value(self, value: str) -> bool:
        """Check whether it is a literal value (excluding variable references, function calls, etc.)"""
        v = value.strip()
        # Empty value
        if not v:
            return False
        # String literal quantity
        if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
            return True
        # Number
        try:
            float(v)
            return True
        except ValueError:
            pass
        # Lists, dictionaries, etc.
        if v.startswith(("[", "{", "(")):
            return True
        return False

    def _check_readability_issues(self, code: str, lines: List[str], language: str) -> List[Dict[str, Any]]:
        """Check the readability problem"""
        findings = []

        # Variable Naming Check - Matching Simple Assignment Pattern
        bad_names = ["x", "y", "z", "tmp", "temp", "obj"]
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            # Skip the comment line
            if stripped.startswith("#") or stripped.startswith("//"):
                continue
            # Skip function parameter definition, for loop variables, etc.
            if stripped.startswith("def ") or stripped.startswith("for ") or stripped.startswith("if "):
                continue
            for name in bad_names:
                # Accurately match simple variable assignment: name = value or name = value
                # Use regular rules to ensure that it is an independent variable name.
                pattern = rf'\b{name}\b\s*='
                if re.search(pattern, line):
                    findings.append({
                        "severity": "low",
                        "category": "style",
                        "message": f"The meaning of the variable name '{name}' is unclear",
                        "suggestion": "Use more descriptive variable names, such as 'index', 'count', 'result', etc.",
                        "line_number": i,
                        "line_content": line.strip()
                    })

        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                findings.append({
                    "severity": "low",
                    "category": "style",
                    "message": "The line length is more than 120 characters",
                    "suggestion": "Consider line changing or using a multi-line string",
                    "line_number": i,
                    "line_content": line[:80] + "..."
                })

        return findings

    def _check_maintainability_issues(self, code: str, lines: List[str], language: str) -> List[Dict[str, Any]]:
        """Check the maintainability problem"""
        findings = []

        in_function = False
        function_start = 0
        function_lines = 0

        for i, line in enumerate(lines, 1):
            if line.strip().startswith("def "):
                if in_function and function_lines > 50:
                    findings.append({
                        "severity": "medium",
                        "category": "maintainability",
                        "message": f"The function is too long ({function_lines} lines)",
                        "suggestion": "Consider splitting the function into several small functions, and each function only does one thing.",
                        "line_number": function_start,
                        "line_content": f"The function starts from the {function_start} line"
                    })
                in_function = True
                function_start = i
                function_lines = 0
            elif in_function:
                if line.strip() and not line.strip().startswith("#"):
                    function_lines += 1

        has_docstring = '"""' in code or "'''" in code
        if not has_docstring:
            findings.append({
                "severity": "low",
                "category": "documentation",
                "message": "Missing document string",
                "suggestion": "Add document strings to modules and functions to explain functions and parameters"
            })

        return findings

    def _check_performance_issues(self, code: str, lines: List[str], language: str) -> List[Dict[str, Any]]:
        """Check the performance problems"""
        findings = []

        for i, line in enumerate(lines, 1):
            if "range(len(" in line:
                findings.append({
                    "severity": "low",
                    "category": "performance",
                    "message": "Use range(len()) mode to traverse",
                    "suggestion": "Directly use for item in iterable or enumerate()",
                    "line_number": i,
                    "line_content": line.strip()
                })

        return findings


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
    tool = AnalyzeCodeTool()
    result = asyncio.run(tool.execute(**params))
    return {
        "status": "success" if result.success else "error",
        "data": result.metadata if result.success else None,
        "error": result.error if not result.success else None
    }


if __name__ == "__main__":
    """Local test"""
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

    import json
    result = execute({
        "code": test_code,
        "language": "python",
        "focus_areas": ["security", "readability", "maintainability", "performance"]
    })

    print(json.dumps(result, indent=2, ensure_ascii=False))
