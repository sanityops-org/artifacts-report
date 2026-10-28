"""
Event bus module

Provide an event release subscription mechanism to simulate event notifications during execution.
"""

from datetime import datetime
from typing import Callable, Dict, List
from uuid import uuid4

from models.enums import EventType
from models.execution import FeedbackEvent


class EventBus:
    """
    Event bus

    Implement the release subscription mode and support the subscription and release of events.

    Attributes:
        _subscribers: Mapping of event type to subscriber list
    """

    def __init__(self):
        """Initialize the event bus"""
        self._subscribers: Dict[EventType, List[Callable]] = {}

    def subscribe(self, event_type: EventType, callback: Callable) -> None:
        """
        Subscription event

        Args:
            event_type: The type of event to subscribe
            callback: Event callback function, receive FeedbackEvent parameters
        """
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def publish(self, event: FeedbackEvent) -> None:
        """
        Release events

        Args:
            event: The event object to be published
        """
        callbacks = self._subscribers.get(event.event_type, [])
        for callback in callbacks:
            callback(event)

    def emit(
        self,
        event_type: EventType,
        payload: dict,
        execution_id: str = None
    ) -> FeedbackEvent:
        """
        Generate and publish events

        Args:
            event_type: Type of event
            payload: Event load data
            execution_id: Associated execution ID, optional

        Returns:
            FeedbackEvent: Generated event objects
        """
        # Generate eventsID
        event_id = f"E{uuid4().hex[:8].upper()}"

        # Generate a time stamp
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        # Create an event
        event = FeedbackEvent(
            event_id=event_id,
            event_type=event_type,
            timestamp=timestamp,
            execution_id=execution_id,
            payload=payload,
        )

        # Release events
        self.publish(event)

        return event


__all__ = ["EventBus"]
