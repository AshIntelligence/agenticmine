from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from agents.document_intelligence import DocumentIntelligenceAgent
from agents.job_research import JobResearchAgent
from agents.product_design import ProductDesignAgent

ROOT = Path(__file__).resolve().parent
GOLDEN = json.loads((ROOT / "evals/golden_cases.json").read_text(encoding="utf-8"))


def run() -> dict:
    results = {"document_intelligence": [], "research_ranking": [], "product_design": []}

    doc_agent = DocumentIntelligenceAgent(
        [ROOT / "demo_data/policy_a.txt", ROOT / "demo_data/policy_b.txt"],
        trace_dir=ROOT / "traces",
    )
    for case in GOLDEN["document_intelligence"]:
        out = doc_agent.answer(case["question"])
        text = out.answer.lower()
        hits = [term for term in case["expected_terms"] if term.lower() in text]
        passed = len(hits) == len(case["expected_terms"])
        results["document_intelligence"].append({"case": case["question"], "passed": passed, "hits": hits})

    profile = (ROOT / "demo_data/example_profile.txt").read_text(encoding="utf-8")
    ranking_agent = JobResearchAgent(ROOT / "demo_data/jobs.json", profile, trace_dir=ROOT / "traces")
    for case in GOLDEN["research_ranking"]:
        ranked = ranking_agent.rank(case["query"], top_k=4)
        top = ranked[0].job.id if ranked else None
        results["research_ranking"].append({"case": case["query"], "passed": top == case["expected_top_job_id"], "top": top})

    brief = (ROOT / "demo_data/product_brief.txt").read_text(encoding="utf-8")
    design = ProductDesignAgent(trace_dir=ROOT / "traces").design(brief)
    obj = asdict(design)
    required = GOLDEN["product_design"][0]["required_sections"]
    missing = [k for k in required if not obj.get(k)]
    results["product_design"].append({"case": "schema completeness", "passed": not missing, "missing": missing})

    groups = ["document_intelligence", "research_ranking", "product_design"]
    results["summary"] = {
        "passed": sum(1 for group in groups for row in results[group] if row["passed"]),
        "total": sum(len(results[group]) for group in groups),
    }
    return results


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
