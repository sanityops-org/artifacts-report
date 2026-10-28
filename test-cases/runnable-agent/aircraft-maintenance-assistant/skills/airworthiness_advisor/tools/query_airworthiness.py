#!/usr/bin/env python3
"""
Airworthiness status query tool

Query the airworthiness status of AD to determine the conformity.
"""

import sys
from pathlib import Path
from typing import Any, Dict, Optional, List

from sanityops_agent import Tool, ToolContext, ToolResult

# Handle the module import at direct runtime
if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent.parent
    sys.path.insert(0, str(project_root))

from data import sim_db
from data.helpers import evaluate_ad_compliance


class QueryAirworthinessTool(Tool):
    """Airworthiness status query tool"""

    name = "query_airworthiness"
    description = "Query the airworthiness status of AD and determine the conformity"
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
            "ad_id": {
                "type": "string",
                "description": "AD Number, optional. If it is not provided, all AD statuses of the aircraft will be returned.",
                "minLength": 3,
                "maxLength": 30,
                "pattern": "^AD-[0-9]{4}-[0-9]{2}-[0-9]{3}$",
            },
        },
        "required": ["reg_no"],
        "additionalProperties": False,
    }
    tags = ["airworthiness", "ad", "compliance"]

    def __init__(self, context: ToolContext | None = None):
        super().__init__(context)

    async def execute(
        self,
        reg_no: str,
        ad_id: Optional[str] = None,
        **kwargs
    ) -> ToolResult:
        """
        Execute the airworthiness status query

        Args:
            reg_no: Aircraft registration number
            ad_id: AD Number (optional)

        Returns:
            ToolResult Contains AD status information
        """
        # Verify the existence of the aircraft
        aircraft = sim_db.AIRCRAFT_RECORDS.get(reg_no)
        if not aircraft:
            return ToolResult(
                content=f"Query failure: the plane {reg_no} does not exist",
                success=False,
                error=f"The plane {reg_no} does not exist"
            )

        ad_compliance_records = aircraft.get("ad_compliance", {})

        # Query single AD
        if ad_id:
            ad = sim_db.AIRWORTHINESS_DIRECTIVES.get(ad_id)
            if not ad:
                return ToolResult(
                    content=f"Query failure: AD {ad_id} does not exist",
                    success=False,
                    error=f"AD {ad_id} does not exist"
                )

            compliance_record = ad_compliance_records.get(ad_id)
            result = evaluate_ad_compliance(ad, compliance_record)

            return ToolResult(
                success=True,
                content=f"AD {ad_id} State: {result['status']}",
                metadata={
                    "ad_id": ad_id,
                    **result,
                    "title": ad.get("title"),
                    "affected_parts": ad.get("affected_parts", []),
                }
            )

        # Query all AD
        ad_list = []
        for aid, ad in sim_db.AIRWORTHINESS_DIRECTIVES.items():
            if ad.get("status") == "superseded":
                continue  # Skip the replaced

            compliance_record = ad_compliance_records.get(aid)
            result = evaluate_ad_compliance(ad, compliance_record)
            ad_list.append({
                "ad_id": aid,
                "title": ad.get("title"),
                "status": result["status"],
                "action_required": result["action_required"],
            })

        return ToolResult(
            success=True,
            content=f"Airplane {reg_no} has a total of {len(ad_list)} AD",
            metadata={
                "reg_no": reg_no,
                "ad_count": len(ad_list),
                "ad_list": ad_list,
            }
        )


# Synchronized entrance
def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """Synchronous execution entrance"""
    import asyncio
    tool = QueryAirworthinessTool()
    result = asyncio.run(tool.execute(**params))
    return {
        "status": "success" if result.success else "error",
        "data": result.metadata if result.success else None,
        "error": result.error if not result.success else None,
    }


if __name__ == "__main__":
    import json
    result = execute({"reg_no": "B-1234", "ad_id": "AD-2024-01-001"})
    print(json.dumps(result, indent=2, ensure_ascii=False))
