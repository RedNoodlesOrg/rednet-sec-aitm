from __future__ import annotations

from simple_observer.event import Event


class MfaMethodRegisteredEvent(Event):
    """
    Represents an event when an MFA method is registered.

    Attributes:
        method (str): The registered MFA method.
    """

    def __init__(self, secret_key: str | None, success: bool):
        super().__init__("MfaMethodRegistered", {"secret_key": secret_key, "success": success})
        self.secret_key = secret_key
        self.success = success

    def __str__(self) -> str:
        if self.success:
            return f"MFA method registered: {self.secret_key}"
        return "MFA method registration failed"
