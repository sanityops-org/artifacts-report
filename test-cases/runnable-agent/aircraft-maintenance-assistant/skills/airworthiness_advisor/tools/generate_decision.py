#!/usr/bin/env python3
"""
Maintenance decision generation tool

Comprehensively generate a maintenance plan decision-making list.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List

from sanityops_agent import Tool, ToolContext, ToolResult

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent.parent
    sys.path.insert(0, str(project_root))


class GenerateDecisionTool(Tool):
    """Maintenance decision generation tool"""

    name = "generate_decision"
    description = "Comprehensively generate a maintenance plan decision-making list"
    parameters = {
        "type": "object",
        "properties": {
            "reg_no": {
                "type": "string",
                "description": "Aircraft registration number, such as B-1234",
                "minLength": 2,
                "maxLength": 10,
                "pattern": "^[A-Z]-[0-9A-Z]+$",
            },
            "assessment_data": {
                "type": "object",
                "description": "Evaluation data, including ad_status, component_status, defects, etc.",
                "properties": {
                    "ad_status": {
                        "type": "object",
                        "description": "AD Airworthiness status, including the execution of a single AD",
                        "properties": {
                            "ad_id": {
                                "type": "string",
                                "description": "AD Number, such as AD-2024-01-001",
                                "minLength": 3,
                                "maxLength": 30,
                            },
                            "status": {
                                "type": "string",
                                "description": "AD Execution status: compliant-executed, open-not executed, superseded-replaced",
                                "enum": ["compliant", "open", "superseded"],
                            },
                            "action_required": {
                                "type": "boolean",
                                "description": "Do you need to perform the action?",
                            },
                            "message": {
                                "type": "string",
                                "description": "Status description information",
                                "maxLength": 200,
                            },
                        },
                        "additionalProperties": False,
                    },
                    "component_status": {
                        "type": "object",
                        "description": "Part life/time control status, including remaining life and early warning level",
                        "properties": {
                            "part_no": {
                                "type": "string",
                                "description": "Part number, such as PN-12345",
                                "minLength": 3,
                                "maxLength": 30,
                            },
                            "alert_level": {
                                "type": "string",
                                "description": "Early warning level: ok-normal, warning-warning, critical-critical, exceeded-over-limit",
                                "enum": ["ok", "warning", "critical", "exceeded"],
                            },
                            "remaining_hours": {
                                "type": "number",
                                "description": "Remaining flight hours",
                                "minimum": 0,
                                "maximum": 50000,
                            },
                            "remaining_cycles": {
                                "type": "number",
                                "description": "Remaining number of cycles",
                                "minimum": 0,
                                "maximum": 30000,
                            },
                        },
                        "additionalProperties": False,
                    },
                    "defects": {
                        "type": "array",
                        "description": "List of legacy defects, including defect ID, description and impact level",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "string",
                                    "description": "Defect number, such as DEF-001",
                                    "minLength": 3,
                                    "maxLength": 20,
                                },
                                "description": {
                                    "type": "string",
                                    "description": "Defect description",
                                    "maxLength": 500,
                                },
                                "impact": {
                                    "type": "string",
                                    "description": "Impact level: grounding-stop, mel-MEL control, monitor-monitoring",
                                    "enum": ["grounding", "mel", "monitor"],
                                },
                                "mel_reference": {
                                    "type": "string",
                                    "description": "MEL Reference number",
                                    "maxLength": 30,
                                },
                                "mel_deadline": {
                                    "type": "string",
                                    "description": "MEL Deadline, format YYYY-MM-DD",
                                    "pattern": "^\\d{4}-\\d{2}-\\d{2}$",
                                },
                            },
                            "additionalProperties": False,
                        },
                        "maxItems": 50,
                    },
                    "total_hours": {
                        "type": "number",
                        "description": "Total flight hours of the plane",
                        "minimum": 0,
                        "maximum": 200000,
                    },
                    "total_cycles": {
                        "type": "number",
                        "description": "The total number of cycles of the aircraft",
                        "minimum": 0,
                        "maximum": 100000,
                    },
                },
                "additionalProperties": False,
            },
        },
        "required": ["reg_no", "assessment_data"],
        "additionalProperties": False,
    }
    tags = ["decision", "maintenance", "planning"]

    def __init__(self, context: ToolContext | None = None):
        super().__init__(context)

    async def execute(
        self,
        reg_no: str,
        assessment_data: Dict[str, Any],
        **kwargs
    ) -> ToolResult:
        """Executive decision-making generation"""
        ad_status = assessment_data.get("ad_status", {})
        component_status = assessment_data.get("component_status", {})
        defects = assessment_data.get("defects", [])

        open_actions: List[Dict[str, Any]] = []
        parts: List[Dict[str, Any]] = []
        deferred_items: List[Dict[str, Any]] = []
        ground_time_hours = 0
        rationale: List[str] = []

        # Analyze the status of AD
        if ad_status.get("action_required"):
            open_actions.append({
                "priority": "critical",
                "action": f"Execute AD: {ad_status.get('ad_id', 'Unknown')}",
                "reason": ad_status.get("message", "AD Not executed"),
            })
            ground_time_hours += 4
            rationale.append(f"AD {ad_status.get('ad_id')} Need to be implemented")

        # Analyze the status of components
        alert_level = component_status.get("alert_level", "ok")
        if alert_level == "exceeded":
            open_actions.append({
                "priority": "critical",
                "action": f"Replacement parts: {component_status.get('part_no', 'unknown')}",
                "reason": "The life span has exceeded the limit.",
            })
            parts.append({
                "part_no": component_status.get("part_no"),
                "quantity": 1,
                "priority": "critical",
            })
            ground_time_hours += 8
            rationale.append(f"Parts {component_status.get('part_no')} life exceeds the limit")
        elif alert_level == "critical":
            open_actions.append({
                "priority": "high",
                "action": f"Planned replacement parts: {component_status.get('part_no', 'unknown')}",
                "reason": "The life of the piece is close to the limit",
            })
            parts.append({
                "part_no": component_status.get("part_no"),
                "quantity": 1,
                "priority": "high",
            })
            rationale.append(f"Parts {component_status.get('part_no')} life is close to the limit")
        elif alert_level == "warning":
            open_actions.append({
                "priority": "medium",
                "action": f"Monitoring components: {component_status.get('part_no', 'unknown')}",
                "reason": "The life piece enters the early warning area.",
            })
            rationale.append(f"Parts {component_status.get('part_no')} enter the warning")

        # Analyze defects
        for defect in defects:
            impact = defect.get("impact", "monitor")
            if impact == "grounding":
                open_actions.append({
                    "priority": "critical",
                    "action": f"Dealing with defects: {defect.get('description', 'unknown')}",
                    "reason": "Serious defects affect airworthiness",
                })
                ground_time_hours += 4
                rationale.append(f"Defect {defect.get('id')} affects airworthiness")
            elif impact == "mel":
                deferred_items.append({
                    "id": defect.get("id"),
                    "description": defect.get("description"),
                    "mel_reference": defect.get("mel_reference"),
                    "deadline": defect.get("mel_deadline"),
                })
                rationale.append(f"Defect {defect.get('id')} included in MEL control")

        # Comprehensive judgment
        critical_actions = [a for a in open_actions if a["priority"] == "critical"]
        if critical_actions:
            assessment = "grounding"
            assessment_text = "Can't be released"
        elif deferred_items:
            assessment = "restricted"
            assessment_text = "Restricted release"
        else:
            assessment = "airworthy"
            assessment_text = "Can be released"

        return ToolResult(
            success=True,
            content=f"Make a strategic decision: {assessment_text}",
            metadata={
                "reg_no": reg_no,
                "assessment": assessment,
                "assessment_text": assessment_text,
                "open_actions": open_actions,
                "parts": parts,
                "ground_time_impact": {
                    "hours": ground_time_hours,
                    "requires_ground_stop": ground_time_hours > 0,
                },
                "deferred_items": deferred_items,
                "rationale": rationale,
            }
        )


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """Synchronous execution entrance"""
    import asyncio
    tool = GenerateDecisionTool()
    result = asyncio.run(tool.execute(**params))
    return {
        "status": "success" if result.success else "error",
        "data": result.metadata if result.success else None,
        "error": result.error if not result.success else None,
    }


if __name__ == "__main__":
    import json
    result = execute({
        "reg_no": "B-1234",
        "assessment_data": {
            "ad_status": {"status": "open", "action_required": True, "ad_id": "AD-2024-02-001"},
            "component_status": {"alert_level": "warning", "part_no": "PN-12345"},
            "defects": [],
        }
    })
    print(json.dumps(result, indent=2, ensure_ascii=False))
