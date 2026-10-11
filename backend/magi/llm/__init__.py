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

    out: dict[str, LLMAdapter] = {}
    for r in roles:
        provider, model = settings.model_for(r)
        if models and models.get(r):
            spec = models[r]
            provider, model = spec.split(":", 1) if ":" in spec else (provider, spec)
        inner = make_live_adapter(settings, provider, model)
        out[r] = RecordingAdapter(inner, recording) if mode == "record" else inner
    return out


def make_live_adapter(settings: Settings, provider: str, model: str) -> LLMAdapter:
    if not model:
        raise ValueError(f"No model configured for provider '{provider}'. Set OPENAI_MODEL (or MODEL_<AGENT>) in .env.")
    if provider == "openai":
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is not set in .env.")
        from magi.llm.openai_compat import OpenAICompatAdapter

        return OpenAICompatAdapter(model, settings.openai_api_key, settings.openai_base_url, settings.llm_timeout_s,
                                   settings.openai_reasoning_effort, min_output_tokens=settings.llm_min_output_tokens,
                                   max_tool_calls=settings.llm_max_tool_calls)
    if provider == "anthropic":
        if not settings.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY is not set in .env.")
        from magi.llm.claude import ClaudeAdapter

        return ClaudeAdapter(model, settings.anthropic_api_key, settings.effort_default, settings.llm_timeout_s)
    raise ValueError(f"Unknown LLM provider '{provider}' (use openai or anthropic).")
