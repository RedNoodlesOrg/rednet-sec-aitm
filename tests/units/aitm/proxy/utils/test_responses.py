"""Tests for responses"""

from __future__ import annotations

import unittest
from http.cookies import SimpleCookie
from unittest.mock import MagicMock, patch

from mitmproxy import http
from mitmproxy.test.tutils import tresp

from aitm.proxy.utils.config import Config
from aitm.proxy.utils.responses import (
    modify_content,
    modify_cookies,
    modify_header,
    save_cookies,
)

mock_config = Config(
    content_types=["text/html", "application/json"],
    custom_modifications=[
        {
            "mimes": ["application/json"],
            "sites": ["example.com"],
            "search": "example",
            "replace": "sample",
        },
    ],
)
mock_config.targets = [
    {"origin": "example.com", "proxy": "proxy.example.com"},
    {"origin": "another.com", "proxy": "proxy.another.com"},
]


class TestResponses(unittest.TestCase):

    def setUp(self):
        self.patcher = patch("aitm.proxy.utils.responses.get_config", return_value=mock_config)
        self.mock_get_config = self.patcher.start()

        self.mock_flow = MagicMock()
        headers = http.Headers(
            (
                (b"header-response", b"svalue"),
                (b"content-length", b"7"),
                (b"Content-Type", b"text/html"),
                (b"set-cookie", b"session=abcd; Domain=example.com"),
                (b"Location", b"example.com"),
            )
        )
        self.mock_flow.response = tresp(headers=headers)
        self.mock_flow.response.text = "Response from https://example.com with session=abcd"
        self.mock_flow.server_conn = MagicMock()
        self.mock_flow.server_conn.address = ("example.com", 80)

    def tearDown(self):
        self.patcher.stop()

    def test_invalid_flow(self):
        self.mock_flow.response = None
        self.mock_flow.server_conn = None
        simple_cookie = SimpleCookie()
        self.assertFalse(save_cookies(self.mock_flow, simple_cookie))
        self.assertFalse(modify_header(self.mock_flow, "Location"))
        self.assertFalse(modify_content(self.mock_flow))
        self.assertFalse(modify_cookies(self.mock_flow))

    def test_modify_header(self):
        modify_header(self.mock_flow, "Location")
        modify_header(self.mock_flow, "not_exist")
        self.assertEqual(self.mock_flow.response.headers["Location"], "proxy.example.com")

    def test_modify_content(self):
        self.mock_flow.response.headers["Content-Type"] = "application/json"
        modify_content(self.mock_flow)
        self.assertIn("Response from https://proxy.sample.com with session=abcd", self.mock_flow.response.text)
        self.mock_flow.response.headers = {}
        modify_content(self.mock_flow)

    def test_modify_cookies(self):
        modify_cookies(self.mock_flow)
        self.assertTrue(
            any(
                "Domain=proxy.example.com" in cookie for cookie in self.mock_flow.response.headers.get_all("set-cookie")
            )
        )
        self.mock_flow.response.headers = http.Headers()
        modify_cookies(self.mock_flow)

    def test_save_cookies(self):
        simple_cookie = SimpleCookie()
        save_cookies(self.mock_flow, simple_cookie)
        self.assertIn("session", simple_cookie)


if __name__ == "__main__":
    unittest.main()
