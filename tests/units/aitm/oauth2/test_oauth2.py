from __future__ import annotations

import base64
import json
import unittest
from unittest.mock import MagicMock, patch

import requests_mock
from hypothesis import given
from hypothesis_jsonschema import from_schema
from requests import Session
from requests_oauthlib import OAuth2Session

from aitm.oauth2.config import (
    ADD_SECURITY_INFO_URL,
    AUTHORIZE_MOBILE_APP_URL,
    INITIALIZE_MOBILE_APP_URL,
    VERIFY_SECURITY_INFO_URL,
)
from aitm.oauth2.schemas import (
    ADD_SECURITY_INFO_SCHEMA,
    AUTHORIZE_MOBILE_APP_SCHEMA,
    INITIALIZE_MOBILE_APP_SCHEMA,
)
from aitm.oauth2.state_machine.actions import (
    add_security_info,
    authorize,
    authorize_mobileapp,
    initialize_mobileapp_registration,
    verify_security_info,
)
from aitm.oauth2.utils import get_tenant_id


class TestOAuth2Actions(unittest.TestCase):

    @patch("aitm.oauth2.state_machine.actions.create_oauth2_session")
    @patch("aitm.oauth2.state_machine.actions.get_authorization_url")
    @patch("aitm.oauth2.state_machine.actions.get_tenant_id")
    @patch("aitm.oauth2.state_machine.actions.OAuth2Session.fetch_token")
    @patch("aitm.oauth2.state_machine.actions.OAuth2Session.refresh_token")
    def test_authorize(
        self,
        mock_refresh_token,
        mock_fetch_token,
        mock_get_tenant_id,
        mock_get_authorization_url,
        mock_create_oauth2_session,
    ):
        session = Session()
        mock_create_oauth2_session.return_value = OAuth2Session()
        mock_get_authorization_url.return_value = ("https://example.com/authorize", {})
        mock_get_tenant_id.return_value = "dummy_tenant_id"
        mock_fetch_token.return_value = {
            "access_token": "dummy_access_token",
            "refresh_token": "dummy_refresh_token",
        }
        mock_refresh_token.return_value = {
            "access_token": "dummy_access_token",
            "refresh_token": "dummy_refresh_token",
        }

        result = authorize(session)

        self.assertIsInstance(result, OAuth2Session)
        mock_create_oauth2_session.assert_called_once_with(session)
        mock_get_authorization_url.assert_called_once_with(mock_create_oauth2_session.return_value)
        mock_get_tenant_id.assert_called_once_with(mock_create_oauth2_session.return_value)

    def test_get_tenant_id(self):
        session = MagicMock()
        tid = "12345678-1234-1234-1234-123456789abc"
        access_token_s1 = {
            "aud": "https://webshell.suite.office.com",
            "acr": "1",
            "amr": ["pwd", "mfa"],
            "tid": tid,
            "xms_tdbr": "EU",
        }
        access_token_s1 = json.dumps(access_token_s1).encode("utf-8")
        access_token_s1 = base64.urlsafe_b64encode(access_token_s1).decode("utf-8")
        access_token_s1 = access_token_s1.rstrip("=")
        access_token = f"eyJhbGciOi.{access_token_s1}.SflKxw"
        session.token = {"access_token": access_token}
        tenant_id = get_tenant_id(session)
        self.assertEqual(tenant_id, tid)

    @given(from_schema(AUTHORIZE_MOBILE_APP_SCHEMA))
    def test_authorize_mobileapp(self, mock_response):
        session, ctx = MagicMock(), "test_session_ctx"

        with requests_mock.mock() as m:
            mock_response.update(
                {
                    "isAuthorized": True,
                    "sessionCtx": ctx,
                }
            )
            post_adapter = m.post(AUTHORIZE_MOBILE_APP_URL, json=mock_response)

            response = authorize_mobileapp(session)

            self.assertEqual(response, "test_session_ctx")
            self.assertTrue(post_adapter.called)

    def test_verify_security_info(self):
        session, ctx = MagicMock(), "test_session_ctx"
        verification_context = "test_verification_context"
        otp_code = "123456"
        mock_response = {"Type": 3, "VerificationState": 2, "ErrorCode": 0}
        mock_response_text = ")]}',\n" + json.dumps({"Type": 3, "VerificationState": 2, "ErrorCode": 0})
        with requests_mock.mock() as m:
            post_adapter = m.post(VERIFY_SECURITY_INFO_URL, text=mock_response_text)

            response = verify_security_info(session, verification_context, otp_code, ctx)

            self.assertEqual(response, mock_response)
            self.assertTrue(post_adapter.called)
            self.assertEqual(
                post_adapter.last_request.json(),
                {
                    "Type": 3,
                    "VerificationContext": verification_context,
                    "VerificationData": otp_code,
                },
            )

    @given(from_schema(ADD_SECURITY_INFO_SCHEMA))
    def test_add_security_info(self, mock_response):
        session, ctx = MagicMock(), "test_session_ctx"
        secret_key = "test_secret_key"

        with requests_mock.Mocker() as m:
            mock_response.update({"Type": 3, "VerificationState": 1, "ErrorCode": 0})
            post_adapter = m.post(ADD_SECURITY_INFO_URL, json=mock_response)

            response = add_security_info(session, secret_key, ctx)

            self.assertEqual(response, mock_response)
            self.assertTrue(post_adapter.called)
            self.assertEqual(
                post_adapter.last_request.json(),
                {
                    "Type": 3,
                    "Data": json.dumps(
                        {
                            "secretKey": secret_key,
                            "affinityRegion": None,
                            "isResendNotificationChallenge": False,
                        }
                    ),
                },
            )

    @given(from_schema(INITIALIZE_MOBILE_APP_SCHEMA))
    def test_initialize_mobileapp_registration(self, mock_response):
        session, ctx = MagicMock(), "test_session_ctx"

        with requests_mock.Mocker() as m:
            mock_response.update({"RegistrationType": 3})
            post_adapter = m.post(INITIALIZE_MOBILE_APP_URL, json=mock_response)

            response = initialize_mobileapp_registration(session, ctx)

            self.assertEqual(response, mock_response)
            self.assertEqual(response["RegistrationType"], 3)
            self.assertTrue(post_adapter.called)
            self.assertEqual(post_adapter.last_request.json(), {"securityInfoType": 3})


if __name__ == "__main__":
    unittest.main()
