#!/usr/bin/env python3
"""
gate_query_status: Query the occupancy status and queue information of the gate channel.

Support filtering by channel ID, channel type and status.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform the gate channel status query.

    Args:
        params:
            - channel_id: Channel ID, specify to query a single channel (optional)
            - type: Channel type filtering (inbound, outbound) (optional)
            - status: Channel status filtering (open, closed, congested) (optional)

    Returns:
        {"status": "success", "data": {"channels": [...]}} Someone
        {"status": "success", "data": {"channel": {...}}} Someone
        {"status": "error", "error": "..."}
    """
    data_store = DataStore(data_dir=project_root / "data")
    channel_id = params.get("channel_id")
    type_filter = params.get("type")
    status_filter = params.get("status")

    try:
        channels = data_store.load_gate_channels()

        if channel_id:
            # Query a single channel
            for channel in channels:
                if channel.channel_id == channel_id:
                    return {
                        "status": "success",
                        "data": {
                            "channel": channel.model_dump(mode="json")
                        }
                    }
            # No channel found
            return {
                "status": "error",
                "error": f"Gate channel {channel_id} does not exist"
            }

        # Apply filter conditions
        filtered_channels = channels

        if type_filter:
            filtered_channels = [
                c for c in filtered_channels if c.type.value == type_filter
            ]

        if status_filter:
            filtered_channels = [
                c for c in filtered_channels if c.status.value == status_filter
            ]

        return {
            "status": "success",
            "data": {
                "channels": [c.model_dump(mode="json") for c in filtered_channels]
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to query the status of the gate channel: {str(e)}"
        }
