"""Scripted adapter: deterministic agent outputs from a YAML script.

Used for frontend development, tests, and as an offline demo fallback. Each
entry has a `when` condition and an `output` matching the phase schema.
Strings may contain templates resolved from the call context:
  {{ballot_ref}} {{ballot_hash}} {{target}} {{leading}}
  {{latest:P-3}}  -> newest version ref of P-3
  {{tool:check_ip_allowlist}} -> id of the newest evidence from that tool
  {{src:oncall_human}} -> id of the newest evidence from that source
"""

from __future__ import annotations

import asyncio
import re
from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from magi.llm.base import LLMResult, PhaseContext, T

_TEMPLATE = re.compile(r"\{\{\s*([a-z_]+)(?::([^}\s]+))?\s*\}\}")


class ScriptedAdapter:
    def __init__(self, script_dir: Path, delay_s: float = 0.9):
        self.name = "scripted"
        self.script_dir = script_dir
        self.delay_s = delay_s
        self._cache: dict[str, dict] = {}

    def _script(self, scenario_id: str) -> dict:
        if scenario_id not in self._cache:
            path = self.script_dir / f"{scenario_id}.yaml"
            self._cache[scenario_id] = yaml.safe_load(path.read_text()) if path.exists() else {}
        return self._cache[scenario_id]

    @staticmethod
    def _matches(when: dict[str, Any], ctx: PhaseContext) -> bool:
        for k, v in (when or {}).items():
            if k == "dp" and ctx.decision_point != v:
                return False
            if k == "round" and ctx.round not in (v if isinstance(v, list) else [v]):
                return False
            if k == "evidence" and ctx.target_evidence != v:
                return False
            if k == "seen" and v not in ctx.seen_ids:
                return False
            if k == "not_seen" and v in ctx.seen_ids:
                return False
            if k == "seen_source" and v not in ctx.seen_sources:
                return False
            if k == "not_seen_source" and v in ctx.seen_sources:
                return False
            if k == "ballot" and not (ctx.ballot_ref or "").startswith(v):
                return False
            if k == "leading" and not (ctx.leading_ref or "").startswith(v):
                return False
            if k == "call_index" and ctx.call_index != v:
                return False
        return True

    @staticmethod
    def _render(obj: Any, ctx: PhaseContext) -> Any:
        if isinstance(obj, dict):
            return {k: ScriptedAdapter._render(v, ctx) for k, v in obj.items()}
        if isinstance(obj, list):
            return [ScriptedAdapter._render(v, ctx) for v in obj]
        if not isinstance(obj, str):
            return obj

        def sub(m: re.Match) -> str:
            name, arg = m.group(1), m.group(2)
            if name == "ballot_ref":
                return ctx.ballot_ref or ""
            if name == "ballot_hash":
                return ctx.ballot_hash or ""
            if name == "target":
                return ctx.target_evidence or ""
            if name == "leading":
                return ctx.leading_ref or ""
            if name == "latest" and arg:
                return ctx.latest_refs.get(arg, f"{arg}@1")
            if name == "tool" and arg:
                return ctx.seen_sources.get(f"tool:{arg}", "")
            if name == "src" and arg:
                return ctx.seen_sources.get(arg, "")
            return m.group(0)

        return _TEMPLATE.sub(sub, obj)

    async def structured(
        self, *, system: str, user: str, schema: type[T], ctx: PhaseContext, max_tokens: int = 4000,
        tools=None, tool_runner=None,
    ) -> LLMResult:
        if self.delay_s:
            await asyncio.sleep(self.delay_s)
        entries = (self._script(ctx.scenario_id).get(ctx.agent) or {}).get(ctx.phase) or []
        for entry in entries:
            if self._matches(entry.get("when", {}), ctx):
                data = self._render(entry["output"], ctx)
                try:
                    return LLMResult(schema.model_validate(data), "ok", model="scripted")
                except ValidationError as e:
                    return LLMResult(None, "parse_error", model="scripted", detail=str(e)[:400])
        return LLMResult(None, "no_script", model="scripted", detail=ctx.key())
