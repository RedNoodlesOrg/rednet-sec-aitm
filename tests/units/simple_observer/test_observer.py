from __future__ import annotations

import unittest

from simple_observer.observer import Observer


class MockObserver(Observer):
    def __init__(self):
        super().__init__()
        self.updated = False

    def update(self, *args, **kwargs):
        self.updated = True


class TestObserver(unittest.TestCase):

    def setUp(self):
        self.observer = MockObserver()

    def test_update(self):
        self.observer.update()
        self.assertTrue(self.observer.updated)


if __name__ == "__main__":
    unittest.main()
