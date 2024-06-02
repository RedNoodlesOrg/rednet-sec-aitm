from __future__ import annotations

import asyncio

from hypercorn.asyncio import serve
from hypercorn.config import Config

from . import create_app
from .event_listener import EventListener as WebEventListener

app = create_app()

if __name__ == "__main__":
    listener = WebEventListener.get_listener()

    asyncio.run(serve(app, Config()))
