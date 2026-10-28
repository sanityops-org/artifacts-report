#!/usr/bin/env python3
"""
Aircraft maintenance airworthiness decision-making skills processing script

The script realizes the core logic of airworthiness decision-making and runs using the sanityops_agent framework.
"""

import sys
import asyncio
from pathlib import Path
from typing import Dict, Any

from sanityops_agent import Tool, ToolContext, ToolResult

# Handle the module import at direct runtime
if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))

# Import tools
from skills.airworthiness_advisor.tools.query_airworthiness import QueryAirworthinessTool
from skills.airworthiness_advisor.tools.query_component_status import QueryComponentStatusTool
from skills.airworthiness_advisor.tools.query_maintenance_history import QueryMaintenanceHistoryTool
from skills.airworthiness_advisor.tools.generate_decision import GenerateDecisionTool


class AirworthinessAdvisorHandler:
    """Airworthiness decision-making processor for aircraft maintenance"""

    def __init__(self):
        self.airworthiness_tool = QueryAirworthinessTool()
        self.component_tool = QueryComponentStatusTool()
        self.history_tool = QueryMaintenanceHistoryTool()
        self.decision_tool = GenerateDecisionTool()

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Implement airworthiness decision-making

        Args:
            params: Parameter dictionary containing reg_no, part_no

        Returns:
            Dictionary of decision-making results
        """
        reg_no = params.get("reg_no")
        part_no = params.get("part_no")

        if not reg_no:
            return {
                "status": "error",
                "error": "The aircraft registration number is not provided.",
                "message": "Please provide the reg_no parameter"
            }

        # Step 1: Check the status of AD
        ad_result = await self.airworthiness_tool.execute(reg_no=reg_no)
        if not ad_result.success:
            return {
                "status": "error",
                "error": "Airworthiness status query failed",
                "details": ad_result.error
            }

        # Get the first AD that needs to be executed (if any)
        ad_list = ad_result.metadata.get("ad_list", [])
        open_ad = next((ad for ad in ad_list if ad.get("action_required")), None)
        ad_status = {
            "status": open_ad["status"] if open_ad else "complied",
            "action_required": open_ad["action_required"] if open_ad else False,
            "ad_id": open_ad["ad_id"] if open_ad else None,
        }

        # Step 2: Check the status of the parts
        component_status = {}
        if part_no:
            comp_result = await self.component_tool.execute(reg_no=reg_no, part_no=part_no)
            if comp_result.success:
                component_status = comp_result.metadata

        # Step 3: Check the history and defects
        history_result = await self.history_tool.execute(reg_no=reg_no, part_no=part_no)
        if not history_result.success:
            return {
                "status": "error",
                "error": "Resume query failed",
                "details": history_result.error
            }

        defects = history_result.metadata.get("open_defects", [])

        # Step 4: Generate decision-making
        assessment_data = {
            "ad_status": ad_status,
            "component_status": component_status,
            "defects": defects,
        }

        decision_result = await self.decision_tool.execute(
            reg_no=reg_no,
            assessment_data=assessment_data
        )

        if not decision_result.success:
            return {
                "status": "error",
                "error": "Decision generation failure",
                "details": decision_result.error
            }

        decision = decision_result.metadata

        return {
            "status": "success",
            "data": {
                "reg_no": reg_no,
                "assessment": decision["assessment"],
                "assessment_text": decision["assessment_text"],
                "open_actions": decision["open_actions"],
                "parts": decision["parts"],
                "ground_time_impact": decision["ground_time_impact"],
                "deferred_items": decision["deferred_items"],
                "rationale": decision["rationale"],
            },
            "message": f"Airworthiness decision-making completed: {decision['assessment_text']}"
        }


# Create a global processor instance
_handler = AirworthinessAdvisorHandler()


async def main(params: Dict[str, Any]) -> Dict[str, Any]:
    """Skill main entrance (asynchronous)"""
    return await _handler.execute(params)


def run(params: Dict[str, Any]) -> Dict[str, Any]:
    """Synchronized entrance function"""
    return asyncio.run(main(params))


if __name__ == "__main__":
    import json

    result = run({
        "reg_no": "B-1234",
        "part_no": "PN-12345"
    })

    print(json.dumps(result, indent=2, ensure_ascii=False))
