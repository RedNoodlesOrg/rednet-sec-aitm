"""Tests for cookies"""

from __future__ import annotations

from http.cookies import SimpleCookie
from unittest.mock import patch

import pytest

from aitm.helpers.config import Config
from aitm.helpers.cookies import parse_cookies  # Adjust the import as necessary

# Mocking config for our tests
mock_config = Config()
mock_config.targets = [
    {"origin": "example.com", "proxy": "proxy.example.com"},
    {"origin": "another.com", "proxy": "proxy.another.com"},
]


@pytest.fixture
def cookie_input():
    cookie = SimpleCookie()
    cookie["session"] = "sessionid123"
    cookie["session"]["domain"] = "proxy.example.com"
    cookie["pref"] = "user_pref"
    cookie["pref"]["domain"] = "proxy.another.com"
    return cookie


@patch("aitm.helpers.cookies.config", mock_config)
def test_parse_cookies(cookie_input):
    """Test parsing of cookies with domain replacements."""
    parsed_cookies = parse_cookies(cookie_input)

    assert len(parsed_cookies) == 2  # Ensure two cookies are parsed

    # Check session cookie parsing and domain modification
    session_cookie = next((c for c in parsed_cookies if c["name"] == "session"), None)
    assert session_cookie is not None
    assert session_cookie["value"] == "sessionid123"
    assert session_cookie["domain"] == "example.com"

    # Check pref cookie parsing and domain modification
    pref_cookie = next((c for c in parsed_cookies if c["name"] == "pref"), None)
    assert pref_cookie is not None
    assert pref_cookie["value"] == "user_pref"
    assert pref_cookie["domain"] == "another.com"


def test_parse_cookies_no_domain(cookie_input):
    """Test parsing of cookies without domain replacements."""
    # Remove domain from input cookies to test cookies without domain attribute
    del cookie_input["session"]["domain"]
    del cookie_input["pref"]["domain"]

    with patch("aitm.helpers.config.Config", mock_config):
        parsed_cookies = parse_cookies(cookie_input)

    assert len(parsed_cookies) == 2  # Ensure two cookies are parsed

    # Verify that cookies without domain attributes are parsed correctly
    for cookie in parsed_cookies:
        assert "domain" not in cookie
