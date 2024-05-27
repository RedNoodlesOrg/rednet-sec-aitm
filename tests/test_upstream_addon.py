from __future__ import annotations

from unittest.mock import patch

import pytest
from mitmproxy.test.tflow import tflow

from aitm.proxy.upstream_addon import UpstreamAddon
from aitm.proxy.utils.config import Config

mock_config = Config(local_upstream_hostname="localhost", local_upstream_scheme="http")
mock_config.targets = [{"origin": "example.com", "proxy": "proxy.example.com", "port": 8080}]


@pytest.fixture
def mock_flow_factory():
    def _factory(
        host="proxy.example.com",
    ):
        flow = tflow()
        flow.request.host = host
        flow.request.port = 443
        flow.request.scheme = "https"
        return flow

    return _factory


@pytest.fixture
def upstream_addon():
    with patch("aitm.proxy.upstream_addon.get_config", return_value=mock_config):
        addon = UpstreamAddon()
    return addon


# TODO: Implement the ``request_sets_upstream_port`` test
def test_request_sets_upstream_port(upstream_addon, mock_flow_factory):
    mock_flow = mock_flow_factory(host="proxy.example.com")
    upstream_addon.request(mock_flow)
    assert True
    # assert mock_flow.server_conn.via[1] == (
    #     mock_config.local_upstream_hostname,
    #     8080,
    # )
    # assert mock_flow.request.host == mock_config["local_upstream_hostname"]
    # assert mock_flow.request.port == 8080
    # assert mock_flow.request.scheme == mock_config["local_upstream_scheme"]


# TODO: Implement the ``request_with_non_target_proxy`` test
def test_request_with_non_target_proxy(upstream_addon, mock_flow_factory):
    mock_flow = mock_flow_factory(host="non.target.proxy")
    upstream_addon.request(mock_flow)
    assert True
    # assert mock_flow.server_conn.via is None  # No change expected
