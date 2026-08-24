from __future__ import annotations

from dataclasses import asdict
import html
import os
from pathlib import Path
from typing import Any

import streamlit as st

from agents.document_intelligence import DocumentIntelligenceAgent
from ui.demo_adapters import CATALOG, CATALOG_BY_SLUG, run_product, verify_catalog

ROOT = Path(__file__).resolve().parent

st.set_page_config(
    page_title="Ash Intelligence · Interactive Systems Lab",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
.block-container {max-width: 1240px; padding-top: 2rem; padding-bottom: 4rem;}
[data-testid="stSidebar"] {border-right: 1px solid rgba(120,120,140,.20);}
.ash-eyebrow {font-size:.76rem; letter-spacing:.12em; font-weight:800; opacity:.62; text-transform:uppercase;}
.ash-hero {font-size:clamp(2.6rem,7vw,5.8rem); line-height:.92; letter-spacing:-.055em; font-weight:900; margin:.35rem 0 1rem;}
.ash-sub {font-size:1.08rem; max-width:800px; opacity:.78; margin-bottom:1.25rem;}
.ash-pill {display:inline-block; border:1px solid rgba(120,120,140,.28); border-radius:999px; padding:.32rem .62rem; margin:.15rem .3rem .15rem 0; font-size:.78rem; opacity:.78;}
.ash-answer {padding:1rem 1.15rem; border-radius:14px; border:1px solid rgba(120,120,140,.25); background:rgba(120,120,140,.06);}
</style>
""",
    unsafe_allow_html=True,
)


def _safe_html_text(value: Any) -> str:
    return html.escape(str(value)).replace("\n", "<br>")


def _set_product(slug: str | None) -> None:
    st.session_state["selected_product"] = slug
    if slug:
        st.query_params["product"] = slug
    elif "product" in st.query_params:
        del st.query_params["product"]


def _open_product(slug: str) -> None:
    _set_product(slug)
    st.rerun()


def _status(value: Any) -> None:
    text = str(value)
    positive = {"SHIP", "ALLOW", "ANSWER", "PASS", "PRODUCTION", "CANARY", "READY", "TRUE", "IMPROVING"}
    caution = {"REVIEW", "TUNE", "HOLD", "SIMPLIFY", "ESCALATE", "ASSISTED-AGENT", "STABLE", "APPROVAL_REQUIRED"}
    negative = {"STOP", "BLOCK", "DENY", "SEV0", "SEV1", "FALSE", "DEGRADING"}
    upper = text.upper()
    if upper in positive:
        st.success(text)
    elif upper in negative:
        st.error(text)
    elif upper in caution:
        st.warning(text)
    else:
        st.info(text)


def _result_panel(slug: str, result: Any) -> None:
    st.markdown("### Result")
    if isinstance(result, dict):
        if slug == "support-knowledge-os":
            _status(result.get("status", ""))
            if result.get("answer"):
                safe_answer = _safe_html_text(result["answer"])
                st.markdown(f'<div class="ash-answer"><b>Answer</b><br>{safe_answer}</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            c1.metric("Confidence", result.get("confidence", 0))
            sources = ", ".join(result.get("sources", [])) or "—"
            c2.markdown(f"**Sources**  \n{sources}")
            return

        if slug == "agentic-product-control-plane":
            c1, c2 = st.columns(2)
            with c1:
                st.caption("TOOL AUTHORIZATION")
                _status(result["tool_authorization"]["decision"])
                st.write(result["tool_authorization"].get("reason", ""))
            with c2:
                st.caption("ROLLOUT")
                _status(result["rollout"]["state"])
                st.write(result["rollout"].get("next_action", ""))
            with st.expander("Audit trail", expanded=True):
                st.json(result["audit"])
            return

        if slug == "mautam-evaluation":
            c1, c2, c3 = st.columns(3)
            c1.metric("MAUTAM score", result.get("score"))
            with c2:
                st.caption("DECISION")
                _status(result.get("decision"))
            c3.metric("Weakest lens", str(result.get("weakest_lens", "")).replace("_", " ").title())
            if result.get("gate_failures"):
                st.error("Gate failures: " + ", ".join(result["gate_failures"]))
            st.bar_chart(result.get("lens_scores", {}))
            with st.expander("Full evaluation"):
                st.json(result)
            return

        if slug == "fraud-signal-decision-engine":
            c1, c2 = st.columns(2)
            c1.metric("Risk score", result.get("score"))
            with c2:
                st.caption("DECISION")
                _status(result.get("action"))
            st.write("**Top reason codes:**", ", ".join(result.get("top_contributors", [])) or "none")
            st.bar_chart(result.get("contributions", {}))
            with st.expander("Decision details"):
                st.json(result)
            return

        if slug == "incident-triage-agent":
            c1, c2, c3 = st.columns(3)
            with c1:
                st.caption("SEVERITY")
                _status(result.get("severity"))
            c2.metric("Owner", result.get("owner"))
            c3.metric("Triage score", result.get("score"))
            st.write("**Next action:**", result.get("next_action"))
            st.write("**Matched terms:**", ", ".join(result.get("matched_terms", [])) or "none")
            return

        if slug == "prfaq-product-spec-agent":
            st.markdown(f"## {result.get('headline', '')}")
            st.write("**Customer:**", result.get("customer"))
            st.write("**Problem:**", result.get("problem"))
            st.write("**Promise:**", result.get("promise"))
            c1, c2 = st.columns(2)
            with c1:
                st.write("**Metrics**")
                for x in result.get("metrics", []):
                    st.write("•", x)
            with c2:
                st.write("**Risks / constraints**")
                for x in result.get("risks", []):
                    st.write("•", x)
            st.write("**Open questions**")
            for x in result.get("questions", []):
                st.write("•", x)
            return

        if slug in {"experiment-analysis-copilot", "payment-provider-onboarding", "rag-quality-gate", "retrieval-eval-benchmark", "tool-permission-policy-engine"}:
            primary = None
            for key in ("decision", "status", "action", "ready"):
                if key in result:
                    primary = result[key]
                    break
            if primary is not None:
                _status(primary)
            st.json(result)
            return

        st.json(result)
        return

    if isinstance(result, list):
        if result and isinstance(result[0], dict):
            st.dataframe(result, use_container_width=True, hide_index=True)
        else:
            st.write(result)
        return

    st.write(result)


def _render_field(slug: str, field: dict[str, Any]) -> Any:
    key = f"demo:{slug}:{field['name']}"
    kind = field["kind"]
    label = field["label"]
    default = field["default"]
    if kind == "slider":
        return st.slider(label, min_value=field["min"], max_value=field["max"], value=default, step=field["step"], key=key)
    if kind == "number":
        return st.number_input(label, min_value=field.get("min"), max_value=field.get("max"), value=default, step=field.get("step", 1), key=key)
    if kind == "checkbox":
        return st.checkbox(label, value=default, key=key)
    if kind == "select":
        options = field["options"]
        index = options.index(default) if default in options else 0
        return st.selectbox(label, options=options, index=index, key=key)
    if kind == "multiselect":
        return st.multiselect(label, options=field["options"], default=default, key=key)
    if kind == "textarea":
        return st.text_area(label, value=default, height=120 if len(str(default)) < 220 else 180, key=key)
    return st.text_input(label, value=str(default), key=key)


def _render_product(slug: str) -> None:
    item = CATALOG_BY_SLUG[slug]
    top_left, top_right = st.columns([1, .25])
    with top_left:
        st.markdown(f'<div class="ash-eyebrow">{item["category"]}</div>', unsafe_allow_html=True)
        st.markdown(f"# {item['title']}")
        st.write(item["summary"])
    with top_right:
        if st.button("← All systems", use_container_width=True):
            _set_product(None)
            st.rerun()

    st.markdown('<span class="ash-pill">Original Python engine</span><span class="ash-pill">Synthetic/public-safe inputs</span><span class="ash-pill">No API key required</span>', unsafe_allow_html=True)

    payload: dict[str, Any] = {}
    with st.form(f"product-form-{slug}", border=True):
        for field in item["fields"]:
            payload[field["name"]] = _render_field(slug, field)
        submitted = st.form_submit_button("Run product", type="primary", use_container_width=True)

    result_key = f"demo-result:{slug}"
    error_key = f"demo-error:{slug}"
    if submitted:
        try:
            st.session_state[result_key] = run_product(slug, payload)
            st.session_state.pop(error_key, None)
        except Exception as exc:
            st.session_state[error_key] = f"{type(exc).__name__}: {exc}"
            st.session_state.pop(result_key, None)

    if error_key in st.session_state:
        st.error(st.session_state[error_key])
    if result_key in st.session_state:
        _result_panel(slug, st.session_state[result_key])

    st.divider()
    st.markdown("### What this demonstrates")
    st.write("The UI is only an interaction layer. The decision or analysis above is produced by the same engine under `projects/` that is exercised by the repository's automated checks.")
    st.page_link(f"https://github.com/AshIntelligence/agenticmine/tree/main/projects/{slug}", label="View source + architecture ↗")


def _render_grounded_agent() -> None:
    st.markdown('<div class="ash-eyebrow">BONUS AGENT PLAYGROUND</div>', unsafe_allow_html=True)
    st.markdown("# Ask a grounded document agent")
    st.write("Ask a natural-language question over two synthetic policy documents. The agent retrieves evidence first, answers from that evidence, cites the chunks, and exposes its evaluation trace.")

    question = st.text_input("Question", value="What availability targets do the documents specify, and where do they conflict?", key="grounded-agent-question")
    if st.button("Ask agent", type="primary", use_container_width=True):
        old_mode = os.environ.get("AGENT_MODE")
        os.environ["AGENT_MODE"] = "mock"
        try:
            agent = DocumentIntelligenceAgent([ROOT / "demo_data/policy_a.txt", ROOT / "demo_data/policy_b.txt"], trace_dir=ROOT / "traces")
            st.session_state["grounded-agent-result"] = asdict(agent.answer(question))
        finally:
            if old_mode is None:
                os.environ.pop("AGENT_MODE", None)
            else:
                os.environ["AGENT_MODE"] = old_mode

    result = st.session_state.get("grounded-agent-result")
    if result:
        safe_answer = _safe_html_text(result["answer"])
        st.markdown(f'<div class="ash-answer">{safe_answer}</div>', unsafe_allow_html=True)
        st.markdown("### Retrieved evidence")
        for ev in result["evidence"]:
            with st.expander(f"{ev['chunk_id']} · {Path(ev['source']).name} · score {ev['score']}"):
                st.write(ev["text"])
        st.markdown("### Evaluation")
        st.json(result["evals"])


query_product = st.query_params.get("product")
if isinstance(query_product, list):
    query_product = query_product[0] if query_product else None
if query_product in CATALOG_BY_SLUG:
    st.session_state["selected_product"] = query_product

selected = st.session_state.get("selected_product")

with st.sidebar:
    st.markdown("## Ash Intelligence")
    st.caption("Interactive Systems Lab")
    if st.button("⌂ Demo Hub", use_container_width=True):
        _set_product(None)
        st.rerun()
    if st.button("✦ Ask an Agent", use_container_width=True):
        st.session_state["selected_product"] = "__agent__"
        if "product" in st.query_params:
            del st.query_params["product"]
        st.rerun()
    st.divider()
    title_by_slug = {item["slug"]: item["title"] for item in CATALOG}
    options = ["— Select a product —"] + [title_by_slug[item["slug"]] for item in CATALOG]
    choice = st.selectbox("Jump to a product", options, index=0, key="product-jump")
    if choice != options[0]:
        target = next(slug for slug, title in title_by_slug.items() if title == choice)
        if target != selected:
            _set_product(target)
            st.rerun()
    st.divider()
    st.page_link("https://github.com/AshIntelligence/agenticmine", label="GitHub source ↗")
    st.page_link("https://ashbaskaran.netlify.app/", label="Portfolio ↗")

if selected == "__agent__":
    _render_grounded_agent()
elif selected in CATALOG_BY_SLUG:
    _render_product(selected)
else:
    check = verify_catalog()
    st.markdown('<div class="ash-eyebrow">ASH INTELLIGENCE · INTERACTIVE SYSTEMS LAB</div>', unsafe_allow_html=True)
    st.markdown('<div class="ash-hero">Touch the product.<br>Change the decision.</div>', unsafe_allow_html=True)
    st.markdown('<div class="ash-sub">Twenty runnable AI/product system prototypes, now exposed as interactive product experiences. Ask a question, change a risk signal, rank a feed, test a rollout gate, reconcile billing, or generate a product spec.</div>', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Interactive systems", check["count"])
    m2.metric("Engine coverage", "20 / 20" if not check["missing"] else "Check failed")
    m3.metric("Public-safe mode", "Deterministic")
    m4.metric("Agent playground", "Grounded Q&A")

    if check["missing"] or not check["unique"]:
        st.error(f"Catalog integrity issue: {check}")

    search = st.text_input("Find a system", placeholder="Try: risk, RAG, finance, agent, experiment…")
    categories = ["All"] + sorted({item["category"] for item in CATALOG})
    category = st.segmented_control("Category", categories, default="All")

    filtered = []
    for item in CATALOG:
        haystack = f"{item['title']} {item['summary']} {item['category']}".lower()
        if search and search.lower() not in haystack:
            continue
        if category and category != "All" and item["category"] != category:
            continue
        filtered.append(item)

    st.markdown("## Interactive products")
    cols = st.columns(3)
    for index, item in enumerate(filtered):
        with cols[index % 3]:
            with st.container(border=True):
                st.caption(item["category"].upper())
                st.markdown(f"### {item['title']}")
                st.write(item["summary"])
                if st.button("Open product →", key=f"open:{item['slug']}", use_container_width=True):
                    _open_product(item["slug"])

    st.divider()
    with st.container(border=True):
        c1, c2 = st.columns([1.2, .8])
        with c1:
            st.markdown("## Ask an actual agent")
            st.write("A grounded document-intelligence agent is also wired into the hub. Type a question, retrieve evidence, get a cited answer, and inspect the eval trace.")
        with c2:
            if st.button("Open grounded Q&A →", type="primary", use_container_width=True):
                st.session_state["selected_product"] = "__agent__"
                st.rerun()

    st.caption("All product interactions use synthetic or public-safe inputs. The 20 system cards call the original engines under `projects/`; the UI does not reimplement their decision logic.")
