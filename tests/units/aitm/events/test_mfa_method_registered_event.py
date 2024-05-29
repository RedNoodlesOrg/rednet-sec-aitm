from __future__ import annotations

import unittest

from aitm.events.mfa_method_registered_event import MfaMethodRegisteredEvent
from simple_observer.event import Event


class TestMfaMethodRegisteredEvent(unittest.TestCase):

    def test_event_inheritance(self):
        self.assertTrue(issubclass(MfaMethodRegisteredEvent, Event))

    def test_event_attributes(self):
        secret_key = "123456"
        success = True
        event = MfaMethodRegisteredEvent(secret_key, success)
        self.assertEqual(event.secret_key, secret_key)
        self.assertEqual(event.success, success)

    def test_event_string_representation_success(self):
        secret_key = "123456"
        success = True
        event = MfaMethodRegisteredEvent(secret_key, success)
        expected_string = f"MFA method registered: {secret_key}"
        self.assertEqual(str(event), expected_string)

    def test_event_string_representation_failure(self):
        secret_key = None
        success = False
        event = MfaMethodRegisteredEvent(secret_key, success)
        expected_string = "MFA method registration failed"
        self.assertEqual(str(event), expected_string)


if __name__ == "__main__":
    unittest.main()
