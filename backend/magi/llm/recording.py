"""Record live responses; replay them later with zero network calls (demo safety net)."""

from __future__ import annotations

import json
from pathlib import Path

from magi.llm.base import LLMAdapter, LLMResult, PhaseContext, T


class RecordingAdapter:
    def __init__(self, inner: LLMAdapter, path: Path):
        self.name = f"record:{inner.name}"
        self.inner = inner
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)

    async def structured(self, *, system: str, user: str, schema: type[T], ctx: PhaseContext, max_tokens: int = 4000) -> LLMResult:
        res = await self.inner.structured(system=system, user=user, schema=schema, ctx=ctx, max_tokens=max_tokens)
        record = {"key": ctx.key(), "status": res.status,
                  "output": res.parsed.model_dump(mode="json") if res.parsed is not None else None}
        with self.path.open("a") as f:
            f.write(json.dumps(record) + "\n")
        return res


class ReplayAdapter:
    def __init__(self, path: Path, delay_s: float = 0.6):
        self.name = "replay"
        self.delay_s = delay_s
        self.records: dict[str, list[dict]] = {}
        if path.exists():
            for line in path.read_text().splitlines():
                rec = json.loads(line)
                self.records.setdefault(rec["key"], []).append(rec)

    async def structured(self, *, system: str, user: str, schema: type[T], ctx: PhaseContext, max_tokens: int = 4000) -> LLMResult:
        import asyncio

        if self.delay_s:
            await asyncio.sleep(self.delay_s)
        recs = self.records.get(ctx.key())
        if not recs:
            return LLMResult(None, "no_script", model="replay", detail=ctx.key())
        rec = recs.pop(0)
        if rec["output"] is None:
            return LLMResult(None, rec["status"], model="replay")
        return LLMResult(schema.model_validate(rec["output"]), "ok", model="replay")
