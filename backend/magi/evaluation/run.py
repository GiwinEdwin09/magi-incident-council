"""Evaluation runner.

    uv run python -m magi.evaluation.run --conditions B1,B2,C --runs 1
    uv run python -m magi.evaluation.run --scenarios pm_dormant_flag,syn_phantom_spike --conditions C --runs 3
    uv run python -m magi.evaluation.run --estimate          # count runs and calls, spend nothing

Writes eval_results/<timestamp>/: runs.jsonl (one scored row per run), traces/ (every event of
every run), and summary.json + summary.md (see report.py). Uses the live LLM settings from .env.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import time
from datetime import datetime
from pathlib import Path

from magi.config import get_settings
from magi.evaluation import report
from magi.evaluation.harness import run_b1, run_council
from magi.llm import build_adapters, make_live_adapter
from magi.sim.scenario import list_scenarios, load_scenario

RESULTS = Path(__file__).resolve().parents[2] / "eval_results"


def plan(scenario_ids: list[str], conditions: list[str], runs: int) -> list[tuple[str, str, str, int]]:
    jobs = []
    for sid in scenario_ids:
        sc = load_scenario(sid)
        for dp in sc.decision_points:
            if dp.id not in sc.labels:
                continue
            for cond in conditions:
                for r in range(runs):
                    jobs.append((sid, dp.id, cond, r))
    return jobs


async def one(job: tuple[str, str, str, int], mode: str, out: Path, sem: asyncio.Semaphore, lock: asyncio.Lock,
              done: list[int], total: int) -> None:
    sid, dp_id, cond, r = job
    settings = get_settings()
    sc = load_scenario(sid)
    dp = next(d for d in sc.decision_points if d.id == dp_id)
    async with sem:
        if cond == "B1":
            provider, model = settings.model_for("MELCHIOR")
            adapter = build_adapters(settings, sid, mode=mode)["MELCHIOR"] if mode != "live" else make_live_adapter(settings, provider, model)
            row, trace = await run_b1(sc, dp, settings, adapter)
        else:
            row, trace = await run_council(sc, dp, settings, build_adapters(settings, sid, mode=mode), cond)
    row = {"scenario": sid, "kind": sc.kind, "decision_point": dp_id, "condition": cond, "run": r, **row}
    async with lock:
        with (out / "runs.jsonl").open("a") as f:
            f.write(json.dumps(row) + "\n")
        (out / "traces" / f"{sid}.{dp_id}.{cond}.{r}.json").write_text(json.dumps(trace, default=str))
        done[0] += 1
        flag = "HARMFUL " if row["harmful"] else ""
        print(f"[{done[0]}/{total}] {sid} {dp_id} {cond}#{r}: {row['outcome']} {flag}"
              f"actions={row['actions']} esc_ok={row['escalation_correct']} "
              f"tokens={row['input_tokens'] + row['output_tokens']} {row['wall_s']}s"
              + (f" ERROR {row['error']}" if row.get("error") else ""), flush=True)


async def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scenarios", default="all", help="comma-separated ids, or all")
    ap.add_argument("--conditions", default="B1,B2,C")
    ap.add_argument("--runs", type=int, default=1, help="runs per decision point and condition")
    ap.add_argument("--concurrency", type=int, default=4)
    ap.add_argument("--mode", default="live", choices=["live", "scripted"], help="scripted = offline smoke test (S1/S2 only)")
    ap.add_argument("--out", default="")
    ap.add_argument("--estimate", action="store_true", help="print the run count and exit")
    args = ap.parse_args()

    ids = [s["id"] for s in list_scenarios()] if args.scenarios == "all" else args.scenarios.split(",")
    conditions = [c.strip() for c in args.conditions.split(",") if c.strip()]
    jobs = plan(ids, conditions, args.runs)
    by_cond = {c: sum(1 for j in jobs if j[2] == c) for c in conditions}
    print(f"{len(jobs)} runs over {len({(j[0], j[1]) for j in jobs})} decision points: {by_cond}")
    if args.estimate:
        print("Typical LLM calls per run: B1 = 1, B2 ≈ 10-14, C ≈ 15-30 (more with tool calls and extra rounds).")
        return

    out = Path(args.out) if args.out else RESULTS / datetime.now().strftime("%Y%m%d-%H%M%S")
    (out / "traces").mkdir(parents=True, exist_ok=True)
    settings = get_settings()
    (out / "config.json").write_text(json.dumps({
        "started": datetime.now().isoformat(timespec="seconds"), "mode": args.mode, "conditions": conditions,
        "runs": args.runs, "scenarios": ids,
        "models": {r: ":".join(settings.model_for(r)) for r in ["MELCHIOR", "BALTHASAR", "CASPER", "SCRIBE"]},
        "reasoning_effort": settings.openai_reasoning_effort,
    }, indent=2))
    sem, lock, done = asyncio.Semaphore(args.concurrency), asyncio.Lock(), [0]
    t0 = time.monotonic()
    await asyncio.gather(*(one(j, args.mode, out, sem, lock, done, len(jobs)) for j in jobs))
    summary = report.write(out)
    print(f"\nDone in {time.monotonic() - t0:.0f}s. Results: {out}")
    print(report.headline(summary))


if __name__ == "__main__":
    asyncio.run(main())
