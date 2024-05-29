"""Tests for requests"""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from mitmproxy.test.tutils import treq

from aitm.proxy.utils.config import Config
from aitm.proxy.utils.requests import modify_header, modify_host, modify_query

mock_config = Config()
mock_config.targets = [
    {"origin": "example.com", "proxy": "proxy.example.com", "port": 80},
    {"origin": "another.com", "proxy": "proxy.another.com", "port": 443},
]


class TestRequests(unittest.TestCase):

    def setUp(self):
        self.mock_flow = MagicMock()
        self.mock_flow.request = treq()

    def test_modify_header(self):
        with patch("aitm.proxy.utils.requests.get_config", return_value=mock_config):
            self.mock_flow.request.headers = {"User-Agent": "agent", "Host": "proxy.example.com"}
            modify_header(self.mock_flow, "User-Agent")
            self.assertEqual(self.mock_flow.request.headers["User-Agent"], "agent")
            modify_header(self.mock_flow, "Host")
            self.assertEqual(self.mock_flow.request.headers["Host"], "example.com")
            modify_header(self.mock_flow, "not_exist")

    def test_modify_query(self):
        with patch("aitm.proxy.utils.requests.get_config", return_value=mock_config):
            self.mock_flow.request.query = {"key": "value", "redirect": "proxy.example.com"}
            modify_query(self.mock_flow, "redirect")
            self.assertEqual(self.mock_flow.request.query["redirect"], "example.com")
            modify_query(self.mock_flow, "not_exist")

    def test_modify_host_port(self):
        with patch("aitm.proxy.utils.requests.get_config", return_value=mock_config):
            self.mock_flow.request.headers = {"Host": "local.fsoc.bid:443"}
            modify_host(self.mock_flow)
            self.assertEqual(self.mock_flow.request.headers["Host"], "another.com")
            self.mock_flow.request.headers = {"Host": "invalid.host.bid:443"}
            modify_host(self.mock_flow)
            self.assertEqual(self.mock_flow.request.headers.get("Host"), "invalid.host.bid:443")

    def test_modify_host(self):
        with patch("aitm.proxy.utils.requests.get_config", return_value=mock_config):
            self.mock_flow.request.headers = {"Host": "proxy.example.com"}
            modify_host(self.mock_flow)
            self.assertEqual(self.mock_flow.request.headers["Host"], "example.com")
            self.mock_flow.request.headers = {}
            modify_host(self.mock_flow)


if __name__ == "__main__":
    unittest.main()
