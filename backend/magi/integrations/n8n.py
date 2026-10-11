"""n8n client. n8n owns every boundary between MAGI and the outside world:
tool data, action execution, Slack confirmation, the escalation call, the record.

If N8N_BASE_URL is unset, every method returns None and the caller uses the
local fallback, so the whole system still runs on a laptop.
"""

from __future__ import annotations

import logging
from typing import Any, Optional

import httpx

from magi.config import Settings

log = logging.getLogger("magi.n8n")

PATHS = {
    "tool": "/webhook/magi/tool",
    "execute": "/webhook/magi/execute",
    "confirm": "/webhook/magi/confirm",
    "escalate": "/webhook/magi/escalate",
    "close": "/webhook/magi/close",
    "notify": "/webhook/magi/notify",
}


class N8nClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.enabled = settings.n8n_enabled

    async def _post(self, kind: str, payload: dict[str, Any], timeout: float = 15.0) -> Optional[dict]:
        if not self.enabled:
            return None
        url = self.settings.n8n_base_url.rstrip("/") + PATHS[kind]
        headers = {"X-MAGI-Secret": self.settings.n8n_shared_secret}
        # Workflows call back into MAGI using this URL, so nothing is hardcoded in n8n.
        payload = {**payload, "backend_url": self.settings.public_backend_url.rstrip("/")}
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                r = await client.post(url, json=payload, headers=headers)
                r.raise_for_status()
                try:
                    return r.json()
                except ValueError:
                    return {"text": r.text}
        except httpx.HTTPError as e:
            log.warning("n8n %s failed: %s", kind, e)
            return {"error": str(e)}

    async def tool(self, payload: dict[str, Any]) -> Optional[dict]:
        return await self._post("tool", payload)

    async def execute(self, payload: dict[str, Any]) -> Optional[dict]:
        return await self._post("execute", payload, timeout=30.0)

    async def confirm(self, payload: dict[str, Any]) -> Optional[dict]:
        return await self._post("confirm", payload, timeout=5.0)

    async def escalate(self, payload: dict[str, Any]) -> Optional[dict]:
        return await self._post("escalate", payload)

    async def close(self, payload: dict[str, Any]) -> Optional[dict]:
        return await self._post("close", payload)

    async def notify(self, payload: dict[str, Any]) -> Optional[dict]:
        return await self._post("notify", payload, timeout=5.0)
