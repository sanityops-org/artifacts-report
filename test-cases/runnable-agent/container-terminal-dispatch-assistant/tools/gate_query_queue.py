#!/usr/bin/env python3
"""
gate_query_queue: Check the queue of the gate passage.

Return the total number of queues and the queue information of each channel.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check the queue at the gate.

    Args:
        params: Query parameters (no parameters, reserved for extension)

    Returns:
        {"status": "success", "data": {"total_queue": N, "inbound_queue": N, "outbound_queue": N, "channels": [...]}} Someone
        {"status": "error", "error": "..."}
    """
    data_store = DataStore(data_dir=project_root / "data")

    try:
        channels = data_store.load_gate_channels()

        # Calculate the queue statistics
        total_queue = 0
        inbound_queue = 0
        outbound_queue = 0
        channel_queues = []

        for channel in channels:
            queue_len = channel.queue_length
            total_queue += queue_len

            if channel.type.value == "inbound":
                inbound_queue += queue_len
            else:
                outbound_queue += queue_len

            channel_queues.append({
                "channel_id": channel.channel_id,
                "channel_name": channel.channel_name,
                "type": channel.type.value,
                "status": channel.status.value,
                "queue_length": queue_len
            })

        return {
            "status": "success",
            "data": {
                "total_queue": total_queue,
                "inbound_queue": inbound_queue,
                "outbound_queue": outbound_queue,
                "channels": channel_queues
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to query the queue: {str(e)}"
        }
