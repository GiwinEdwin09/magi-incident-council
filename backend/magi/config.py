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

    # LLM
    anthropic_api_key: str = ""
    model_melchior: str = "claude-opus-5-5"
    model_balthasar: str = "claude-opus-5-5"
    model_casper: str = "claude-opus-5-5"
    model_scribe: str = "claude-opus-5-5"
    effort_default: str = "low"
    llm_timeout_s: float = 45.0

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
    def mode(self) -> str:
        if self.magi_mode != "auto":
            return self.magi_mode
        return "live" if self.anthropic_api_key else "scripted"

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

    def model_for(self, agent: str) -> str:
        return {
            "MELCHIOR": self.model_melchior,
            "BALTHASAR": self.model_balthasar,
            "CASPER": self.model_casper,
        }.get(agent, self.model_scribe)


@lru_cache
def get_settings() -> Settings:
    return Settings()
