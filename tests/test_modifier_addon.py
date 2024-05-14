from __future__ import annotations

from unittest.mock import patch

import pytest
from mitmproxy.test.tflow import tflow
from mitmproxy.test.tutils import treq

from aitm.helpers.config import Config
from aitm.modifier_addon import ModifierAddon

mock_config = Config(mfa_claim="mock_mfa_claim", auth_url=["/mock/auth/url"])
mock_config.targets = [{"origin": "example.com", "proxy": "proxy.example.com"}]


@pytest.fixture
def modifier_addon():
    with patch("aitm.modifier_addon.config", mock_config):
        addon = ModifierAddon()
    return addon


@pytest.fixture
def mock_flow_request():
    flow = tflow(req=treq())
    flow.request.urlencoded_form = {"login": "user", "passwd": "pass"}
    return flow


@pytest.fixture
def mock_flow_response():
    flow = tflow(req=treq(), resp=True)
    return flow


# TODO Implement the ``request_host_header`` test
def test_request_host_header(modifier_addon, mock_flow_request):
    mock_flow_request.request.path = "/common/oauth2/v2.0/authorize"
    modifier_addon.request(mock_flow_request)
    mock_flow_request.request.path = "/common/login"
    modifier_addon.request(mock_flow_request)
    assert True


# TODO Implement the ``response_location_header`` test
def test_response_location_header(modifier_addon, mock_flow_response):
    mock_flow_response.response.path = "/mock/auth/url"
    modifier_addon.response(mock_flow_response)
    assert True
