from __future__ import annotations

from datetime import datetime


class Event:
    """
    Represents an event in the system.

    Attributes:
        event_type (str): The type of the event.
        data (Any): Optional data associated with the event.
    """

    __slots__ = ["event_type", "data", "timestamp"]

    def __init__(self, event_type, data=None):
        self.event_type = event_type
        self.data = data
        self.timestamp = datetime.now()

    def __str__(self) -> str:
        return f"[{self.timestamp.strftime('%d/%b/%Y %H:%M:%S')}] Event type: {self.event_type}, data: {self.data}"

    def to_dict(self) -> dict:
        return {
            "event_type": self.event_type,
            "data": self.data,
            "timestamp": self.timestamp.strftime("%d/%b/%Y %H:%M:%S"),
        }
