from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parent.parent
REPO_DIR = BACKEND_DIR.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(REPO_DIR / ".env", BACKEND_DIR / ".env"), extra="ignore"
    )

    # LLM. LLM_PROVIDER picks the default provider; MODEL_<AGENT> can override per agent with
    # "provider:model" (e.g. "anthropic:claude-opus-5-5") to mix model families.
    llm_provider: str = "auto"  # auto | openai | anthropic
    openai_api_key: str = ""
    openai_base_url: str = ""  # empty = api.openai.com; set for any OpenAI-compatible server
    openai_model: str = ""
    openai_reasoning_effort: str = ""  # optional, only for models that support it
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-opus-5-5"
    model_melchior: str = ""
    model_balthasar: str = ""
    model_casper: str = ""
    model_scribe: str = ""
    effort_default: str = "low"  # Anthropic effort
    llm_timeout_s: float = 90.0
    # Reasoning models spend output tokens on hidden reasoning, so phase caps are raised to this floor.
    llm_min_output_tokens: int = 32000
    llm_max_tool_calls: int = 4  # native tool calls per agent per phase (official OpenAI only)
    llm_price_in_per_mtok: float = 0.0  # USD per million input tokens, for the cost readout (0 = unknown)
    llm_price_out_per_mtok: float = 0.0

    # Modes: scripted (no API calls) | live | record | replay
    magi_mode: str = "auto"
    scripted_delay_s: float = 0.9
    anonymize_peers: bool = True
    max_rounds: int = 3
    decision_time_budget_s: float = 180.0
    confirm_timeout_s: float = 120.0

    # Security
    magi_signing_key: str = "dev-signing-key-change-me"
    n8n_shared_secret: str = ""
    elevenlabs_tool_secret: str = ""
    elevenlabs_webhook_secret: str = ""  # HMAC secret of the workspace post-call webhook
    agent_token_melchior: str = ""
    agent_token_balthasar: str = ""
    agent_token_casper: str = ""

    # Integrations (empty = local fallback)
    public_backend_url: str = "http://127.0.0.1:8787"
    n8n_base_url: str = ""
    elevenlabs_api_key: str = ""
    elevenlabs_agent_id: str = ""
    elevenlabs_phone_number_id: str = ""
    oncall_name: str = "Alex"
    oncall_phone: str = ""

    # Storage
    db_path: str = str(BACKEND_DIR / "magi.sqlite")
    recordings_dir: str = str(BACKEND_DIR / "recordings")
    scenarios_dir: str = str(BACKEND_DIR / "scenarios")

    @property
    def provider(self) -> str:
        if self.llm_provider != "auto":
            return self.llm_provider
        return "openai" if self.openai_api_key else "anthropic"

    @property
    def has_llm(self) -> bool:
        return bool(self.openai_api_key if self.provider == "openai" else self.anthropic_api_key)

    @property
    def mode(self) -> str:
        if self.magi_mode != "auto":
            return self.magi_mode
        return "live" if self.has_llm else "scripted"

    @property
    def n8n_enabled(self) -> bool:
        return bool(self.n8n_base_url)

    @property
    def phone_enabled(self) -> bool:
        return bool(
            self.n8n_base_url
            and self.elevenlabs_agent_id
            and self.elevenlabs_phone_number_id
            and self.oncall_phone
        )

    def model_for(self, agent: str) -> tuple[str, str]:
        """(provider, model) for an agent role: per-agent override, else the provider default."""
        spec = {"MELCHIOR": self.model_melchior, "BALTHASAR": self.model_balthasar,
                "CASPER": self.model_casper}.get(agent, self.model_scribe)
        if spec and ":" in spec:
            provider, _, model = spec.partition(":")
            return provider, model
        provider = self.provider
        default = self.openai_model if provider == "openai" else self.anthropic_model
        return provider, spec or default


@lru_cache
def get_settings() -> Settings:
    return Settings()
