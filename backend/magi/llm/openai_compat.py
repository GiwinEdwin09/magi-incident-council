"""OpenAI adapter: official OpenAI SDK, schema-validated structured outputs.

- Official OpenAI (OPENAI_BASE_URL empty or api.openai.com): Responses API with native function
  tools. The agent can call its own data tools mid-turn (bounded by max_tool_calls) and the
  model's reasoning carries across those calls; the final answer is parsed into the phase schema.
- Any other OpenAI-compatible server (vLLM, Together, Groq, OpenRouter, a NIM on Brev...): Chat
  Completions with strict JSON-schema output, falling back to JSON mode when the server lacks
  structured outputs. No native tools there; agents use structured tool_requests instead.
"""

from __future__ import annotations

import json
import time
from typing import Optional

import openai
from pydantic import ValidationError

from magi.llm.base import LLMResult, PhaseContext, T, ToolRunner


class OpenAICompatAdapter:
    def __init__(self, model: str, api_key: str, base_url: str = "", timeout_s: float = 90.0,
                 reasoning_effort: str = "", http_client=None, min_output_tokens: int = 0, max_tool_calls: int = 4):
        self.name = f"openai:{model}"
        self.model = model
        self.official = not base_url or "api.openai.com" in base_url
        self.reasoning_effort = reasoning_effort
        self.min_output_tokens = min_output_tokens
        self.max_tool_calls = max_tool_calls
        self.client = openai.AsyncOpenAI(api_key=api_key, base_url=base_url or None, timeout=timeout_s, max_retries=1,
                                         http_client=http_client)
        self._json_mode_only = False  # set after a compatible server rejects json_schema once

    async def structured(
        self, *, system: str, user: str, schema: type[T], ctx: PhaseContext, max_tokens: int = 4000,
        tools: Optional[list[dict]] = None, tool_runner: Optional[ToolRunner] = None,
    ) -> LLMResult:
        t0 = time.monotonic()
        max_tokens = max(max_tokens, self.min_output_tokens)
        try:
            if self.official:
                return await self._responses(system, user, schema, max_tokens, tools, tool_runner, t0)
            return await self._chat(system, user, schema, max_tokens, t0)
        except openai.APITimeoutError:
            return LLMResult(None, "timeout", model=self.model)
        except openai.APIStatusError as e:
            return LLMResult(None, "error", model=self.model, detail=f"{e.status_code}: {str(e)[:300]}")
        except openai.APIConnectionError as e:
            return LLMResult(None, "error", model=self.model, detail=str(e)[:300])
        except (ValidationError, openai.LengthFinishReasonError, openai.ContentFilterFinishReasonError) as e:
            return LLMResult(None, "parse_error", model=self.model, detail=str(e)[:300])

    # ------------------------------------------------------------------ Responses API (official OpenAI)
    async def _responses(self, system: str, user: str, schema: type[T], max_tokens: int,
                         tools: Optional[list[dict]], tool_runner: Optional[ToolRunner], t0: float) -> LLMResult:
        kwargs: dict = {"model": self.model, "instructions": system, "text_format": schema,
                        "max_output_tokens": max_tokens}
        if self.reasoning_effort:
            kwargs["reasoning"] = {"effort": self.reasoning_effort}
        if tools and tool_runner and self.max_tool_calls > 0:
            kwargs["tools"] = tools

        items: list = [{"role": "user", "content": user}]
        previous: Optional[str] = None
        tin = tout = calls = 0
        while True:
            resp = await self.client.responses.parse(
                input=items, **({"previous_response_id": previous} if previous else {}), **kwargs)
            if resp.usage:
                tin += resp.usage.input_tokens
                tout += resp.usage.output_tokens
            function_calls = [o for o in resp.output if o.type == "function_call"]
            if not function_calls:
                break
            outputs = []
            for fc in function_calls:
                calls += 1
                if calls > self.max_tool_calls:
                    result = "Tool budget for this turn is used up. Answer with the evidence you have."
                else:
                    try:
                        args = json.loads(fc.arguments or "{}")
                    except json.JSONDecodeError:
                        args = {}
                    result = await tool_runner(fc.name, args)  # type: ignore[misc]
                outputs.append({"type": "function_call_output", "call_id": fc.call_id, "output": result})
            if calls >= self.max_tool_calls:
                kwargs["tool_choice"] = "none"  # the next turn must answer
            previous, items = resp.id, outputs

        latency = int((time.monotonic() - t0) * 1000)
        for item in resp.output:
            if item.type == "message":
                for part in item.content:
                    if part.type == "refusal":
                        return LLMResult(None, "refusal", tin, tout, latency, resp.model, detail=part.refusal[:200])
        if resp.status == "incomplete":
            reason = getattr(resp.incomplete_details, "reason", "") if resp.incomplete_details else ""
            return LLMResult(None, "parse_error", tin, tout, latency, resp.model, detail=f"incomplete: {reason}")
        if resp.output_parsed is None:
            return LLMResult(None, "parse_error", tin, tout, latency, resp.model)
        return LLMResult(resp.output_parsed, "ok", tin, tout, latency, resp.model,
                         detail=f"{calls} tool call(s)" if calls else "")

    # ------------------------------------------------------------------ Chat Completions (compatible servers)
    def _limits(self, max_tokens: int) -> dict:
        extra: dict = {"max_completion_tokens": max_tokens} if self.official else {"max_tokens": max_tokens}
        if self.reasoning_effort:
            extra["reasoning_effort"] = self.reasoning_effort
        return extra

    async def _chat(self, system: str, user: str, schema: type[T], max_tokens: int, t0: float) -> LLMResult:
        messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]
        if not self._json_mode_only:
            try:
                resp = await self.client.chat.completions.parse(
                    model=self.model, messages=messages, response_format=schema, **self._limits(max_tokens))
                return self._from_parsed(resp, t0)
            except openai.BadRequestError as e:
                if "response_format" not in str(e) and "json_schema" not in str(e):
                    raise
                self._json_mode_only = True
        return await self._json_mode(messages, schema, max_tokens, t0)

    def _from_parsed(self, resp, t0: float) -> LLMResult:
        latency = int((time.monotonic() - t0) * 1000)
        usage = resp.usage
        tin, tout = (usage.prompt_tokens, usage.completion_tokens) if usage else (0, 0)
        msg = resp.choices[0].message
        if getattr(msg, "refusal", None):
            return LLMResult(None, "refusal", tin, tout, latency, resp.model, detail=msg.refusal[:200])
        if msg.parsed is None:
            return LLMResult(None, "parse_error", tin, tout, latency, resp.model)
        return LLMResult(msg.parsed, "ok", tin, tout, latency, resp.model)

    async def _json_mode(self, messages: list[dict], schema: type[T], max_tokens: int, t0: float) -> LLMResult:
        instruction = ("Respond with ONLY a JSON object that validates against this JSON Schema:\n"
                       + json.dumps(schema.model_json_schema()))
        msgs = [{"role": "system", "content": messages[0]["content"] + "\n\n" + instruction}, messages[1]]
        resp = await self.client.chat.completions.create(
            model=self.model, messages=msgs, response_format={"type": "json_object"}, **self._limits(max_tokens))
        latency = int((time.monotonic() - t0) * 1000)
        usage = resp.usage
        tin, tout = (usage.prompt_tokens, usage.completion_tokens) if usage else (0, 0)
        text = resp.choices[0].message.content or ""
        try:
            return LLMResult(schema.model_validate_json(text), "ok", tin, tout, latency, resp.model)
        except ValidationError as e:
            return LLMResult(None, "parse_error", tin, tout, latency, resp.model, detail=str(e)[:300])
