from __future__ import annotations

import json
import os
import tempfile
from dataclasses import asdict
from pathlib import Path

import streamlit as st

from agents.document_intelligence import DocumentIntelligenceAgent
from agents.job_research import JobResearchAgent
from agents.product_design import ProductDesignAgent

ROOT = Path(__file__).resolve().parent

st.set_page_config(page_title="Agentic AI Builder Portfolio", layout="wide")
st.title("Agentic AI Builder Portfolio")
st.caption("Three inspectable prototypes: document intelligence, job research, and product/technical design.")

mode = st.sidebar.radio("Mode", ["mock", "live"], index=0)
os.environ["AGENT_MODE"] = mode
if mode == "live":
    st.sidebar.info("Set ANTHROPIC_API_KEY in your environment before launching Streamlit.")
    st.sidebar.text_input("Model", value=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5"), key="model")
    os.environ["ANTHROPIC_MODEL"] = st.session_state.model


tab1, tab2, tab3, tab4 = st.tabs(["Document Intelligence", "Job Research", "Product Design", "Architecture / Proof"])

with tab1:
    st.subheader("Document Intelligence Agent")
    st.write("Upload evidence, retrieve relevant chunks, synthesize with explicit citations, and inspect contradictions.")
    uploaded = st.file_uploader("Upload TXT / MD / PDF / DOCX files", accept_multiple_files=True, key="docs")
    question = st.text_input("Question", "Compare availability targets and postmortem timing. Where do the sources conflict?")
    if st.button("Run document agent"):
        paths = []
        tmpdir = tempfile.mkdtemp(prefix="doc-agent-")
        if uploaded:
            for f in uploaded:
                p = Path(tmpdir) / f.name
                p.write_bytes(f.read())
                paths.append(p)
        else:
            paths = [ROOT / "demo_data/policy_a.txt", ROOT / "demo_data/policy_b.txt"]
        agent = DocumentIntelligenceAgent(paths, trace_dir=ROOT / "traces")
        result = agent.answer(question)
        st.markdown(result.answer)
        st.markdown("**Retrieved evidence**")
        for ev in result.evidence:
            with st.expander(f"{ev.chunk_id} · score {ev.score}"):
                st.write(ev.text)
        st.json(result.evals)
        st.caption(f"Trace: {result.trace_path}")

with tab2:
    st.subheader("Research / Job Discovery Agent")
    st.write("Separates discovery, evidence extraction, fit scoring, gap analysis, and prioritization.")
    resume_text = st.text_area("Resume evidence", (ROOT / "demo_data/resume_excerpt.txt").read_text(encoding="utf-8"), height=260)
    query = st.text_input("Search intent", "infrastructure reliability distributed systems ai ml developer platform", key="jobq")
    if st.button("Run job agent"):
        agent = JobResearchAgent(ROOT / "demo_data/jobs.json", resume_text, trace_dir=ROOT / "traces")
        matches = agent.rank(query, top_k=4)
        for m in matches:
            st.markdown(f"### {m.job.title} — {m.job.company} ({m.score}%)")
            st.write(m.rationale)
            c1, c2 = st.columns(2)
            c1.write({"matched": m.matched_terms})
            c2.write({"gaps": m.gaps})
        st.caption(f"Trace: {agent.logger.path}")

with tab3:
    st.subheader("Product / Technical Design Agent")
    brief = st.text_area("Product brief", (ROOT / "demo_data/product_brief.txt").read_text(encoding="utf-8"), height=220)
    if st.button("Run product design agent"):
        agent = ProductDesignAgent(trace_dir=ROOT / "traces")
        design = agent.design(brief)
        st.json(asdict(design))
        st.caption(f"Trace: {design.trace_path}")

with tab4:
    st.subheader("What this proves")
    st.markdown(
        """
- **Grounding:** local retrieval before synthesis; evidence IDs remain inspectable.
- **Agent decomposition:** product design uses discovery → architecture → evaluation → red-team stages.
- **Tool-like boundaries:** job research separates discovery, evidence extraction, scoring, and prioritization.
- **Evaluation:** outputs are checked for citations, schema completeness, and expected ranking behavior.
- **Observability:** every important step produces a JSONL trace with inputs, outputs, and latency.
- **Human control:** consequential product actions are explicitly modeled behind approval gates.
- **Reliability:** deterministic mock mode supports repeatable demos when external APIs are unavailable.
        """
    )
    st.code("python demo.py all\n# or\nstreamlit run app.py", language="bash")
