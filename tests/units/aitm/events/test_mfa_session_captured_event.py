from __future__ import annotations

import unittest

from aitm.events.mfa_session_captured_event import MfaSessionCapturedEvent
from simple_observer.event import Event


class TestMfaSessionCapturedEvent(unittest.TestCase):

    def setUp(self):
        self.parsed_cookies = [{"name": "cookie1", "value": "value1"}, {"name": "cookie2", "value": "value2"}]
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        self.event = MfaSessionCapturedEvent(self.parsed_cookies, self.user_agent)

    def test_event_inheritance(self):
        self.assertIsInstance(self.event, Event)

    def test_parsed_cookies(self):
        self.assertEqual(self.event.parsed_cookies, self.parsed_cookies)

    def test_user_agent(self):
        self.assertEqual(self.event.user_agent, self.user_agent)

    def test_str_representation(self):
        expected_str = f"MFA session captured with cookies: {self.parsed_cookies} and user agent: {self.user_agent}"
        self.assertEqual(str(self.event), expected_str)


if __name__ == "__main__":
    unittest.main()
