"""Agentic Product Control Plane.

A compact control plane for agent registration, tool authorization, evaluation
gates, cost budgets, incident thresholds, rollout transitions and audit traces.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import sys
from typing import Any


@dataclass(frozen=True)
class AgentSpec:
    name: str
    tools: list[str]
    max_cost: float
    min_eval: float = .75
    requires_approval: list[str] = field(default_factory=list)
    rollout: str = "shadow"
    version: str = "v1"


@dataclass(frozen=True)
class RuntimeSignals:
    eval_score: float
    incident_rate: float
    cost_p95: float


@dataclass(frozen=True)
class RolloutDecision:
    agent: str
    state: str
    blockers: tuple[str, ...]
    tools: tuple[str, ...]
    approval_tools: tuple[str, ...]
    next_action: str
    signals: dict[str, float]


VALID_ROLLOUTS = {"shadow", "canary", "production"}
NEXT_STATE = {"shadow": "CANARY", "canary": "PRODUCTION", "production": "PRODUCTION"}


def authorize_tool(spec: AgentSpec, tool: str, approved: bool = False) -> dict[str, Any]:
    """Return an explicit tool authorization decision."""
    if tool not in spec.tools:
        return {"tool": tool, "decision": "DENY", "reason": "tool-not-registered"}
    if tool in spec.requires_approval and not approved:
        return {"tool": tool, "decision": "REVIEW", "reason": "human-approval-required"}
    return {"tool": tool, "decision": "ALLOW", "reason": "policy-pass"}


def assess_rollout(spec: AgentSpec, signals: RuntimeSignals) -> RolloutDecision:
    """Assess health gates separately from agent registration and tool policy."""
    if spec.rollout not in VALID_ROLLOUTS:
        raise ValueError(f"unsupported rollout state: {spec.rollout}")

    blockers: list[str] = []
    if signals.eval_score < spec.min_eval:
        blockers.append("eval-below-gate")
    if signals.incident_rate > .02:
        blockers.append("incident-rate")
    if signals.cost_p95 > spec.max_cost:
        blockers.append("cost-budget")

    state = "HOLD" if blockers else NEXT_STATE[spec.rollout]
    next_action = (
        "remediate-gates"
        if blockers
        else "hold-production"
        if spec.rollout == "production"
        else f"promote-to-{state.lower()}"
    )
    return RolloutDecision(
        agent=spec.name,
        state=state,
        blockers=tuple(blockers),
        tools=tuple(spec.tools),
        approval_tools=tuple(spec.requires_approval),
        next_action=next_action,
        signals={
            "eval_score": round(signals.eval_score, 4),
            "incident_rate": round(signals.incident_rate, 4),
            "cost_p95": round(signals.cost_p95, 4),
        },
    )


def evaluate_rollout(spec: AgentSpec, eval_score: float, incident_rate: float, cost_p95: float) -> dict:
    """Backward-compatible wrapper used by the browser demo and self-checks."""
    decision = assess_rollout(spec, RuntimeSignals(eval_score, incident_rate, cost_p95))
    result = asdict(decision)
    result["blockers"] = list(decision.blockers)
    result["tools"] = list(decision.tools)
    result["approval_tools"] = list(decision.approval_tools)
    return result


class ControlPlane:
    """In-memory registry with explicit audit events for prototype inspection."""

    def __init__(self) -> None:
        self.registry: dict[str, AgentSpec] = {}
        self.audit: list[dict[str, Any]] = []

    def register(self, spec: AgentSpec) -> None:
        self.registry[spec.name] = spec
        self.audit.append({"event": "register", "agent": spec.name, "version": spec.version})

    def authorize(self, agent: str, tool: str, approved: bool = False) -> dict[str, Any]:
        spec = self.registry[agent]
        decision = authorize_tool(spec, tool, approved)
        self.audit.append({"event": "tool-policy", "agent": agent, **decision})
        return decision

    def assess(self, agent: str, signals: RuntimeSignals) -> dict[str, Any]:
        spec = self.registry[agent]
        decision = evaluate_rollout(
            spec, signals.eval_score, signals.incident_rate, signals.cost_p95
        )
        self.audit.append({
            "event": "rollout-assessment",
            "agent": agent,
            "state": decision["state"],
            "blockers": decision["blockers"],
        })
        return decision


def self_test():
    spec = AgentSpec(
        "a",
        ["search", "refund"],
        1,
        min_eval=.9,
        requires_approval=["refund"],
    )
    assert evaluate_rollout(spec, .7, 0, .1)["state"] == "HOLD"
    canary = AgentSpec("a", [], 1, min_eval=.8, rollout="canary")
    assert evaluate_rollout(canary, .9, 0, .1)["state"] == "PRODUCTION"
    assert authorize_tool(spec, "refund")["decision"] == "REVIEW"
    assert authorize_tool(spec, "refund", approved=True)["decision"] == "ALLOW"
    assert authorize_tool(spec, "delete-account")["decision"] == "DENY"

    plane = ControlPlane()
    plane.register(spec)
    plane.authorize("a", "refund")
    plane.assess("a", RuntimeSignals(.95, .005, .2))
    assert len(plane.audit) == 3


def demo():
    plane = ControlPlane()
    spec = AgentSpec(
        "finance-agent",
        ["search", "draft", "refund"],
        max_cost=.25,
        min_eval=.82,
        requires_approval=["refund"],
        rollout="canary",
    )
    plane.register(spec)
    print(plane.authorize("finance-agent", "refund"))
    print(plane.assess("finance-agent", RuntimeSignals(.89, .005, .19)))
    print({"audit": plane.audit})


if __name__ == "__main__":
    self_test() if "--test" in sys.argv else demo()
