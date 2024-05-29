from __future__ import annotations

import unittest
from unittest.mock import patch

from mitmproxy.test.tflow import tflow

from aitm.proxy.upstream_addon import UpstreamAddon, proxy_port
from aitm.proxy.utils.config import Config

mock_config = Config(local_upstream_hostname="localhost", local_upstream_scheme="http")
mock_config.targets = [
    {"origin": "example.com", "proxy": "proxy.example.com", "port": 8080},
    {"origin": "another.com", "proxy": "proxy.another.com", "port": None},
]


class TestUpstreamAddon(unittest.TestCase):

    def setUp(self):
        self.patcher = patch("aitm.proxy.upstream_addon.get_config", return_value=mock_config)
        self.mock_get_config = self.patcher.start()
        self.addon = UpstreamAddon()

    def tearDown(self):
        self.patcher.stop()

    def mock_flow_factory(self, host="proxy.example.com"):
        flow = tflow()
        flow.request.host = host
        flow.request.port = 443
        flow.request.scheme = "https"
        return flow

    def test_request_sets_upstream_port(self):
        mock_flow = self.mock_flow_factory(host="proxy.example.com")
        self.addon.request(mock_flow)
        self.assertEqual(mock_flow.server_conn.via[1], (mock_config.local_upstream_hostname, 8080))
        self.assertEqual(mock_flow.request.host, mock_config.local_upstream_hostname)
        self.assertEqual(mock_flow.request.port, 8080)
        self.assertEqual(mock_flow.request.scheme, mock_config.local_upstream_scheme)

    def test_request_with_non_target_proxy(self):
        mock_flow = self.mock_flow_factory(host="non.target.proxy")
        self.addon.request(mock_flow)
        self.assertIsNone(mock_flow.server_conn.via)  # No change expected

    def test_request_with_non_target_port(self):
        mock_flow = self.mock_flow_factory(host="proxy.another.com")
        self.addon.request(mock_flow)
        self.assertIsNone(mock_flow.server_conn.via)  # No change expected

    def test_proxy_port(self):
        mock_flow = self.mock_flow_factory(host="proxy.invalid.com")
        self.assertIsNone(proxy_port(mock_flow))
        mock_flow = self.mock_flow_factory(host="proxy.example.com")
        self.assertEqual(proxy_port(mock_flow), 8080)


if __name__ == "__main__":
    unittest.main()
