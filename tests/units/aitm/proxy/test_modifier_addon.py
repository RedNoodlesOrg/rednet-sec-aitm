from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from mitmproxy.test.tflow import tflow
from mitmproxy.test.tutils import treq

from aitm.proxy.modifier_addon import ModifierAddon
from aitm.proxy.utils.config import Config

mock_config = Config(
    mfa_claim="mock_mfa_claim", auth_url=["/mock/auth/url"], local_upstream_hostname="local.upstream.host"
)
mock_config.targets = [{"origin": "example.com", "proxy": "proxy.example.com"}]


class TestModifierAddon(unittest.TestCase):

    @patch("aitm.proxy.modifier_addon.requests.modify_header")
    @patch("aitm.proxy.modifier_addon.requests.modify_query")
    @patch("aitm.proxy.modifier_addon.get_config", return_value=mock_config)
    @patch("aitm.proxy.modifier_addon.ModifierAddon.event_emitter")
    def setUp(
        self,
        mock_event_emitter: MagicMock,
        mock_get_config: MagicMock,
        mock_modify_query: MagicMock,
        mock_modify_header: MagicMock,
    ):
        self.addon = ModifierAddon()
        self.addon.state_machine = MagicMock()
        self.addon.event_emitter = mock_event_emitter
        self.mock_flow_request = tflow(req=treq())
        self.mock_flow_request.request.urlencoded_form = {"login": "user", "passwd": "pass"}
        self.mock_flow_response = tflow(req=treq(), resp=True)

    def tearDown(self):
        super().tearDown()

    @patch("aitm.proxy.modifier_addon.requests.modify_header")
    @patch("aitm.proxy.modifier_addon.requests.modify_query")
    @patch("aitm.proxy.modifier_addon.get_config", return_value=mock_config)
    @patch("aitm.proxy.modifier_addon.ModifierAddon.event_emitter")
    def test_upstream_hostname(
        self,
        mock_event_emitter: MagicMock,
        mock_get_config: MagicMock,
        mock_modify_query: MagicMock,
        mock_modify_header: MagicMock,
    ):
        self.mock_flow_request.request.host = "local.upstream.host"
        self.addon.request(self.mock_flow_request)
        mock_get_config.assert_called_once()
        mock_event_emitter.assert_not_called()
        mock_modify_header.assert_not_called()
        mock_modify_query.assert_not_called()

    @patch("aitm.proxy.modifier_addon.requests.modify_header")
    @patch("aitm.proxy.modifier_addon.requests.modify_query")
    @patch("aitm.proxy.modifier_addon.get_config", return_value=mock_config)
    @patch("aitm.proxy.modifier_addon.ModifierAddon.event_emitter")
    def test_request_host_header(
        self,
        mock_event_emitter: MagicMock,
        mock_get_config: MagicMock,
        mock_modify_query: MagicMock,
        mock_modify_header: MagicMock,
    ):
        self.addon.event_emitter = mock_event_emitter
        self.mock_flow_request.request.host = "proxy.example.com"
        self.mock_flow_request.request.path = "/common/oauth2/v2.0/authorize"
        self.addon.request(self.mock_flow_request)
        self.mock_flow_request.request.path = "/common/login"
        self.addon.request(self.mock_flow_request)
        self.addon.event_emitter.method_calls[0][1][0].password = "pass"
        self.addon.event_emitter.method_calls[0][1][0].username = "user"

    @patch("aitm.proxy.modifier_addon.cookies.parse_cookies")
    @patch("aitm.proxy.modifier_addon.responses.modify_header")
    @patch("aitm.proxy.modifier_addon.responses.modify_cookies")
    @patch("aitm.proxy.modifier_addon.responses.modify_content")
    @patch("aitm.proxy.modifier_addon.get_config", return_value=mock_config)
    @patch("aitm.proxy.modifier_addon.ModifierAddon.event_emitter")
    def test_valid_response(
        self,
        mock_event_emitter: MagicMock,
        mock_get_config: MagicMock,
        mock_modify_content: MagicMock,
        mock_modify_cookies: MagicMock,
        mock_modify_header: MagicMock,
        mock_parse_cookies: MagicMock,
    ):
        self.addon.event_emitter = mock_event_emitter
        self.mock_flow_response.request.host = "proxy.example.com"
        self.mock_flow_response.request.path = "/mock/auth/url"
        self.mock_flow_response.request.headers["User-Agent"] = "mock_user_agent"
        self.addon.response(self.mock_flow_response)
        mock_parse_cookies.assert_called_once()
        mock_modify_header.assert_called_once()
        mock_modify_cookies.assert_called_once()
        mock_modify_content.assert_called_once()

        mock_event_emitter.method_calls[0][1][0].user_agent = "mock_user_agent"
        mock_event_emitter.method_calls[0][1][0].parsed_cookies = mock_parse_cookies.return_value

        mock_parse_cookies.reset_mock()
        mock_modify_header.reset_mock()
        mock_modify_cookies.reset_mock()
        mock_modify_content.reset_mock()
        mock_event_emitter.reset_mock()
        self.mock_flow_response.request.path = "/path"
        self.addon.response(self.mock_flow_response)
        mock_parse_cookies.assert_not_called()
        mock_modify_header.assert_called_once()
        mock_modify_cookies.assert_called_once()
        mock_modify_content.assert_called_once()
        mock_event_emitter.assert_not_called()


if __name__ == "__main__":
    unittest.main()
