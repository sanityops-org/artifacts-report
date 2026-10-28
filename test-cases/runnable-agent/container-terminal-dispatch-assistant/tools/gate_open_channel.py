#!/usr/bin/env python3
"""
gate_open_channel: Set the status of the designated gate channel to open.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore
from models.enums import GateChannelStatus
from tools._permission import check_tool_permission


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Carry out the open operation of the gate channel.

    Args:
        params:
            - channel_id: Channel ID to be opened (required)

    Returns:
        {"status": "success", "message": "..."} Someone
        {"status": "error", "error": "..."}
    """

    # Permission verification
    permission_error = check_tool_permission("gate_open_channel", params)
    if permission_error:
        return permission_error

    channel_id = params.get("channel_id")

    # Parameter verification
    if not channel_id:
        return {
            "status": "error",
            "error": "The required parameters are missing: channel_id"
        }

    data_store = DataStore(data_dir=project_root / "data")

    try:
        channels = data_store.load_gate_channels()

        # Find the channel
        channel = None
        for c in channels:
            if c.channel_id == channel_id:
                channel = c
                break

        if not channel:
            return {
                "status": "error",
                "error": f"Gate channel {channel_id} does not exist"
            }

        # Check the current status
        if channel.status == GateChannelStatus.OPEN:
            return {
                "status": "success",
                "message": f"Gate channel {channel_id} ({channel.channel_name}) is already open."
            }

        # Perform open operation
        channel.status = GateChannelStatus.OPEN

        # Save data
        data_store.save_gate_channels(channels)

        return {
            "status": "success",
            "message": f"Gate channel {channel_id} ({channel.channel_name}) has been successfully opened"
        }

    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to open the gate channel: {str(e)}"
        }
