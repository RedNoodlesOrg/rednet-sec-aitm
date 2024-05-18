"""Tests for responses"""

from __future__ import annotations

from http.cookies import SimpleCookie
from unittest.mock import MagicMock, patch

import pytest
from mitmproxy import http
from mitmproxy.test.tutils import tresp

from aitm.helpers.config import Config
from aitm.helpers.responses import (modify_content, modify_cookies,
                                    modify_header, save_cookies)

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


@pytest.fixture
def mock_flow():
    flow = MagicMock()
    headers = http.Headers(
        (
            (b"header-response", b"svalue"),
            (b"content-length", b"7"),
            (b"Content-Type", b"text/html"),
            (b"set-cookie", b"session=abcd; Domain=example.com"),
            (b"Location", b"example.com"),
        )
    )
    flow.response = tresp(headers=headers)
    flow.response.text = "Response from https://example.com with session=abcd"
    flow.server_conn = MagicMock()
    flow.server_conn.address = ("example.com", 80)
    return flow


def test_invalid_flow(mock_flow):
    mock_flow.response = None
    mock_flow.server_conn = None
    simple_cookie = SimpleCookie()
    assert not save_cookies(mock_flow, simple_cookie)
    assert not modify_header(mock_flow, "Location")
    assert not modify_content(mock_flow)
    assert not modify_cookies(mock_flow)


@patch("aitm.helpers.responses.config", mock_config)
def test_modify_header(mock_flow):
    modify_header(mock_flow, "Location")
    assert mock_flow.response.headers["Location"] == "proxy.example.com"


@patch("aitm.helpers.responses.config", mock_config)
def test_modify_content(mock_flow):
    mock_flow.response.headers["Content-Type"] = "application/json"
    modify_content(mock_flow)
    assert "Response from https://proxy.sample.com with session=abcd" in mock_flow.response.text


@patch("aitm.helpers.responses.config", mock_config)
def test_modify_cookies(mock_flow):
    modify_cookies(mock_flow)
    assert any("Domain=proxy.example.com" in cookie for cookie in mock_flow.response.headers.get_all("set-cookie"))


@patch("aitm.helpers.responses.config", mock_config)
def test_save_cookies(mock_flow):
    simple_cookie = SimpleCookie()
    save_cookies(mock_flow, simple_cookie)
    assert "session" in simple_cookie
