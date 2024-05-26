from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from aitm.msft_aama.state_machine import RegistrationStateMachine


@pytest.fixture
def state_machine():
    return RegistrationStateMachine()


@patch("aitm.msft_aama.state_machine.add_security_info", return_value={"VerificationContext": "verification_context"})
@patch("aitm.msft_aama.state_machine.authorize_mobileapp", return_value="session_ctx")
@patch("aitm.msft_aama.state_machine.initialize_mobileapp_registration", return_value={"SecretKey": "5jm2hkk5jfn7s6dj"})
@patch("aitm.msft_aama.state_machine.prepare_session", return_value="session")
@patch("aitm.msft_aama.state_machine.verify_security_info", return_value="")
def test(
    mock_verify_security_info: MagicMock,
    mock_prepare_session: MagicMock,
    mock_initialize_mobileapp_registration: MagicMock,
    mock_authorize_mobileapp: MagicMock,
    mock_add_security_info: MagicMock,
    state_machine: RegistrationStateMachine,
):
    assert state_machine.is_IDLE

    state_machine.session_captured("cookies", "user_agent")
    assert state_machine.is_IDLE
    mock_verify_security_info.assert_called_once
    mock_prepare_session.assert_called_once
    mock_initialize_mobileapp_registration.assert_called_once
    mock_authorize_mobileapp.assert_called_once
    mock_add_security_info.assert_called_once
