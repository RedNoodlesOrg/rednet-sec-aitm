from __future__ import annotations

import unittest

from aitm.events.credentials_captured_event import CredentialsCapturedEvent
from simple_observer.event import Event


class TestCredentialsCapturedEvent(unittest.TestCase):

    def test_event_inheritance(self):
        event = CredentialsCapturedEvent("test_user", "test_password")
        self.assertIsInstance(event, Event)

    def test_event_attributes(self):
        username = "test_user"
        password = "test_password"
        event = CredentialsCapturedEvent(username, password)
        self.assertEqual(event.username, username)
        self.assertEqual(event.password, password)

    def test_event_string_representation(self):
        username = "test_user"
        password = "test_password"
        event = CredentialsCapturedEvent(username, password)
        expected_string = f"Credentials captured with username: {username} and password: {password}"
        self.assertEqual(str(event), expected_string)


if __name__ == "__main__":
    unittest.main()
