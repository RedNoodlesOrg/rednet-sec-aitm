from __future__ import annotations


class Event:
    """
    Represents an event in the system.

    Attributes:
        event_type (str): The type of the event.
        data (Any): Optional data associated with the event.
    """

    __slots__ = ["event_type", "data"]

    def __init__(self, event_type, data=None):
        self.event_type = event_type
        self.data = data

    def __str__(self) -> str:
        return f"Event type: {self.event_type}, data: {self.data}"
