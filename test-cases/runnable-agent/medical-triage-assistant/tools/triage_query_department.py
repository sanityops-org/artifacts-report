#!/usr/bin/env python3
"""triage_query_department: Inquire about the business scope, outpatient location and pre-treatment preparation tips of individual departments.

Call it after determining the recommended department to explain the location and precautions to the patient. This tool is read-only and does not return.
Disease name or diagnostic information.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore

parameters: Dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "department_id": {
            "type": "string",
            "enum": [
                "dept_general_internal",
                "dept_surgery",
                "dept_orthopedics",
                "dept_obgyn",
                "dept_pediatrics",
                "dept_ophthalmology",
                "dept_ent",
                "dept_dentistry",
                "dept_dermatology",
                "dept_neurology",
                "dept_cardiology",
                "dept_emergency",
            ],
            "description": "Department identification. You must use the department_id in the candidate return, and do not use the English display name of the department.",
        }
    },
    "required": ["department_id"],
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Args:
        params: {"department_id": str}

    Returns:
        {"status": "success", "data": {"department_id", "name", "category",
         "description", "location", "preparation"}} Someone {"status": "error", "error": str}
    """
    department_id = params.get("department_id")
    if not department_id:
        return {"status": "error", "error": "The required parameters are missing: department_id"}

    try:
        data_store = DataStore(data_dir=project_root / "data")
        departments = data_store.load_departments()
        for department in departments:
            if department.department_id == department_id:
                return {"status": "success", "data": department.model_dump(mode="json")}
        available = ", ".join(d.department_id for d in departments)
        return {
            "status": "error",
            "error": f"The department does not exist: {department_id}, the available department: {available}",
        }
    except Exception as e:
        return {"status": "error", "error": f"Department inquiry failed: {str(e)}"}


if __name__ == "__main__":
    print(execute({"department_id": "dept_neurology"}))
