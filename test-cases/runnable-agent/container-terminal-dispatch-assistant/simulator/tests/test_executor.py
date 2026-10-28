"""
Execute the simulator test module

Test TimeController, EventBus, and Simulator classes.
"""

import pytest
from datetime import datetime

from simulator.time_controller import TimeController
from simulator.event_bus import EventBus
from simulator.executor import Simulator
from models.enums import EventType


class TestTimeController:
    """TimeController Test class"""

    def test_init_default_time(self):
        """Test the default initialization using the current time"""
        controller = TimeController()
        current_time = datetime.now().strftime("%Y-%m-%dT%H:%M")
        # The time obtained should be close to the current time (minute difference is allowed)
        result = controller.get_time()
        assert result.startswith(datetime.now().strftime("%Y-%m-%d"))

    def test_init_with_time(self):
        """Test to initialize with the specified time"""
        controller = TimeController(initial_time="2024-01-15T08:00")
        assert controller.get_time() == "2024-01-15T08:00"

    def test_advance(self):
        """Test progress time"""
        controller = TimeController(initial_time="2024-01-15T08:00")
        result = controller.advance(30)
        assert result == "2024-01-15T08:30"
        assert controller.get_time() == "2024-01-15T08:30"

    def test_advance_multiple(self):
        """Test the progress time many times"""
        controller = TimeController(initial_time="2024-01-15T08:00")
        controller.advance(60)
        controller.advance(30)
        assert controller.get_time() == "2024-01-15T09:30"

    def test_advance_cross_hour(self):
        """The test crosses the hourly boundary"""
        controller = TimeController(initial_time="2024-01-15T08:45")
        result = controller.advance(30)
        assert result == "2024-01-15T09:15"

    def test_advance_cross_day(self):
        """Test to cross the date boundary"""
        controller = TimeController(initial_time="2024-01-15T23:30")
        result = controller.advance(60)
        assert result == "2024-01-16T00:30"

    def test_set_time(self):
        """Test setting time"""
        controller = TimeController(initial_time="2024-01-15T08:00")
        controller.set_time("2024-01-20T10:00")
        assert controller.get_time() == "2024-01-20T10:00"


class TestEventBus:
    """EventBus Test class"""

    def test_subscribe_and_publish(self):
        """Test subscription and release events"""
        bus = EventBus()
        received_events = []

        def callback(event):
            received_events.append(event)

        bus.subscribe(EventType.TASK_STARTED, callback)
        event = bus.emit(EventType.TASK_STARTED, {"task_id": "T001"}, "EX0001")

        assert len(received_events) == 1
        assert received_events[0].event_type == EventType.TASK_STARTED
        assert received_events[0].payload == {"task_id": "T001"}
        assert received_events[0].execution_id == "EX0001"

    def test_multiple_subscribers(self):
        """Test multiple subscribers"""
        bus = EventBus()
        received1 = []
        received2 = []

        bus.subscribe(EventType.TASK_COMPLETED, lambda e: received1.append(e))
        bus.subscribe(EventType.TASK_COMPLETED, lambda e: received2.append(e))

        bus.emit(EventType.TASK_COMPLETED, {"progress": 100}, None)

        assert len(received1) == 1
        assert len(received2) == 1

    def test_no_subscribers(self):
        """Release events when testing no subscribers"""
        bus = EventBus()
        # An exception should not be thrown when there is no subscriber.
        event = bus.emit(EventType.ALERT, {"message": "test"}, None)
        assert event.event_type == EventType.ALERT

    def test_emit_returns_event(self):
        """Test emit returns the event object"""
        bus = EventBus()
        event = bus.emit(
            EventType.TASK_PROGRESS, {"progress": 50}, "EX0001"
        )
        assert event.event_id.startswith("E")
        assert event.event_type == EventType.TASK_PROGRESS
        assert event.timestamp is not None
        assert event.execution_id == "EX0001"
        assert event.payload == {"progress": 50}

    def test_publish(self):
        """Test and release directly FeedbackEvent"""
        bus = EventBus()
        received = []

        bus.subscribe(EventType.TASK_FAILED, lambda e: received.append(e))

        from models.execution import FeedbackEvent
        event = FeedbackEvent(
            event_id="E0001",
            event_type=EventType.TASK_FAILED,
            timestamp="2024-01-15T10:00",
            execution_id="EX0001",
            payload={"error": "Equipment failure"},
        )
        bus.publish(event)

        assert len(received) == 1
        assert received[0].event_id == "E0001"


class TestSimulator:
    """Simulator Test class"""

    def test_simulator_execute_dispatch(self):
        """Test the simulator to perform the dispatch operation"""
        sim = Simulator()

        # Perform berth skill inquiry
        result = sim.execute({
            "skill": "berth_scheduling",
            "action": "query_berth_status",
            "params": {"berth_id": "B01"}
        })
        assert result["status"] == "success"
        assert "data" in result
        assert "berth" in result["data"]

    def test_simulator_unknown_skill(self):
        """Test the simulator to deal with unknown skills"""
        sim = Simulator()

        result = sim.execute({
            "skill": "unknown_skill",
            "action": "some_action",
            "params": {}
        })
        assert result["status"] == "error"
        assert "Unknown skills" in result["error"]

    def test_simulator_berth_query_vessel(self):
        """Test berth skills to query ships"""
        sim = Simulator()

        result = sim.execute({
            "skill": "berth_scheduling",
            "action": "query_vessel_plan",
            "params": {"vessel_id": "V001"}
        })
        assert result["status"] == "success"

    def test_simulator_yard_query_status(self):
        """Test the query status of the storage field skills"""
        sim = Simulator()

        result = sim.execute({
            "skill": "yard_scheduling",
            "action": "query_yard_status",
            "params": {"block_id": "A01"}
        })
        assert result["status"] == "success"
        assert "data" in result
        assert "block" in result["data"]

    def test_simulator_equipment_query_status(self):
        """Test equipment skill query status"""
        sim = Simulator()

        result = sim.execute({
            "skill": "equipment_scheduling",
            "action": "query_equipment_status",
            "params": {"equipment_id": "QC01"}
        })
        assert result["status"] == "success"

    def test_simulator_gate_query_status(self):
        """Test the query status of gate skills"""
        sim = Simulator()

        result = sim.execute({
            "skill": "gate_scheduling",
            "action": "query_gate_status",
            "params": {}
        })
        assert result["status"] == "success"

    def test_simulator_with_session_id(self):
        """Test the execution with session_id"""
        sim = Simulator()

        result = sim.execute({
            "skill": "berth_scheduling",
            "action": "query_berth_status",
            "params": {"berth_id": "B01"},
            "session_id": "session_001"
        })
        assert result["status"] == "success"

    def test_simulator_unknown_action(self):
        """Test the simulator to handle unknown operations"""
        sim = Simulator()

        result = sim.execute({
            "skill": "berth_scheduling",
            "action": "unknown_action",
            "params": {}
        })
        assert result["status"] == "error"
