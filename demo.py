from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from agents.document_intelligence import DocumentIntelligenceAgent
from agents.job_research import JobResearchAgent
from agents.product_design import ProductDesignAgent

ROOT = Path(__file__).resolve().parent


def demo_docs() -> None:
    agent = DocumentIntelligenceAgent([ROOT / "demo_data/policy_a.txt", ROOT / "demo_data/policy_b.txt"], trace_dir=ROOT / "traces")
    result = agent.compare("availability targets, incident leadership timing, postmortem timing, and automated remediation")
    print("\n=== DOCUMENT INTELLIGENCE ===")
    print(result.answer)
    print(f"\nTrace: {result.trace_path}")


def demo_ranking() -> None:
    profile = (ROOT / "demo_data/candidate_profile.txt").read_text(encoding="utf-8")
    agent = JobResearchAgent(ROOT / "demo_data/jobs.json", profile, trace_dir=ROOT / "traces")
    ranked = agent.rank("infrastructure reliability distributed systems ai ml developer platform", top_k=3)
    print("\n=== RESEARCH & RANKING ===")
    for i, match in enumerate(ranked, 1):
        print(f"{i}. {match.job.title} — {match.job.company}: {match.score}%")
        print(f"   matched={match.matched_terms}")
        print(f"   gaps={match.gaps}")
    print(f"\nTrace: {agent.logger.path}")


def demo_product() -> None:
    brief = (ROOT / "demo_data/product_brief.txt").read_text(encoding="utf-8")
    agent = ProductDesignAgent(trace_dir=ROOT / "traces")
    design = agent.design(brief)
    print("\n=== PRODUCT / TECHNICAL DESIGN ===")
    print(json.dumps(asdict(design), indent=2))
    print(f"\nTrace: {design.trace_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Agentic AI Builder Portfolio")
    parser.add_argument("demo", nargs="?", choices=["docs", "ranking", "product", "all"], default="all")
    args = parser.parse_args()
    if args.demo in {"docs", "all"}:
        demo_docs()
    if args.demo in {"ranking", "all"}:
        demo_ranking()
    if args.demo in {"product", "all"}:
        demo_product()


if __name__ == "__main__":
    main()
