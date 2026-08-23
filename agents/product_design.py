from __future__ import annotations

import time
from dataclasses import dataclass, asdict
from typing import Any

from core.evaluation import schema_fields_present
from core.llm import ClaudeClient
from core.tracing import TraceLogger, traced_step


@dataclass
class ProductDesign:
    problem: str
    users: list[str]
    hypotheses: list[str]
    user_journeys: list[str]
    requirements: list[str]
    architecture: list[str]
    risks: list[str]
    human_review_points: list[str]
    eval_plan: list[str]
    rollout: list[str]
    trace_path: str = ""


class ProductDesignAgent:
    """Multi-stage agent for turning an ambiguous idea into an evaluable technical product design."""

    def __init__(self, trace_dir: str = "traces") -> None:
        self.logger = TraceLogger("product-design", trace_dir)
        self.llm = ClaudeClient()

    def design(self, brief: str) -> ProductDesign:
        discovery = self._discovery(brief)
        architecture = self._architecture(brief, discovery)
        evaluation = self._evaluation(brief, discovery, architecture)
        critique = self._critique(brief, discovery, architecture, evaluation)

        design = ProductDesign(
            problem=discovery["problem"],
            users=discovery["users"],
            hypotheses=discovery["hypotheses"],
            user_journeys=discovery["user_journeys"],
            requirements=architecture["requirements"],
            architecture=architecture["architecture"],
            risks=critique["risks"],
            human_review_points=critique["human_review_points"],
            eval_plan=evaluation["eval_plan"],
            rollout=evaluation["rollout"],
            trace_path=str(self.logger.path),
        )
        eval_result = schema_fields_present(asdict(design), [
            "problem", "users", "user_journeys", "requirements", "architecture",
            "risks", "human_review_points", "eval_plan", "rollout",
        ]).to_dict()
        self.logger.record("evaluate_design_schema", {"brief": brief[:300]}, eval_result, time.time())
        return design

    def _discovery(self, brief: str) -> dict[str, Any]:
        fallback = {
            "problem": brief.strip(),
            "users": ["primary operator", "decision-maker"],
            "hypotheses": ["Structured agent decomposition will reduce repeated manual analysis."],
            "user_journeys": ["Submit goal -> gather context -> generate plan -> verify evidence -> approve consequential action"],
        }
        with traced_step(self.logger, "discovery_agent", brief) as trace:
            result = self.llm.json(
                system="You are a product discovery agent.",
                prompt=f"Identify the problem, users, testable hypotheses, and user journeys for this product brief:\n{brief}",
                fallback=fallback,
            )
            trace.set_output(result)
            return result

    def _architecture(self, brief: str, discovery: dict[str, Any]) -> dict[str, Any]:
        fallback = {
            "requirements": [
                "Ground outputs in retrieved or tool-returned evidence",
                "Use structured outputs between agent stages",
                "Persist trace metadata for debugging and evaluation",
                "Require explicit approval before consequential external actions",
            ],
            "architecture": [
                "User/UI", "Orchestrator", "Retriever + tool registry", "Claude model",
                "State store", "Evaluator", "Human approval gate", "Trace/telemetry store",
            ],
        }
        with traced_step(self.logger, "architecture_agent", discovery) as trace:
            result = self.llm.json(
                system="You are a pragmatic AI systems architect. Favor simple, inspectable components and explicit failure boundaries.",
                prompt=f"Product brief: {brief}\nDiscovery: {discovery}\nDefine requirements and an architecture suitable for an agentic prototype.",
                fallback=fallback,
            )
            trace.set_output(result)
            return result

    def _evaluation(self, brief: str, discovery: dict[str, Any], architecture: dict[str, Any]) -> dict[str, Any]:
        fallback = {
            "eval_plan": [
                "Task completion on a fixed golden set",
                "Grounding/citation correctness",
                "Tool-call success and parameter validity",
                "Latency and model-call count",
                "Human override rate on consequential steps",
                "Failure-mode regression suite",
            ],
            "rollout": ["offline eval", "shadow mode", "small pilot", "expand with telemetry gates"],
        }
        with traced_step(self.logger, "evaluation_agent", architecture) as trace:
            result = self.llm.json(
                system="You are an AI evaluation lead. Define measurable behavioral and operational tests, not vanity metrics.",
                prompt=f"Brief: {brief}\nDiscovery: {discovery}\nArchitecture: {architecture}\nCreate the eval and rollout plan.",
                fallback=fallback,
            )
            trace.set_output(result)
            return result

    def _critique(self, brief: str, discovery: dict[str, Any], architecture: dict[str, Any], evaluation: dict[str, Any]) -> dict[str, Any]:
        fallback = {
            "risks": [
                "Hallucinated or weakly grounded conclusions",
                "Over-agentization where deterministic logic is simpler",
                "Tool or retrieval failure hidden behind fluent output",
                "Latency/cost growth from unnecessary agent loops",
                "Sensitive data exposure through broad tool permissions",
            ],
            "human_review_points": [
                "Before external side effects",
                "When evidence is contradictory or low-confidence",
                "For high-impact recommendations",
            ],
        }
        with traced_step(self.logger, "red_team_agent", evaluation) as trace:
            result = self.llm.json(
                system="You are a skeptical AI product red-team reviewer. Find concrete failure modes and identify where humans must retain control.",
                prompt=f"Brief: {brief}\nDiscovery: {discovery}\nArchitecture: {architecture}\nEvaluation: {evaluation}\nReturn risks and human_review_points.",
                fallback=fallback,
            )
            trace.set_output(result)
            return result
