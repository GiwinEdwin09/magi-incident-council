"""OpenAI-compatible adapter against a fake server, and per-agent provider routing."""

from __future__ import annotations

import json

import httpx2
import openai

from magi.llm.base import PhaseContext
from magi.llm.openai_compat import OpenAICompatAdapter
from magi.models import ScribeOutput
from tests.conftest import make_settings

CTX = PhaseContext(scenario_id="s", decision_point="DP1", agent="SCRIBE", phase="SCRIBE")
GOOD = {"situation": "s", "crux": "c", "option_summaries": ["a", "b"]}


def completion(content: str) -> dict:
    return {"id": "x", "object": "chat.completion", "created": 0, "model": "fake-model",
            "choices": [{"index": 0, "finish_reason": "stop",
                         "message": {"role": "assistant", "content": content, "refusal": None}}],
            "usage": {"prompt_tokens": 11, "completion_tokens": 7, "total_tokens": 18}}


def adapter(handler, base_url="http://fake/v1") -> OpenAICompatAdapter:
    client = openai.DefaultAsyncHttpxClient(transport=httpx2.MockTransport(handler))
    return OpenAICompatAdapter("fake-model", "k", base_url, http_client=client)


async def test_strict_structured_output():
    seen = []

    def handler(req):
        body = json.loads(req.content)
        seen.append(body)
        return httpx2.Response(200, json=completion(json.dumps(GOOD)))

    res = await adapter(handler).structured(system="sys", user="u", schema=ScribeOutput, ctx=CTX)
    assert res.status == "ok" and res.parsed.crux == "c" and res.input_tokens == 11
    assert seen[0]["response_format"]["type"] == "json_schema"
    assert "max_tokens" in seen[0]  # compatible server: max_tokens, not max_completion_tokens


async def test_falls_back_to_json_mode_when_server_lacks_structured_outputs():
    calls = []

    def handler(req):
        body = json.loads(req.content)
        calls.append(body["response_format"]["type"])
        if body["response_format"]["type"] == "json_schema":
            return httpx2.Response(400, json={"error": {"message": "response_format json_schema not supported"}})
        return httpx2.Response(200, json=completion(json.dumps(GOOD)))

    a = adapter(handler)
    res = await a.structured(system="sys", user="u", schema=ScribeOutput, ctx=CTX)
    assert res.status == "ok" and calls == ["json_schema", "json_object"]
    await a.structured(system="sys", user="u", schema=ScribeOutput, ctx=CTX)
    assert calls[-1] == "json_object"  # remembers the server can't do json_schema


async def test_invalid_json_is_a_parse_error_not_a_crash():
    def handler(req):
        body = json.loads(req.content)
        if body["response_format"]["type"] == "json_schema":
            return httpx2.Response(400, json={"error": {"message": "response_format unsupported"}})
        return httpx2.Response(200, json=completion('{"situation": 1}'))

    res = await adapter(handler).structured(system="sys", user="u", schema=ScribeOutput, ctx=CTX)
    assert res.parsed is None and res.status == "parse_error"


def test_model_routing():
    s = make_settings(magi_mode="auto", openai_api_key="k", openai_model="gpt-x", model_casper="anthropic:claude-opus-5-5")
    assert s.provider == "openai" and s.mode == "live"
    assert s.model_for("MELCHIOR") == ("openai", "gpt-x")
    assert s.model_for("CASPER") == ("anthropic", "claude-opus-5-5")
    assert make_settings(magi_mode="auto").mode == "scripted"


def response(output: list, rid: str) -> dict:
    return {"id": rid, "object": "response", "created_at": 0, "model": "fake-model", "status": "completed",
            "output": output, "parallel_tool_calls": True, "tool_choice": "auto", "tools": [],
            "usage": {"input_tokens": 20, "output_tokens": 10, "total_tokens": 30,
                      "input_tokens_details": {"cached_tokens": 0}, "output_tokens_details": {"reasoning_tokens": 5}}}


async def test_responses_api_runs_native_tools_then_parses_answer():
    from magi.agents.tools import openai_tools

    requests = []

    def handler(req):
        body = json.loads(req.content)
        requests.append(body)
        if len(requests) == 1:
            return httpx2.Response(200, json=response([{
                "type": "function_call", "id": "fc_1", "call_id": "call_1", "name": "check_ip_allowlist",
                "arguments": json.dumps({"ip": "185.220.101.47"}), "status": "completed"}], "resp_1"))
        return httpx2.Response(200, json=response([{
            "type": "message", "id": "msg_1", "role": "assistant", "status": "completed",
            "content": [{"type": "output_text", "text": json.dumps(GOOD), "annotations": []}]}], "resp_2"))

    ran = []

    async def runner(name, args):
        ran.append((name, args))
        return "[E-105] NOT on allowlist"

    a = adapter(handler, base_url="")  # official OpenAI => Responses API
    tools = openai_tools("BALTHASAR")
    res = await a.structured(system="sys", user="u", schema=ScribeOutput, ctx=CTX, tools=tools, tool_runner=runner)

    assert res.status == "ok" and res.parsed.crux == "c" and res.detail == "1 tool call(s)"
    assert ran == [("check_ip_allowlist", {"ip": "185.220.101.47"})]
    assert {t["name"] for t in requests[0]["tools"]} == {"query_siem", "check_ip_allowlist", "get_process_list",
                                                         "get_replication_state"}  # only BALTHASAR's own tools
    assert requests[0]["max_output_tokens"] >= 4000
    assert requests[1]["previous_response_id"] == "resp_1"
    assert requests[1]["input"] == [{"type": "function_call_output", "call_id": "call_1",
                                     "output": "[E-105] NOT on allowlist"}]
    assert res.input_tokens == 40  # usage summed across the tool loop


async def test_tool_budget_forces_an_answer():
    calls = []

    def handler(req):
        body = json.loads(req.content)
        calls.append(body)
        if body.get("tool_choice") != "none":
            return httpx2.Response(200, json=response([{
                "type": "function_call", "id": f"fc_{len(calls)}", "call_id": f"c{len(calls)}",
                "name": "query_siem", "arguments": "{\"target\": \"db-7\"}", "status": "completed"}], f"r{len(calls)}"))
        return httpx2.Response(200, json=response([{
            "type": "message", "id": "m", "role": "assistant", "status": "completed",
            "content": [{"type": "output_text", "text": json.dumps(GOOD), "annotations": []}]}], "final"))

    async def runner(name, args):
        return "[E-1] data"

    a = OpenAICompatAdapter("fake-model", "k", "", http_client=openai.DefaultAsyncHttpxClient(
        transport=httpx2.MockTransport(handler)), max_tool_calls=2)
    res = await a.structured(system="s", user="u", schema=ScribeOutput, ctx=CTX,
                             tools=[{"type": "function", "name": "query_siem", "parameters": {}}], tool_runner=runner)
    assert res.status == "ok" and len(calls) == 3 and calls[-1]["tool_choice"] == "none"
