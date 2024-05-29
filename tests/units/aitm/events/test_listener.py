from __future__ import annotations

import asyncio
import unittest
from unittest.mock import patch

from aitm.events import EventEmitter, EventListener
from simple_observer import Event


class TestEventListener(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.subject = EventEmitter()
        self.listener = EventListener()

    async def test_update(self):
        with patch("builtins.print") as mock_print:
            event = Event("test_event", {"data": "test_data"})
            self.subject.attach(self.listener)
            self.subject.notify(event)
            await asyncio.gather(*asyncio.all_tasks() - {asyncio.current_task()})
            mock_print.assert_called_once()


if __name__ == "__main__":
    unittest.main()
