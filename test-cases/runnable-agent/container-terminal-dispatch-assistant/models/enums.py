"""
Enumeration definition module

Contains all the enumeration types required for the container terminal dispatching system.
"""

from enum import Enum


class VesselStatus(str, Enum):
    """
    Ship status enumeration

    Describe the different states of the ship in the life cycle of port operation.
    """
    INBOUND = "inbound"          # Entering the port
    AT_ANCHOR = "at_anchor"      # Anchor and wait
    BERTHING = "berthing"        # In the moor
    BERTHED = "berthed"          # Already docked
    WORKING = "working"          # Doing homework
    DEPARTING = "departing"      # In the middle of the parking
    DEPARTED = "departed"        # Already left Hong Kong


class BerthStatus(str, Enum):
    """
    Enumeration of berth status

    Describe the availability and operation status of the berth.
    """
    AVAILABLE = "available"      # Available
    OCCUPIED = "occupied"        # Already occupied
    RESERVED = "reserved"        # Reserved
    MAINTENANCE = "maintenance"  # In maintenance


class BlockStatus(str, Enum):
    """
    Enumeration of the status of the warehouse block

    Describe the operation status of the warehouse block.
    """
    OPERATIONAL = "operational"  # Normal work
    FULL = "full"                # It is full
    CLOSED = "closed"            # Closed
    MAINTENANCE = "maintenance"  # In maintenance


class ContainerType(str, Enum):
    """
    Enumeration of container types

    According to the type of goods and the type of container classified in the flow.
    """
    IMPORT = "import"                # Import box
    EXPORT = "export"                # Export box
    TRANSSHIPMENT = "transshipment"  # Transit box
    EMPTY = "empty"                  # Empty box
    DANGEROUS = "dangerous"          # Dangerous goods box
    REEFER = "reefer"                # Refrigerator


class ContainerSize(str, Enum):
    """
    Enumeration of container sizes

    Container size type based on ISO standard.
    """
    TWENTY_GP = "20GP"          # 20Feet ordinary box
    FORTY_GP = "40GP"           # 40Feet ordinary box
    FORTY_HQ = "40HQ"           # 40Foot-high box
    FORTY_FIVE_LHC = "45LHC"    # 45Foot-high box

    # Commonly used alias
    GP20 = "20GP"               # 20Alias of foot ordinary box
    GP40 = "40GP"               # 40Alias of foot ordinary box
    HQ40 = "40HQ"               # 40Foot-high box alias


class EquipmentType(str, Enum):
    """
    Enumeration of device types

    Various types of machinery and equipment required for port operations.
    """
    QUAY_CRANE = "quay_crane"           # Shore bridge
    RTG = "rtg"                         # Tire crane
    RMG = "rmg"                         # Track crane
    YARD_TRUCK = "yard_truck"           # On-site trailer
    REACH_STACKER = "reach_stacker"     # Front hanging
    TOP_LOADER = "top_loader"           # Top hanging


class EquipmentStatus(str, Enum):
    """
    Device status enumeration

    Describe the operating status of port equipment.
    """
    IDLE = "idle"               # Free
    WORKING = "working"         # Doing homework
    MOVING = "moving"           # Moving
    FAULT = "fault"             # Breakdown
    MAINTENANCE = "maintenance" # In maintenance
    OFFLINE = "offline"         # Offline


class TaskType(str, Enum):
    """
    Enumeration of task types

    The main types of port operation tasks.
    """
    LOAD = "load"               # Ship
    DISCHARGE = "discharge"     # Unload the ship
    YARD_MOVE = "yard_move"     # In-field transfer box
    GATE_OUT = "gate_out"       # Exit the gate
    GATE_IN = "gate_in"         # Enter the gate


class TaskStatus(str, Enum):
    """
    Enumeration of task status

    Describe the life cycle status of the task.
    """
    PENDING = "pending"             # Pending
    ASSIGNED = "assigned"           # Assigned
    IN_PROGRESS = "in_progress"     # In progress
    COMPLETED = "completed"         # Completed
    FAILED = "failed"               # Be defeated
    CANCELLED = "cancelled"         # Canceled


class GateChannelType(str, Enum):
    """
    Enumeration of gate channel types

    Distinguish between entry and exit channels.
    """
    INBOUND = "inbound"     # Gate passage
    OUTBOUND = "outbound"   # Exit channel


class GateChannelStatus(str, Enum):
    """
    Enumeration of gate channel status

    Describe the operation status of the gate passage.
    """
    OPEN = "open"           # Come into bloom
    CLOSED = "closed"       # Shut
    CONGESTED = "congested" # Traffic jam


class AppointmentStatus(str, Enum):
    """
    Appointment status enumeration

    Describe the life cycle status of the card entry appointment.
    """
    PENDING = "pending"     # To be confirmed
    VALID = "valid"         # Effective
    EXPIRED = "expired"     # Expired
    COMPLETED = "completed" # Completed
    CANCELLED = "cancelled" # Canceled


class EventType(str, Enum):
    """
    Enumeration of event types

    Various types of events recorded by the system.
    """
    TASK_STARTED = "task_started"       # The mission begins.
    TASK_PROGRESS = "task_progress"     # Task progress update
    TASK_COMPLETED = "task_completed"   # The task is completed
    TASK_FAILED = "task_failed"         # The mission failed.
    STATUS_CHANGED = "status_changed"   # Status change
    ALERT = "alert"                     # Alarm


# Export all enumeration types
__all__ = [
    "VesselStatus",
    "BerthStatus",
    "BlockStatus",
    "ContainerType",
    "ContainerSize",
    "EquipmentType",
    "EquipmentStatus",
    "TaskType",
    "TaskStatus",
    "GateChannelType",
    "GateChannelStatus",
    "AppointmentStatus",
    "EventType",
]
