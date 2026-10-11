"""An agent = mandate + adapter. It sees only what its visibility allows."""

from __future__ import annotations

from typing import Any

from magi.agents import prompts
from magi.agents.tools import openai_tools
from magi.facilitator.state import CouncilState
from magi.llm.base import LLMAdapter, LLMResult, PhaseContext, T, ToolRunner

MAX_TOKENS = {"PROPOSE": 3000, "SCORE": 1500, "CRITIQUE": 3000, "DISSENT": 1200, "VOTE": 1500, "ASSESS": 1200, "SCRIBE": 1200}


class Agent:
    def __init__(self, name: str, adapter: LLMAdapter, anonymize: bool = True):
        self.name = name
        self.adapter = adapter
        self.anonymize = anonymize
        self._calls: dict[str, int] = {}

    def build_ctx(self, state: CouncilState, phase: str, round_: int, **extra: Any) -> PhaseContext:
        visible = state.visible_evidence(self.name)
        seen_sources: dict[str, str] = {}
        for e in visible:
            seen_sources[e.source] = e.id
        latest = {p.id: p.ref for p in state.registry.all_versions()}
        key = f"{state.dp.id if state.dp else ''}|{phase}|{round_}|{extra.get('target_evidence') or ''}"
        idx = self._calls.get(key, 0)
        self._calls[key] = idx + 1
        return PhaseContext(
            scenario_id=state.scenario.id,
            decision_point=state.dp.id if state.dp else "",
            agent=self.name,
            phase=phase,
            round=round_,
            call_index=idx,
            seen_ids={e.id for e in visible},
            seen_sources=seen_sources,
            latest_refs=latest,
            **extra,
        )

    def render_user(self, state: CouncilState, phase: str, **fmt: Any) -> str:
        return prompts.context_block(state, self.name, self.anonymize) + "\n\nTASK: " + prompts.TASKS[phase].format(**fmt)

    async def call(self, state: CouncilState, phase: str, schema: type[T], round_: int,
                   fmt: dict[str, Any] | None = None, tool_runner: ToolRunner | None = None,
                   **ctx_extra: Any) -> tuple[LLMResult, str]:
        system = prompts.system_prompt(self.name, state)
        user = self.render_user(state, phase, **(fmt or {}))
        ctx = self.build_ctx(state, phase, round_, **ctx_extra)
        tools = openai_tools(self.name) if tool_runner else None  # only this agent's own tools
        res = await self.adapter.structured(system=system, user=user, schema=schema, ctx=ctx,
                                            max_tokens=MAX_TOKENS.get(phase, 2000), tools=tools,
                                            tool_runner=tool_runner)
        return res, user
