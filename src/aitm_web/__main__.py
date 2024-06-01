from __future__ import annotations

import asyncio

from hypercorn.asyncio import serve
from hypercorn.config import Config

from . import create_app

app = create_app()

if __name__ == "__main__":
    asyncio.run(serve(app, Config()))
