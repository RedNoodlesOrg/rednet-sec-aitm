"""Tests for cookies"""

from __future__ import annotations

import unittest
from http.cookies import SimpleCookie
from unittest.mock import patch

from aitm.proxy.utils.config import Config
from aitm.proxy.utils.cookies import parse_cookies

mock_config = Config()
mock_config.targets = [
    {"origin": "example.com", "proxy": "proxy.example.com"},
    {"origin": "another.com", "proxy": "proxy.another.com"},
]


class TestCookies(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.cookie_input = SimpleCookie()
        self.cookie_input["session"] = "sessionid123"
        self.cookie_input["session"]["domain"] = "proxy.example.com"
        self.cookie_input["pref"] = "user_pref"
        self.cookie_input["pref"]["domain"] = "proxy.another.com"

    def tearDown(self) -> None:
        return super().tearDown()

    @patch("aitm.proxy.utils.cookies.get_config", return_value=mock_config)
    def test_parse_cookies(self, mock_get_config):
        """Test parsing of cookies with domain replacements."""
        parsed_cookies = parse_cookies(self.cookie_input)

        assert len(parsed_cookies) == 2

        session_cookie = next((c for c in parsed_cookies if c["name"] == "session"), None)
        assert session_cookie is not None
        assert session_cookie["value"] == "sessionid123"
        assert session_cookie["domain"] == "example.com"

        pref_cookie = next((c for c in parsed_cookies if c["name"] == "pref"), None)
        assert pref_cookie is not None
        assert pref_cookie["value"] == "user_pref"
        assert pref_cookie["domain"] == "another.com"

    def test_parse_cookies_no_domain(self):
        """Test parsing of cookies without domain replacements."""
        del self.cookie_input["session"]["domain"]
        del self.cookie_input["pref"]["domain"]

        with patch("aitm.proxy.utils.cookies.get_config", return_value=mock_config):
            parsed_cookies = parse_cookies(self.cookie_input)

        assert len(parsed_cookies) == 2  # Ensure two cookies are parsed

        for cookie in parsed_cookies:
            assert "domain" not in cookie


if __name__ == "__main__":
    unittest.main()
