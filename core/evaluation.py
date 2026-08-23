from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class EvalResult:
    name: str
    passed: bool
    score: float
    details: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def keyword_coverage(text: str, keywords: list[str], threshold: float = 0.6) -> EvalResult:
    lower = text.lower()
    hits = [k for k in keywords if k.lower() in lower]
    score = len(hits) / max(1, len(keywords))
    return EvalResult("keyword_coverage", score >= threshold, score, f"hits={hits}")


def citation_coverage(text: str, expected_markers: list[str]) -> EvalResult:
    hits = [m for m in expected_markers if m in text]
    score = len(hits) / max(1, len(expected_markers))
    return EvalResult("citation_coverage", score >= 0.5, score, f"markers={hits}")


def schema_fields_present(obj: dict[str, Any], required: list[str]) -> EvalResult:
    missing = [k for k in required if not obj.get(k)]
    score = (len(required) - len(missing)) / max(1, len(required))
    return EvalResult("schema_fields_present", not missing, score, f"missing={missing}")
