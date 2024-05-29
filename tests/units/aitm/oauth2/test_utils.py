from __future__ import annotations

import base64
import json
import unittest
from unittest.mock import patch

import requests_mock
from requests import Session
from requests_oauthlib import OAuth2Session

from aitm.oauth2.config import AUTH_SCOPES, CLIENT_ID, REDIRECT_URI
from aitm.oauth2.utils import (
    create_oauth2_session,
    get_authorization_url,
    get_tenant_id,
    parse_garbage,
    send_request,
)


class TestOAuth2Utils(unittest.TestCase):

    @patch("aitm.oauth2.utils.OAuth2Session.authorization_url")
    def test_get_authorization_url(self, mock_auth_url):
        mock_auth_url.return_value = ("https://example.com/authorize?param1=test1&param2=test2", None)
        auth_session = OAuth2Session(
            client_id="test_client_id",
            scope=["scope1", "scope2"],
            redirect_uri="https://example.com/callback",
            pkce="S256",
        )
        base_url, params = get_authorization_url(auth_session)
        self.assertEqual(base_url, "https://example.com/authorize")
        self.assertIn("param1", params)
        self.assertEqual(params["param1"], ["test1"])
        self.assertIn("param2", params)
        self.assertEqual(params["param2"], ["test2"])

    def test_create_oauth2_session(self):
        session = Session()
        auth_session = create_oauth2_session(session)
        self.assertEqual(auth_session.client_id, CLIENT_ID)
        self.assertEqual(auth_session.scope, AUTH_SCOPES)
        self.assertEqual(auth_session.redirect_uri, REDIRECT_URI)
        self.assertEqual(auth_session._pkce, "S256")
        self.assertEqual(auth_session.cookies, session.cookies)
        self.assertEqual(auth_session.headers, session.headers)

    def test_get_tenant_id(self):
        access_token = {
            "aud": "https://webshell.suite.office.com",
            "acr": "1",
            "amr": ["pwd", "mfa"],
            "tid": "dummy_tenant_id",
        }
        access_token = json.dumps(access_token).encode("utf-8")
        access_token = base64.urlsafe_b64encode(access_token).decode("utf-8")
        session = OAuth2Session(token={"access_token": f".{access_token}."})
        tenant_id = get_tenant_id(session)
        self.assertEqual(tenant_id, "dummy_tenant_id")

    def test_parse_garbage(self):
        # Test case 1: Valid JSON response without garbage text
        data = '{"key": "value"}'
        result = parse_garbage(data)
        self.assertEqual(result, {"key": "value"})

        # Test case 2: Valid JSON response with garbage text
        data = ')]}\',\n{"key": "value"}'
        result = parse_garbage(data)
        self.assertEqual(result, {"key": "value"})

    def test_send_request(self):
        session = OAuth2Session(token={"access_token": "dummy_token"})
        url = "https://example.com/api"
        schema = {"type": "object", "properties": {"key": {"type": "string"}}}
        data = {"key": "value"}
        response = {"key": "value"}
        with requests_mock.Mocker() as m:
            m.post(url, json=response)
            result = send_request(session, url, schema, data)
            self.assertEqual(result, response)


if __name__ == "__main__":
    unittest.main()
