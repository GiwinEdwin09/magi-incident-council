from __future__ import annotations

import asyncio
from typing import Callable, Optional

import pytest

from magi.config import Settings
from magi.incident import Incident
from magi.integrations.n8n import N8nClient
from magi.llm import build_adapters
from magi.sim.scenario import load_scenario


def make_settings(**kw) -> Settings:
    base = dict(magi_mode="scripted", n8n_base_url="", anthropic_api_key="", confirm_timeout_s=5.0)
    base.update(kw)
    return Settings(**base)


async def run_scenario(scenario_id: str, on_tick: Optional[Callable[[Incident], None]] = None,
                       adapters=None, timeout_s: float = 20.0) -> Incident:
    s = make_settings()
    adapters = adapters or build_adapters(s, scenario_id, mode="scripted", delay_s=0)
    inc = Incident(load_scenario(scenario_id), s, adapters, N8nClient(s), speed=60, tick_s=0.01)
    inc.start()
    loop = asyncio.get_running_loop()
    deadline = loop.time() + timeout_s
    while not inc.closed and loop.time() < deadline:
        await asyncio.sleep(0.005)
        if on_tick:
            on_tick(inc)
    await inc.stop()
    return inc


@pytest.fixture
def settings() -> Settings:
    return make_settings()
