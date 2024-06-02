"""
Main script to start mitmproxy with custom addons.
"""

from __future__ import annotations

import asyncio

from hypercorn.asyncio import serve
from hypercorn.config import Config
from mitmproxy import options
from mitmproxy.tools import dump

from aitm_web import create_app
from aitm_web.event_listener import EventListener as WebEventListener

from .events import EventListener
from .proxy.modifier_addon import ModifierAddon
from .proxy.upstream_addon import UpstreamAddon
from .proxy.utils import get_config


async def start_proxy(proxies: list[str], listener: EventListener):
    """
    Asynchronously starts the mitmproxy with specified proxies.

    This function sets up and runs the mitmproxy with the provided proxy
    configurations, adding custom addons for upstream and request/response
    modification.

    Args:
        proxies (list[str]): A list of proxy modes for mitmproxy to use.

    Returns:
        mitmproxy.tools.dump.DumpMaster: The running mitmproxy instance.
    """
    opts = options.Options(showhost=True, listen_host="0.0.0.0", listen_port=8080, mode=proxies)

    master = dump.DumpMaster(
        opts,
        with_termlog=False,
        with_dumper=False,
    )

    upstream = UpstreamAddon()
    modifier = ModifierAddon()
    modifier.event_emitter.attach(listener)
    modifier.state_machine.event_emitter.attach(listener)
    master.addons.add(upstream)
    master.addons.add(modifier)
    master.options.set("block_global=false")
    master.options.set("connection_strategy=lazy")
    await master.run()


async def start_web():
    app = create_app()
    await serve(app, Config())


if __name__ == "__main__":

    listener = WebEventListener.get_listener()
    reverse_proxies = [f"reverse:https://{target['origin']}@{target['port']}" for target in get_config().targets]
    reverse_proxies.append("upstream:https://dummy:8888")
    loop = asyncio.new_event_loop()
    t_web = loop.create_task(start_web(), name="AITM Web")
    t_proxy = loop.create_task(start_proxy(reverse_proxies, listener), name="AITM Proxy")
    loop.run_until_complete(asyncio.gather(t_web, t_proxy))
    loop.close()
