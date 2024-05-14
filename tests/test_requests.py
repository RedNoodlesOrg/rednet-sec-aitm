"""Tests for requests"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from mitmproxy.test.tutils import treq

from aitm.helpers.config import Config
from aitm.helpers.requests import (  # Adjust the import as necessary
    modify_header,
    modify_host,
    modify_query,
)

# Mock configuration
mock_config = Config()
mock_config.targets = [
    {"origin": "example.com", "proxy": "proxy.example.com", "port": 80},
    {"origin": "another.com", "proxy": "proxy.another.com", "port": 443},
]


@pytest.fixture
def mock_flow():
    flow = MagicMock()
    flow.request = treq()
    return flow


@patch("aitm.helpers.requests.config", mock_config)
def test_modify_header(mock_flow):
    mock_flow.request.headers = {"User-Agent": "agent", "Host": "proxy.example.com"}
    modify_header(mock_flow, "User-Agent")
    assert mock_flow.request.headers["User-Agent"] == "agent"
    modify_header(mock_flow, "Host")
    assert mock_flow.request.headers["Host"] == "example.com"


@patch("aitm.helpers.requests.config", mock_config)
def test_modify_query(mock_flow):
    mock_flow.request.query = {"key": "value", "redirect": "proxy.example.com"}
    modify_query(mock_flow, "redirect")
    assert mock_flow.request.query["redirect"] == "example.com"


@patch("aitm.helpers.requests.config", mock_config)
def test_modify_host_port(mock_flow):
    mock_flow.request.headers = {"Host": "local.fsoc.bid:443"}
    modify_host(mock_flow)
    assert mock_flow.request.headers["Host"] == "another.com"


@patch("aitm.helpers.requests.config", mock_config)
def test_modify_host(mock_flow):
    mock_flow.request.headers = {"Host": "proxy.example.com"}
    modify_host(mock_flow)
    assert mock_flow.request.headers["Host"] == "example.com"
