#!/usr/bin/env python3
"""
nutrition_targets_get: Show the daily nutrition targets a summary is compared against.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import get_data_store
from apis.disclaimers import DIETITIAN_NOTE, ESTIMATE_DISCLAIMER

parameters = {
    "type": "object",
    "properties": {}
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Read the configured daily nutrition targets.

    Args:
        params: No parameters required

    Returns:
        {"status": "success", "data": {...targets...}} or
        {"status": "error", "error": "..."}
    """
    try:
        store = get_data_store(str(project_root / "data"))
        targets = store.load_targets()

        if targets is None:
            return {"status": "error", "error": "No nutrition targets are configured"}

        payload = targets.model_dump(mode="json")
        payload["is_estimate"] = True
        payload["disclaimer"] = ESTIMATE_DISCLAIMER
        payload["dietitian_note"] = DIETITIAN_NOTE

        return {"status": "success", "data": payload}

    except Exception as e:
        return {"status": "error", "error": f"Failed to read nutrition targets: {str(e)}"}
