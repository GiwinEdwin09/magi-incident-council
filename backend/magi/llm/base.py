from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable, Optional, Protocol, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


@dataclass
class PhaseContext:
    """Structured view of the call, used by scripted/replay adapters and for logging."""

    scenario_id: str
    decision_point: str
    agent: str
    phase: str
    round: int = 0
    call_index: int = 0
    ballot_ref: Optional[str] = None
    ballot_hash: Optional[str] = None
    target_evidence: Optional[str] = None
    leading_ref: Optional[str] = None
    seen_ids: set[str] = field(default_factory=set)
    seen_sources: dict[str, str] = field(default_factory=dict)  # source -> newest evidence id
    latest_refs: dict[str, str] = field(default_factory=dict)  # "P-3" -> "P-3@2"

    def key(self) -> str:
        return f"{self.scenario_id}|{self.decision_point}|{self.agent}|{self.phase}|{self.round}|{self.target_evidence or ''}|{self.call_index}"


@dataclass
class LLMResult:
    parsed: Optional[Any]
    status: str  # ok | refusal | parse_error | timeout | error | no_script
    input_tokens: int = 0
    output_tokens: int = 0
    latency_ms: int = 0
    model: str = ""
    detail: str = ""


# Native tool calling: the adapter calls this with (tool name, arguments) and gets back the text
# result. Adapters without native tools ignore it; agents then use structured tool_requests.
ToolRunner = Callable[[str, dict], Awaitable[str]]


class LLMAdapter(Protocol):
    name: str

    async def structured(
        self, *, system: str, user: str, schema: type[T], ctx: PhaseContext, max_tokens: int = 4000,
        tools: Optional[list[dict]] = None, tool_runner: Optional[ToolRunner] = None,
    ) -> LLMResult: ...
