from __future__ import annotations

import unittest

from simple_observer.event import Event


class TestEvent(unittest.TestCase):

    def setUp(self):
        self.event = Event("test_event")

    def test_event_type(self):
        self.assertEqual(self.event.event_type, "test_event")

    def test_to_string(self):
        self.assertEqual(str(self.event), "Event type: test_event, data: None")


if __name__ == "__main__":
    unittest.main()
