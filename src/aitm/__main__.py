"""
Main script to start mitmproxy with custom addons.
"""

from __future__ import annotations

import asyncio
import logging

from mitmproxy import options
from mitmproxy.tools import dump

from .events import EventListener
from .proxy.modifier_addon import ModifierAddon
from .proxy.upstream_addon import UpstreamAddon
from .proxy.utils import get_config

logging.root.setLevel("INFO")


async def start_proxy(proxies: list[str]):
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
        with_termlog=True,
        with_dumper=False,
    )
    master.addons.add(UpstreamAddon())

    modifier = ModifierAddon()
    listener = EventListener()
    modifier.event_emitter.attach(listener)
    modifier.state_machine.event_emitter.attach(listener)
    master.addons.add(ModifierAddon())
    master.options.set("block_global=false")
    master.options.set("connection_strategy=lazy")
    await master.run()
    return master


if __name__ == "__main__":

    reverse_proxies = [f"reverse:https://{target['origin']}@{target['port']}" for target in get_config().targets]
    reverse_proxies.append("upstream:https://dummy:8888")
    asyncio.run(start_proxy(reverse_proxies))
