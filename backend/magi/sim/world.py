"""Simulated production world: state, continuous dynamics, and action effects."""

from __future__ import annotations

import ast
import copy
import operator
import re
from typing import Any

from magi.models import ActionCall

_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}


def get_path(state: dict[str, Any], path: str, default: Any = None) -> Any:
    cur: Any = state
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return default
        cur = cur[part]
    return cur


def set_path(state: dict[str, Any], path: str, value: Any) -> None:
    parts = path.split(".")
    cur = state
    for part in parts[:-1]:
        cur = cur.setdefault(part, {})
    cur[parts[-1]] = value


def eval_expr(expr: str, state: dict[str, Any]) -> float:
    """Tiny arithmetic evaluator over world paths: '=clusters.pay-db.replication_lag_s * 27'."""
    paths = sorted(set(re.findall(r"[A-Za-z_][A-Za-z0-9_\-]*(?:\.[A-Za-z0-9_\-]+)+", expr)), key=len, reverse=True)
    names: dict[str, float] = {}
    for i, p in enumerate(paths):
        var = f"v{i}"
        names[var] = float(get_path(state, p, 0) or 0)
        expr = expr.replace(p, var)

    def ev(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return ev(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        if isinstance(node, ast.Name) and node.id in names:
            return names[node.id]
        if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
            return _OPS[type(node.op)](ev(node.left), ev(node.right))
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -ev(node.operand)
        raise ValueError(f"unsupported expression: {expr}")

    return ev(ast.parse(expr, mode="eval"))


def render_template(text: str, state: dict[str, Any]) -> str:
    """'{clusters.pay-db.replication_lag_s:.0f}' -> '45'."""

    def sub(m: re.Match) -> str:
        val = get_path(state, m.group(1))
        if val is None:
            return m.group(0)
        fmt = m.group(2)
        try:
            return format(val, fmt) if fmt else str(val)
        except (TypeError, ValueError):
            return str(val)

    return re.sub(r"\{([A-Za-z0-9_\-]+(?:\.[A-Za-z0-9_\-]+)+)(?::([^}]+))?\}", sub, text)


class World:
    def __init__(self, initial: dict[str, Any], dynamics: list[dict] | None = None, effects: dict | None = None):
        self.state: dict[str, Any] = copy.deepcopy(initial)
        self.state.setdefault("flags", {})
        # rate: per sim-minute change, applied continuously
        self.rates: dict[str, dict] = {d["path"]: dict(d) for d in (dynamics or [])}
        self.ramps: dict[str, dict] = {}
        self.effects = effects or {}

    def advance(self, dt_sim: float) -> None:
        for path, r in self.rates.items():
            cur = float(get_path(self.state, path, 0) or 0)
            new = cur + float(r.get("per_min", 0)) * dt_sim / 60.0
            lo, hi = r.get("min"), r.get("max")
            if lo is not None:
                new = max(float(lo), new)
            if hi is not None:
                new = min(float(hi), new)
            set_path(self.state, path, new)
        done = []
        for path, rp in self.ramps.items():
            cur = float(get_path(self.state, path, 0) or 0)
            remaining = rp["remaining_s"]
            if remaining <= dt_sim:
                set_path(self.state, path, rp["to"])
                done.append(path)
                continue
            step = (rp["to"] - cur) * dt_sim / remaining
            set_path(self.state, path, cur + step)
            rp["remaining_s"] = remaining - dt_sim
        for path in done:
            del self.ramps[path]

    def _matching_effects(self, action: ActionCall) -> list[dict]:
        out = []
        for key, eff in self.effects.items():
            if key == action.action_id:
                out.append(eff)
            elif key.startswith(action.action_id + "(") and key.endswith(")"):
                want = dict(kv.split("=", 1) for kv in key[len(action.action_id) + 1 : -1].split(",") if "=" in kv)
                if all(action.p.get(k) == v for k, v in want.items()):
                    out.append(eff)
        return out

    def apply(self, action: ActionCall) -> list[str]:
        """Apply an executed action's effects. Returns a short list of what changed."""
        changes: list[str] = []
        for eff in self._matching_effects(action):
            for path, val in (eff.get("set") or {}).items():
                if isinstance(val, str) and val.startswith("="):
                    val = round(eval_expr(val[1:], self.state), 2)
                set_path(self.state, path, val)
                changes.append(f"{path} = {val}")
            for path, spec in (eff.get("ramp") or {}).items():
                self.ramps[path] = {"to": float(spec["to"]), "remaining_s": float(spec.get("over_s", 60))}
                changes.append(f"{path} → {spec['to']} over {spec.get('over_s', 60)}s")
            for path, spec in (eff.get("rate") or {}).items():
                if spec is None:
                    self.rates.pop(path, None)
                    changes.append(f"{path} rate stopped")
                else:
                    self.rates[path] = {"path": path, **spec}
                    changes.append(f"{path} rate {spec.get('per_min')}/min")
        return changes

    def snapshot(self) -> dict[str, Any]:
        return copy.deepcopy(self.state)
