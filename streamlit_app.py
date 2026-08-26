from __future__ import annotations

from dataclasses import asdict
import html
import os
from pathlib import Path
from typing import Any

import streamlit as st

from agents.document_intelligence import DocumentIntelligenceAgent
from ui.demo_adapters import CATALOG, CATALOG_BY_SLUG, default_payload, run_product, verify_catalog
from ui.demo_ux import GUIDANCE, SCENARIOS, validate_payload

ROOT = Path(__file__).resolve().parent

PILLAR_BY_SLUG = {
    "agent-vs-workflow-router": "CONTROL",
    "agentic-product-control-plane": "CONTROL",
    "finance-close-orchestrator": "CONTROL",
    "human-in-loop-risk-router": "CONTROL",
    "tool-permission-policy-engine": "CONTROL",
    "mautam-evaluation": "EVALUATE",
    "rag-quality-gate": "EVALUATE",
    "retrieval-eval-benchmark": "EVALUATE",
    "support-knowledge-os": "EVALUATE",
    "telemetry-anomaly-to-action": "EVALUATE",
    "experiment-analysis-copilot": "EVALUATE",
    "voc-synthesis-studio": "EVALUATE",
    "product-prioritization-engine": "EVALUATE",
    "prfaq-product-spec-agent": "EVALUATE",
    "fraud-signal-decision-engine": "DECIDE",
    "payment-provider-onboarding": "DECIDE",
    "billing-reconciliation-observatory": "DECIDE",
    "incident-triage-agent": "DECIDE",
    "linkedin-career-discovery": "DECIDE",
    "instagram-intentional-discovery": "DECIDE",
}

PILLAR_COPY = {
    "CONTROL": {
        "question": "Set the boundary of action.",
        "detail": "Autonomy · permissions · approvals · orchestration · rollout",
        "flagship": "agentic-product-control-plane",
    },
    "EVALUATE": {
        "question": "Measure whether the product works.",
        "detail": "Grounding · evals · adoption · reliability · experiments · impact",
        "flagship": "mautam-evaluation",
    },
    "DECIDE": {
        "question": "Turn evidence and policy into action.",
        "detail": "Risk · fintech · ranking · incidents · policy tradeoffs",
        "flagship": "fraud-signal-decision-engine",
    },
}

FEATURED_SLUGS = [
    "agentic-product-control-plane",
    "mautam-evaluation",
    "fraud-signal-decision-engine",
]

st.set_page_config(
    page_title="Ash Intelligence · Systems Lab",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="auto",
)

