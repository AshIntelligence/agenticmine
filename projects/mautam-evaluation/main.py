"""MAUTAM AI product evaluation.

Model & Response Quality · Adoption · User Workflow Success · Trust & Controls ·
Availability & Health · Measurable Business Impact.

A deterministic product-level evaluation harness that combines weighted product
signals with hard release gates and windowed trend checks.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from statistics import mean, pstdev
import json
import sys
from typing import Iterable

WEIGHTS = {
    "model_quality": .18,
    "adoption": .15,
    "workflow_success": .20,
    "trust_controls": .18,
    "availability_health": .12,
    "business_impact": .17,
}


@dataclass(frozen=True)
class GatePolicy:
    min_trust: float = .60
    min_availability: float = .55
    ship_score: float = .80
    ship_floor: float = .65
    tune_score: float = .62


@dataclass(frozen=True)
class Result:
    score: float
    decision: str
    weakest_lens: str
    lens_scores: dict
    rationale: tuple
    gate_failures: tuple = ()
    contributions: dict = field(default_factory=dict)


DEFAULT_POLICY = GatePolicy()


def _clean_lenses(lenses: dict) -> dict[str, float]:
    missing = set(WEIGHTS) - set(lenses)
    if missing:
        raise ValueError(f"missing lenses: {sorted(missing)}")
    return {k: max(0.0, min(1.0, float(lenses[k]))) for k in WEIGHTS}


def evaluate(lenses: dict, policy: GatePolicy = DEFAULT_POLICY) -> Result:
    """Evaluate one product snapshot while preserving hard safety/reliability gates."""
    clean = _clean_lenses(lenses)
    contributions = {k: clean[k] * WEIGHTS[k] for k in WEIGHTS}
    score = sum(contributions.values())
    weakest = min(clean, key=clean.get)

    gate_failures = []
    if clean["trust_controls"] < policy.min_trust:
        gate_failures.append("trust-controls-below-gate")
    if clean["availability_health"] < policy.min_availability:
        gate_failures.append("availability-health-below-gate")

    if gate_failures:
        decision = "STOP"
    elif score >= policy.ship_score and min(clean.values()) >= policy.ship_floor:
        decision = "SHIP"
    elif score >= policy.tune_score:
        decision = "TUNE"
    else:
        decision = "SIMPLIFY"

    rationale = (
        f"weighted score={score:.2f}",
        f"weakest={weakest}:{clean[weakest]:.2f}",
        f"gate_failures={','.join(gate_failures) if gate_failures else 'none'}",
    )
    return Result(
        round(score, 3),
        decision,
        weakest,
        clean,
        rationale,
        tuple(gate_failures),
        {k: round(v, 3) for k, v in contributions.items()},
    )


def evaluate_window(samples: Iterable[dict], policy: GatePolicy = DEFAULT_POLICY) -> dict:
    """Evaluate a window of product snapshots and expose volatility + direction."""
    rows = [_clean_lenses(row) for row in samples]
    if not rows:
        raise ValueError("samples must not be empty")

    averages = {k: mean(row[k] for row in rows) for k in WEIGHTS}
    volatility = {k: pstdev(row[k] for row in rows) if len(rows) > 1 else 0.0 for k in WEIGHTS}
    current = evaluate(averages, policy)

    first_score = sum(rows[0][k] * WEIGHTS[k] for k in WEIGHTS)
    last_score = sum(rows[-1][k] * WEIGHTS[k] for k in WEIGHTS)
    delta = last_score - first_score
    trend = "IMPROVING" if delta > .03 else "DEGRADING" if delta < -.03 else "STABLE"

    return {
        "sample_count": len(rows),
        "decision": current.decision,
        "score": current.score,
        "trend": trend,
        "score_delta": round(delta, 3),
        "weakest_lens": current.weakest_lens,
        "gate_failures": list(current.gate_failures),
        "averages": {k: round(v, 3) for k, v in averages.items()},
        "volatility": {k: round(v, 3) for k, v in volatility.items()},
    }


def self_test():
    assert evaluate({k: .9 for k in WEIGHTS}).decision == "SHIP"
    x = {k: .9 for k in WEIGHTS}
    x["trust_controls"] = .4
    stopped = evaluate(x)
    assert stopped.decision == "STOP"
    assert "trust-controls-below-gate" in stopped.gate_failures

    window = evaluate_window([
        {k: .70 for k in WEIGHTS},
        {k: .80 for k in WEIGHTS},
        {k: .90 for k in WEIGHTS},
    ])
    assert window["trend"] == "IMPROVING"
    assert window["sample_count"] == 3


def demo():
    sample = {
        "model_quality": .88,
        "adoption": .74,
        "workflow_success": .82,
        "trust_controls": .91,
        "availability_health": .79,
        "business_impact": .77,
    }
    print(json.dumps(asdict(evaluate(sample)), indent=2))
    print(json.dumps(evaluate_window([
        {**sample, "adoption": .66, "workflow_success": .75},
        sample,
        {**sample, "adoption": .79, "workflow_success": .86},
    ]), indent=2))


if __name__ == "__main__":
    self_test() if "--test" in sys.argv else demo()
