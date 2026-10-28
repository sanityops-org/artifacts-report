"""
Time controller module

It provides simulated time management functions to support initialization, query, promotion and setting time.
"""

from datetime import datetime, timedelta


class TimeController:
    """
    Time controller

    Manage the time in the simulation environment, and support time advancement and setting operations.

    Attributes:
        _current_time: Current simulation time (datetime object)
    """

    def __init__(self, initial_time: str = None):
        """
        Initialize the time controller

        Args:
            initial_time: Initial time (ISO format string), default to the current time
        """
        if initial_time:
            self._current_time = datetime.fromisoformat(initial_time)
        else:
            # The current time is used by default, accurate to the minute.
            self._current_time = datetime.now().replace(second=0, microsecond=0)

    def get_time(self) -> str:
        """
        Get the current simulation time

        Returns:
            str: Current simulation time (ISO format string, excluding seconds)
        """
        return self._current_time.strftime("%Y-%m-%dT%H:%M")

    def advance(self, minutes: int) -> str:
        """
        Time to advance

        Args:
            minutes: The number of minutes of promotion

        Returns:
            str: Time after promotion (ISO format string)
        """
        self._current_time += timedelta(minutes=minutes)
        return self.get_time()

    def set_time(self, time_str: str) -> None:
        """
        Set the time

        Args:
            time_str: Time to be set (ISO format string)
        """
        self._current_time = datetime.fromisoformat(time_str)


__all__ = ["TimeController"]
