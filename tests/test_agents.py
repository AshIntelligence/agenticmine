import os
from pathlib import Path
import subprocess
import sys

from agents.document_intelligence import DocumentIntelligenceAgent
from agents.job_research import JobResearchAgent
from agents.product_design import ProductDesignAgent

ROOT = Path(__file__).resolve().parents[1]


def test_document_agent_returns_evidence():
    agent = DocumentIntelligenceAgent(
        [ROOT / "demo_data/policy_a.txt", ROOT / "demo_data/policy_b.txt"],
        trace_dir=ROOT / "traces",
    )
    result = agent.answer("What is the availability target?")
    assert result.evidence
    assert "[" in result.answer


def test_ranking_agent_prefers_ai_infra_example():
    profile = (ROOT / "demo_data/example_profile.txt").read_text(encoding="utf-8")
    agent = JobResearchAgent(ROOT / "demo_data/jobs.json", profile, trace_dir=ROOT / "traces")
    ranked = agent.rank("infrastructure reliability distributed systems ai ml developer platform", top_k=4)
    assert ranked[0].job.id == "ai-infra-tpm"


def test_product_agent_has_human_review():
    brief = (ROOT / "demo_data/product_brief.txt").read_text(encoding="utf-8")
    design = ProductDesignAgent(trace_dir=ROOT / "traces").design(brief)
    assert design.human_review_points
    assert design.eval_plan


def test_native_tool_demo_executes_in_mock_mode():
    env = os.environ.copy()
    env["AGENT_MODE"] = "mock"
    result = subprocess.run(
        [sys.executable, str(ROOT / "tool_demo.py")],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stderr
    assert "MOCK TOOL MODE" in result.stdout
