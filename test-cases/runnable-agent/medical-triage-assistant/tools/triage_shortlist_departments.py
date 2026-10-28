#!/usr/bin/env python3
"""triage_shortlist_departments: According to the symptoms, candidate departments (up to 3) can be selected.

It is called after the red flag screening is missed and the structured follow-up is completed. Return to the list of candidates and finally recommend the department
Only 1 can be selected from the list. This tool is read-only, only returns to the department, and does not return any disease names or diagnostic conclusions.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore
from apis.triage_engine import shortlist_departments

parameters: Dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "symptoms": {
            "type": "array",
            "items": {"type": "string", "maxLength": 30},
            "minItems": 1,
            "maxItems": 10,
            "description": "A list of normalized symptom words extracted from the dialogue, such as [\"fever\", \"cough\"]. Use standardized symptom words, and don't pass them into the whole sentence.",
        },
        "age": {
            "type": "integer",
            "minimum": 0,
            "maximum": 120,
            "description": "The age of the patient (years old). It must be introduced when it is known: the election meeting at the age of 14 is forcibly converged to pediatrics. It can be omitted when it is unknown.",
        },
        "max_candidates": {
            "type": "integer",
            "minimum": 1,
            "maximum": 3,
            "description": "The maximum number of candidate departments is 3 by default. Usually there is no need to pass it in.",
        },
    },
    "required": ["symptoms"],
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Args:
        params: {"symptoms": list[str], "age": int（Optional), "max_candidates": int (optional)}

    Returns:
        {"status": "success", "data": {"candidates": [...], "fallback_department": ...,
         "age_rule_applied": bool, "note": str}} Someone {"status": "error", "error": str}
    """
    raw_symptoms = params.get("symptoms") or []
    symptoms = [str(item).strip() for item in raw_symptoms if str(item).strip()]
    if not symptoms:
        return {"status": "error", "error": "The required parameters are missing: symptoms"}

    age = params.get("age")
    max_candidates = params.get("max_candidates") or 3

    try:
        data_store = DataStore(data_dir=project_root / "data")
        mappings = data_store.load_symptom_map()
        departments = data_store.load_departments()
        result = shortlist_departments(
            symptoms,
            mappings,
            departments,
            age=int(age) if age is not None else None,
            max_candidates=int(max_candidates),
        )
        return {"status": "success", "data": result.model_dump(mode="json")}
    except Exception as e:
        return {"status": "error", "error": f"The candidate department failed to converge.: {str(e)}"}


if __name__ == "__main__":
    print(execute({"symptoms": ["Headache", "Dizziness"]}))
