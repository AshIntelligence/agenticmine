from pathlib import Path

from agents.document_intelligence import DocumentIntelligenceAgent
from agents.job_research import JobResearchAgent
from agents.product_design import ProductDesignAgent

ROOT = Path(__file__).resolve().parents[1]


def test_document_agent_returns_evidence():
    agent = DocumentIntelligenceAgent([ROOT / "demo_data/policy_a.txt", ROOT / "demo_data/policy_b.txt"], trace_dir=ROOT / "traces")
    result = agent.answer("What is the availability target?")
    assert result.evidence
    assert "[" in result.answer


def test_job_agent_ranks_infrastructure_role():
    resume = (ROOT / "demo_data/resume_excerpt.txt").read_text(encoding="utf-8")
    agent = JobResearchAgent(ROOT / "demo_data/jobs.json", resume, trace_dir=ROOT / "traces")
    ranked = agent.rank("infrastructure reliability distributed systems ai ml developer platform", top_k=4)
    assert ranked[0].job.id == "anthropic-tpm-infra"


def test_product_agent_has_human_review():
    brief = (ROOT / "demo_data/product_brief.txt").read_text(encoding="utf-8")
    design = ProductDesignAgent(trace_dir=ROOT / "traces").design(brief)
    assert design.human_review_points
    assert design.eval_plan
