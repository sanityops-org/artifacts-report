#!/usr/bin/env python3
"""triage_check_red_flags: Red flag symptom screening (compulsory gate).

This tool must be called first when the patient describes the discomfort for the first time, and after each subsequent round of patient supplementary description.
The original description text of the patient is transmitted as it is, do not rewrite or summarize. Return hit=true indicates hit danger
Symptoms, must immediately stop the triage and registration process, and directly output the return advice guidelines; return hit=false
You can continue the routine guidance. This tool is read-only and does not produce any write operations.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore
from apis.triage_engine import check_red_flags

parameters: Dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "text": {
            "type": "string",
            "maxLength": 500,
            "description": "The patient's original oral description of discomfort in this round is transmitted as it is. Do not rewrite, delete or add medical judgment.",
        },
        "symptoms": {
            "type": "array",
            "items": {"type": "string", "maxLength": 30},
            "maxItems": 10,
            "description": "Optional. If the normalized symptom words have been extracted from the conversation (such as [\"headache\", \"dizziness\"]), they will be transmitted together; leave it blank when it is uncertain, and only pass text。",
        },
    },
    "required": ["text"],
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Args:
        params: {"text": str, "symptoms": list[str]（Optional)}

    Returns:
        {"status": "success", "data": {...}} Someone {"status": "error", "error": str}
    """
    text = params.get("text")
    if text is None:
        return {"status": "error", "error": "The required parameters are missing: text"}

    symptoms = params.get("symptoms") or []
    try:
        data_store = DataStore(data_dir=project_root / "data")
        rules = data_store.load_red_flag_rules()
        result = check_red_flags(str(text), rules, symptoms)
        return {"status": "success", "data": result.model_dump(mode="json")}
    except Exception as e:
        return {"status": "error", "error": f"Red flag symptom screening failed: {str(e)}"}


if __name__ == "__main__":
    print(execute({"text": "I suddenly had a terrible chest pain."}))
