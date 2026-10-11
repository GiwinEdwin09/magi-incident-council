"""Claude adapter: official Anthropic SDK, schema-validated structured outputs."""

from __future__ import annotations

import time

import anthropic
from pydantic import ValidationError

from magi.llm.base import LLMResult, PhaseContext, T


class ClaudeAdapter:
    def __init__(self, model: str, effort: str = "low", timeout_s: float = 45.0):
        self.name = f"claude:{model}"
        self.model = model
        self.effort = effort
        self.client = anthropic.AsyncAnthropic(timeout=timeout_s, max_retries=1)

    async def structured(
        self, *, system: str, user: str, schema: type[T], ctx: PhaseContext, max_tokens: int = 4000
    ) -> LLMResult:
        t0 = time.monotonic()
        try:
            resp = await self.client.messages.parse(
                model=self.model,
                max_tokens=max_tokens,
                system=system,
                messages=[{"role": "user", "content": user}],
                output_format=schema,
                output_config={"effort": self.effort},
            )
        except anthropic.APITimeoutError:
            return LLMResult(None, "timeout", model=self.model)
        except ValidationError as e:
            return LLMResult(None, "parse_error", model=self.model, detail=str(e)[:300])
        except anthropic.APIStatusError as e:
            return LLMResult(None, "error", model=self.model, detail=f"{e.status_code}: {str(e)[:300]}")
        except anthropic.APIConnectionError as e:
            return LLMResult(None, "error", model=self.model, detail=str(e)[:300])

        latency = int((time.monotonic() - t0) * 1000)
        usage = resp.usage
        if resp.stop_reason == "refusal":
            return LLMResult(None, "refusal", usage.input_tokens, usage.output_tokens, latency, resp.model)
        parsed = resp.parsed_output
        if parsed is None:
            status = "parse_error" if resp.stop_reason != "max_tokens" else "error"
            return LLMResult(None, status, usage.input_tokens, usage.output_tokens, latency, resp.model,
                             detail=f"stop_reason={resp.stop_reason}")
        return LLMResult(parsed, "ok", usage.input_tokens, usage.output_tokens, latency, resp.model)
