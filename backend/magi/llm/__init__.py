from __future__ import annotations

from pathlib import Path

from magi.config import Settings
from magi.llm.base import LLMAdapter, LLMResult, PhaseContext
from magi.llm.recording import RecordingAdapter, ReplayAdapter
from magi.llm.scripted import ScriptedAdapter

__all__ = ["LLMAdapter", "LLMResult", "PhaseContext", "build_adapters"]


def build_adapters(settings: Settings, scenario_id: str, mode: str | None = None,
                   models: dict[str, str] | None = None, delay_s: float | None = None) -> dict[str, LLMAdapter]:
    """One adapter per agent (plus SCRIBE), so agents can run on different models."""
    mode = mode or settings.mode
    roles = ["MELCHIOR", "BALTHASAR", "CASPER", "SCRIBE"]
    scripted_dir = Path(settings.scenarios_dir) / "scripted"
    delay = settings.scripted_delay_s if delay_s is None else delay_s
    recording = Path(settings.recordings_dir) / f"{scenario_id}.jsonl"

    if mode == "scripted":
        a = ScriptedAdapter(scripted_dir, delay)
        return {r: a for r in roles}
    if mode == "replay":
        a = ReplayAdapter(recording, delay)
        return {r: a for r in roles}

    from magi.llm.claude import ClaudeAdapter

    out: dict[str, LLMAdapter] = {}
    for r in roles:
        model = (models or {}).get(r) or settings.model_for(r)
        inner = ClaudeAdapter(model, settings.effort_default, settings.llm_timeout_s)
        out[r] = RecordingAdapter(inner, recording) if mode == "record" else inner
    return out
