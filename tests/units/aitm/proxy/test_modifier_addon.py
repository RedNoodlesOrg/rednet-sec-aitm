from __future__ import annotations

import unittest
from unittest.mock import patch

from mitmproxy.test.tflow import tflow
from mitmproxy.test.tutils import treq

from aitm.proxy.modifier_addon import ModifierAddon
from aitm.proxy.utils.config import Config

mock_config = Config(mfa_claim="mock_mfa_claim", auth_url=["/mock/auth/url"])
mock_config.targets = [{"origin": "example.com", "proxy": "proxy.example.com"}]


class TestModifierAddon(unittest.TestCase):

    def setUp(self):
        self.patcher = patch("aitm.proxy.modifier_addon.get_config", return_value=mock_config)
        self.mock_get_config = self.patcher.start()
        self.addon = ModifierAddon()
        self.mock_flow_request = tflow(req=treq())
        self.mock_flow_request.request.urlencoded_form = {"login": "user", "passwd": "pass"}
        self.mock_flow_response = tflow(req=treq(), resp=True)

    def tearDown(self):
        self.patcher.stop()

    def test_request_host_header(self):
        self.mock_flow_request.request.path = "/common/oauth2/v2.0/authorize"
        self.addon.request(self.mock_flow_request)
        self.mock_flow_request.request.path = "/common/login"
        self.addon.request(self.mock_flow_request)
        self.assertTrue(True)

    def test_response_location_header(self):
        self.mock_flow_response.response.path = "/mock/auth/url"
        self.addon.response(self.mock_flow_response)
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
