"""Tests for config"""

from __future__ import annotations

import unittest

from aitm.proxy.utils.config import Config, get_config


class TestConfig(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.config = get_config()
        self.config = Config()

    def tearDown(self) -> None:
        del self.config
        super().tearDown()

    def test_initialization(self):
        """Test the initialization and default values."""
        self.assertEqual(self.config.content_types, [])
        self.assertEqual(self.config.custom_modifications, [])
        self.assertEqual(self.config.auth_url, [])
        self.assertEqual(self.config.targets, [])
        self.assertEqual(self.config.target_sites, [])
        self.assertEqual(self.config.target_proxies, [])
        self.assertEqual(self.config.local_upstream_scheme, "http")
        self.assertEqual(self.config.local_upstream_hostname, "")
        self.assertEqual(self.config.mfa_claim, "")

    def test_targets_setting_and_getting(self):
        """Test setting and getting targets."""
        targets = [
            {"origin": "example.com", "proxy": "proxy1", "port": 80},
            {"origin": "example2.com", "proxy": "proxy2", "port": 443},
        ]
        self.config.targets = targets
        self.assertEqual(self.config.targets, targets)
        self.assertEqual(self.config.target_sites, ["example.com", "example2.com"])
        self.assertEqual(self.config.target_proxies, ["proxy1", "proxy2"])

    def test_targets_modification(self):
        """Test modification of targets."""
        targets = [
            {"origin": "example.com", "proxy": "proxy1", "port": 80},
        ]
        self.config.targets = targets
        new_targets = targets + [{"origin": "example3.com", "proxy": "proxy3", "port": 8080}]
        self.config.targets = new_targets
        self.assertEqual(self.config.targets, new_targets)
        self.assertIn("example3.com", self.config.target_sites)
        self.assertIn("proxy3", self.config.target_proxies)

    def test_targets_deletion(self):
        """Test deletion of targets."""
        targets = [
            {"origin": "example.com", "proxy": "proxy1", "port": 80},
        ]
        self.config.targets = targets
        del self.config.targets

        self.assertRaises(AttributeError, lambda: self.config.targets)
        self.assertRaises(AttributeError, lambda: self.config.target_sites)
        self.assertRaises(AttributeError, lambda: self.config.target_proxies)


if __name__ == "__main__":
    unittest.main()