st.markdown(
    """
<style>
.block-container {max-width: 1240px; padding-top: 4.25rem; padding-bottom: 4rem;}
.ash-eyebrow {font-size:.84rem; line-height:1.2; letter-spacing:.12em; font-weight:800; opacity:.78; text-transform:uppercase; margin:0 0 .55rem;}
.ash-hero {font-size:clamp(2.6rem,7vw,5.8rem); line-height:.92; letter-spacing:-.055em; font-weight:900; margin:0 0 1rem;}
.ash-sub {font-size:1.08rem; max-width:920px; opacity:.82; margin-bottom:1.25rem;}
.ash-pill {display:inline-block; border:1px solid rgba(120,120,140,.28); border-radius:999px; padding:.32rem .62rem; margin:.15rem .3rem .15rem 0; font-size:.80rem; opacity:.86;}
.ash-answer {padding:1rem 1.15rem; border-radius:14px; border:1px solid rgba(120,120,140,.25); background:rgba(120,120,140,.06);}
.ash-guide {font-size:.92rem; opacity:.88;}
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
        if slug == "telemetry-anomaly-to-action" and not result:
            st.success("No anomalies detected")
            st.caption("No point exceeded the configured anomaly threshold for this series.")
            return
        if result and isinstance(result[0], dict):
            st.dataframe(result, use_container_width=True, hide_index=True)
        else:
            st.write(result)
        return

    st.write(result)


def _field_help(field: dict[str, Any]) -> str | None:
    label = field["label"].lower()
    if "json" in label:
        return "Keep this as valid JSON. Load a sample scenario if you prefer not to edit the JSON directly."
    if "comma separated" in label:
        return "Enter values separated by commas."
    if "one per line" in label or "one passage per line" in label:
        return "Enter one item per line."
    if field["kind"] == "slider" and field.get("min") == 0.0 and field.get("max") == 1.0:
        return "0 is the minimum signal value; 1 is the maximum."
    return None


def _render_field(slug: str, field: dict[str, Any]) -> Any:
    key = f"demo:{slug}:{field['name']}"
    kind = field["kind"]
    label = field["label"]
    default = field["default"]
    help_text = _field_help(field)
    has_state = key in st.session_state

    if kind == "slider":
        kwargs = {"min_value": field["min"], "max_value": field["max"], "step": field["step"], "key": key, "help": help_text}
        if not has_state:
            kwargs["value"] = default
        return st.slider(label, **kwargs)
    if kind == "number":
        kwargs = {"min_value": field.get("min"), "max_value": field.get("max"), "step": field.get("step", 1), "key": key, "help": help_text}
        if not has_state:
            kwargs["value"] = default
        return st.number_input(label, **kwargs)
    if kind == "checkbox":
        kwargs = {"key": key, "help": help_text}
        if not has_state:
            kwargs["value"] = default
        return st.checkbox(label, **kwargs)
    if kind == "select":
        options = field["options"]
        kwargs = {"options": options, "key": key, "help": help_text}
        if not has_state:
            kwargs["index"] = options.index(default) if default in options else 0
        return st.selectbox(label, **kwargs)
    if kind == "multiselect":
        kwargs = {"options": field["options"], "key": key, "help": help_text}
        if not has_state:
            kwargs["default"] = default
        return st.multiselect(label, **kwargs)
    if kind == "textarea":
        kwargs = {"height": 120 if len(str(default)) < 220 else 180, "key": key, "help": help_text}
        if not has_state:
            kwargs["value"] = default
        return st.text_area(label, **kwargs)
    kwargs = {"key": key, "help": help_text}
    if not has_state:
        kwargs["value"] = str(default)
    return st.text_input(label, **kwargs)


def _load_payload(slug: str, payload: dict[str, Any], label: str, why: str) -> None:
    item = CATALOG_BY_SLUG[slug]
    merged = default_payload(slug)
    merged.update(payload)
    for field in item["fields"]:
        st.session_state[f"demo:{slug}:{field['name']}"] = merged[field["name"]]
    st.session_state[f"demo-loaded:{slug}"] = {"label": label, "why": why}
    st.session_state.pop(f"demo-result:{slug}", None)
    st.session_state.pop(f"demo-error:{slug}", None)


def _render_guidance(slug: str) -> None:
    guide = GUIDANCE[slug]
    st.markdown("### How to use this demo")
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.markdown("**1 · What it does**")
            st.write(guide["what"])
    with c2:
        with st.container(border=True):
            st.markdown("**2 · Inputs**")
            st.write(guide["inputs"])
    with c3:
        with st.container(border=True):
            st.markdown("**3 · Output**")
            st.write(guide["output"])

    st.markdown("#### Sample scenarios")
    st.caption("Each sample exercises a different decision path. Load one, then run the system.")
    scenarios = SCENARIOS[slug]
    cols = st.columns(3)
    with cols[0]:
        if st.button("Reset", key=f"reset:{slug}", use_container_width=True):
            _load_payload(slug, {}, "Starter example", "Baseline values for this system.")
            st.rerun()
    for index, scenario in enumerate(scenarios, start=1):
        with cols[index]:
            if st.button(f"Load: {scenario['label']}", key=f"sample:{slug}:{index}", use_container_width=True):
                _load_payload(slug, scenario["payload"], scenario["label"], scenario["why"])
                st.rerun()

    loaded = st.session_state.get(f"demo-loaded:{slug}")
    if loaded:
        st.info(f"**Loaded:** {loaded['label']}  \n{loaded['why']}")


def _render_product(slug: str) -> None:
    item = CATALOG_BY_SLUG[slug]
    pillar = PILLAR_BY_SLUG[slug]
    top_left, top_right = st.columns([1, .25])
    with top_left:
        st.markdown(f'<div class="ash-eyebrow">{pillar} · {item["category"]}</div>', unsafe_allow_html=True)
        st.markdown(f"# {item['title']}")
        st.write(item["summary"])
    with top_right:
        if st.button("← All systems", use_container_width=True):
            _set_product(None)
            st.rerun()

    st.markdown('<span class="ash-pill">Python engine</span><span class="ash-pill">Synthetic inputs</span><span class="ash-pill">No API key required</span>', unsafe_allow_html=True)

    _render_guidance(slug)

    st.markdown("### Try it")
    payload: dict[str, Any] = {}
    with st.form(f"product-form-{slug}", border=True):
        for field in item["fields"]:
            if "json" in field["label"].lower():
                with st.expander("Advanced · Edit sample dataset (JSON)", expanded=False):
                    payload[field["name"]] = _render_field(slug, field)
            else:
                payload[field["name"]] = _render_field(slug, field)
        submitted = st.form_submit_button("Run system", type="primary", use_container_width=True)

    result_key = f"demo-result:{slug}"
    error_key = f"demo-error:{slug}"
    if submitted:
        errors = validate_payload(slug, payload)
        if errors:
            st.session_state[error_key] = "Please fix the input:\n\n" + "\n".join(f"- {error}" for error in errors)
            st.session_state.pop(result_key, None)
        else:
            try:
                st.session_state[result_key] = run_product(slug, payload)
                st.session_state.pop(error_key, None)
            except Exception as exc:
                st.session_state[error_key] = f"Input could not be processed. Load a sample scenario or check the formats above. Details: {exc}"
                st.session_state.pop(result_key, None)

    if error_key in st.session_state:
        st.error(st.session_state[error_key])
    if result_key in st.session_state:
        _result_panel(slug, st.session_state[result_key])
        st.info("**Result guide:** " + GUIDANCE[slug]["output"])

    st.divider()
    st.markdown("### Under the hood")
    st.write("The interface calls the Python engine under `projects/`; the UI does not duplicate the decision logic.")
    st.page_link(f"https://github.com/AshIntelligence/agenticmine/tree/main/projects/{slug}", label="View source + architecture ↗")


def _render_grounded_agent() -> None:
    st.markdown('<div class="ash-eyebrow">EVALUATE · GROUNDED Q&A</div>', unsafe_allow_html=True)
    st.markdown("# Grounded document Q&A")
    st.write("Ask a question across two policy documents. The agent retrieves relevant passages first, answers from those passages, cites them and shows the evaluation trace.")
    st.info("Enter a question about availability, rollout, controls or another fact in the documents. A starter question is pre-filled.")

    question = st.text_input("Question", value="What availability targets do the documents specify, and where do they conflict?", key="grounded-agent-question")
    if st.button("Run grounded Q&A", type="primary", use_container_width=True):
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
    st.caption("CONTROL · EVALUATE · DECIDE")
    if st.button("⌂ Systems Lab", use_container_width=True):
        _set_product(None)
        st.rerun()
    if st.button("✦ Grounded Q&A", use_container_width=True):
        st.session_state["selected_product"] = "__agent__"
        if "product" in st.query_params:
            del st.query_params["product"]
        st.rerun()
    st.divider()
    title_by_slug = {item["slug"]: item["title"] for item in CATALOG}
    options = ["— Select a system —"] + [title_by_slug[item["slug"]] for item in CATALOG]
    choice = st.selectbox("Jump to a system", options, index=0, key="product-jump")
    if choice != options[0]:
        target = next(slug for slug, title in title_by_slug.items() if title == choice)
        if target != selected:
            _set_product(target)
            st.rerun()
    st.divider()
    st.page_link("https://github.com/AshIntelligence/agenticmine", label="GitHub source ↗")

if selected == "__agent__":
    _render_grounded_agent()
elif selected in CATALOG_BY_SLUG:
    _render_product(selected)
else:
    check = verify_catalog()
    st.markdown('<div class="ash-eyebrow">ASH INTELLIGENCE · SYSTEMS LAB</div>', unsafe_allow_html=True)
    st.markdown('<div class="ash-hero">AI product decisions,<br>made concrete.</div>', unsafe_allow_html=True)
    st.markdown('<div class="ash-sub">20 runnable prototypes across agent control, evaluation, risk, fintech, reliability and product discovery. Each exposes the inputs, state, rules and output behind the decision.</div>', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Runnable systems", check["count"])
    m2.metric("Areas", "3")
    m3.metric("Guided scenarios", "40")
    m4.metric("Grounded Q&A", "Included")

    if check["missing"] or not check["unique"]:
        st.error(f"Catalog integrity issue: {check}")

    st.markdown("## Start with the flagships")
    pillar_cols = st.columns(3)
    for index, pillar in enumerate(("CONTROL", "EVALUATE", "DECIDE")):
        copy = PILLAR_COPY[pillar]
        flagship = CATALOG_BY_SLUG[copy["flagship"]]
        with pillar_cols[index]:
            with st.container(border=True):
                st.caption(pillar)
                st.markdown(f"### {copy['question']}")
                st.write(copy["detail"])
                st.markdown(f"**{flagship['title']}**")
                st.caption(flagship["summary"])
                if st.button("Open →", key=f"flagship:{pillar}", use_container_width=True):
                    _open_product(flagship["slug"])

    st.divider()
    st.markdown("## Explore the full lab")
    st.write("The rest of the systems extend the same three areas: control, evaluation and decisioning.")

    search = st.text_input("Find a system", placeholder="Try: risk, RAG, finance, agent, experiment…")
    pillar_filter = st.segmented_control("Area", ["All", "CONTROL", "EVALUATE", "DECIDE"], default="All")

    filtered = []
    for item in CATALOG:
        pillar = PILLAR_BY_SLUG[item["slug"]]
        haystack = f"{item['title']} {item['summary']} {item['category']} {pillar}".lower()
        if search and search.lower() not in haystack:
            continue
        if pillar_filter and pillar_filter != "All" and pillar != pillar_filter:
            continue
        filtered.append(item)

    with st.expander(f"Browse all {len(filtered)} matching systems", expanded=False):
        cols = st.columns(3)
        for index, item in enumerate(filtered):
            pillar = PILLAR_BY_SLUG[item["slug"]]
            with cols[index % 3]:
                with st.container(border=True):
                    st.caption(f"{pillar} · {item['category'].upper()}")
                    st.markdown(f"### {item['title']}")
                    st.write(item["summary"])
                    if st.button("Open system →", key=f"open:{item['slug']}", use_container_width=True):
                        _open_product(item["slug"])

    st.divider()
    with st.container(border=True):
        c1, c2 = st.columns([1.2, .8])
        with c1:
            st.markdown("## Grounded document Q&A")
            st.write("Retrieve evidence, answer from the retrieved passages, cite the source chunks and review the evaluation trace.")
        with c2:
            if st.button("Open grounded Q&A →", type="primary", use_container_width=True):
                st.session_state["selected_product"] = "__agent__"
                st.rerun()

    st.caption("All demos use synthetic or public-safe inputs. Each card calls the Python engine under `projects/`; the UI does not duplicate the decision logic.")
