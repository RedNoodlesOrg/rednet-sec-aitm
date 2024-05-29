from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from aitm.oauth2.state_machine import StateMachine as RegistrationStateMachine


class TestRegistrationStateMachine(unittest.TestCase):

    def setUp(self):
        self.state_machine = RegistrationStateMachine()

    @patch(
        "aitm.oauth2.state_machine.simple_state_machine.add_security_info",
        return_value={"VerificationContext": "verification_context"},
    )
    @patch("aitm.oauth2.state_machine.simple_state_machine.authorize_mobileapp", return_value="session_ctx")
    @patch(
        "aitm.oauth2.state_machine.simple_state_machine.initialize_mobileapp_registration",
        return_value={"SecretKey": "5jm2hkk5jfn7s6dj"},
    )
    @patch("aitm.oauth2.state_machine.simple_state_machine.prepare_session", return_value="session")
    @patch("aitm.oauth2.state_machine.simple_state_machine.verify_security_info", return_value="")
    def test_state_machine(
        self,
        mock_verify_security_info: MagicMock,
        mock_prepare_session: MagicMock,
        mock_initialize_mobileapp_registration: MagicMock,
        mock_authorize_mobileapp: MagicMock,
        mock_add_security_info: MagicMock,
    ):
        assert self.state_machine.state == self.state_machine.States.IDLE

        self.state_machine.start("cookies", "user_agent")
        self.assertEqual(self.state_machine.state, self.state_machine.States.IDLE)
        mock_verify_security_info.assert_called_once()
        mock_prepare_session.assert_called_once()
        mock_initialize_mobileapp_registration.assert_called_once()
        mock_authorize_mobileapp.assert_called_once()
        mock_add_security_info.assert_called_once()


if __name__ == "__main__":
    unittest.main()
