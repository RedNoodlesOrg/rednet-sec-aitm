"""Tests for config"""

from __future__ import annotations

import pytest

from aitm.helpers.config import Config


def test_initialization():
    """Test the initialization and default values."""
    config = Config()
    assert not config.content_types
    assert not config.custom_modifications
    assert not config.auth_url
    assert not config.targets
    assert not config.target_sites
    assert not config.target_proxies
    assert config.local_upstream_scheme == "http"
    assert config.local_upstream_hostname == ""
    assert config.mfa_claim == ""


def test_targets_setting_and_getting():
    """Test setting and getting targets."""
    config = Config()
    targets = [
        {"origin": "example.com", "proxy": "proxy1", "port": 80},
        {"origin": "example2.com", "proxy": "proxy2", "port": 443},
    ]
    config.targets = targets
    assert config.targets == targets
    assert config.target_sites == ["example.com", "example2.com"]
    assert config.target_proxies == ["proxy1", "proxy2"]


def test_targets_modification():
    """Test modification of targets."""
    config = Config()
    targets = [
        {"origin": "example.com", "proxy": "proxy1", "port": 80},
    ]
    config.targets = targets
    new_targets = targets + [{"origin": "example3.com", "proxy": "proxy3", "port": 8080}]
    config.targets = new_targets
    assert config.targets == new_targets
    assert "example3.com" in config.target_sites
    assert "proxy3" in config.target_proxies


def test_targets_deletion():
    """Test deletion of targets."""
    config = Config()
    targets = [
        {"origin": "example.com", "proxy": "proxy1", "port": 80},
    ]
    config.targets = targets
    del config.targets
    # After deletion, accessing targets or its derivatives should raise an AttributeError
    with pytest.raises(AttributeError):
        _ = config.targets
    with pytest.raises(AttributeError):
        _ = config.target_sites
    with pytest.raises(AttributeError):
        _ = config.target_proxies
