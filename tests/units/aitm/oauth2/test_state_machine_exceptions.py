from __future__ import annotations

import unittest
from unittest.mock import patch

from aitm.oauth2.state_machine import StateMachine as SimpleStateMachine


class TestSimpleStateMachine(unittest.TestCase):

    def setUp(self):
        self.state_machine = SimpleStateMachine()
        self.state_machine.state = self.state_machine.States.VERIFYING_INFO

    def test_on_session_captured_exception(self):
        with patch(
            "aitm.oauth2.state_machine.simple_state_machine.prepare_session",
            side_effect=Exception("Session preparation failed"),
        ):
            self.state_machine.on_session_captured([], "User Agent")
            self.assertEqual(self.state_machine.state, self.state_machine.States.IDLE)

    def test_on_session_prepared_exception(self):
        with patch(
            "aitm.oauth2.state_machine.simple_state_machine.authorize_mobileapp",
            side_effect=Exception("Authorization failed"),
        ):
            self.state_machine.on_session_prepared()
            self.assertEqual(self.state_machine.state, self.state_machine.States.IDLE)

    def test_on_registration_authorized_exception(self):
        with patch(
            "aitm.oauth2.state_machine.simple_state_machine.initialize_mobileapp_registration",
            side_effect=Exception("Registration initialization failed"),
        ):
            self.state_machine.on_registration_authorized()
            self.assertEqual(self.state_machine.state, self.state_machine.States.IDLE)

    def test_on_registration_initialized_exception(self):
        with patch(
            "aitm.oauth2.state_machine.simple_state_machine.add_security_info",
            side_effect=Exception("Adding security info failed"),
        ):
            self.state_machine.on_registration_initialized()
            self.assertEqual(self.state_machine.state, self.state_machine.States.IDLE)

    def test_on_info_added_exception(self):
        with patch(
            "aitm.oauth2.state_machine.simple_state_machine.verify_security_info",
            side_effect=Exception("Verification failed"),
        ):
            self.state_machine.on_info_added("Verification Context", "OTP Code")
            self.assertEqual(self.state_machine.state, self.state_machine.States.IDLE)

    def test_on_exception_raised(self):
        exception = Exception("Custom exception")
        self.state_machine.on_exception_raised(exception)
        self.assertEqual(self.state_machine.state, self.state_machine.States.IDLE)

    def test_on_event_emitted(self):
        self.state_machine.on_event_emitted()
        self.assertEqual(self.state_machine.state, self.state_machine.States.IDLE)
        self.assertIsNone(self.state_machine._session)
        self.assertIsNone(self.state_machine._secret_key)
        self.assertIsNone(self.state_machine._session_ctx)


if __name__ == "__main__":
    unittest.main()
