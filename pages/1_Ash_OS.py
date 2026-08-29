from __future__ import annotations

import html

import streamlit as st

from core.personal_control_plane import SCENARIOS, run_control_plane


st.set_page_config(page_title="Ash OS · Personal Control Plane", page_icon="✦", layout="wide")

st.markdown(
    """
<style>
.block-container {max-width: 1250px; padding-top: 3.1rem; padding-bottom: 4rem;}
[data-testid="stSidebar"] {border-right: 1px solid rgba(120,120,150,.16);}
.ash-kicker {font-size:.78rem; letter-spacing:.16em; font-weight:850; opacity:.68; text-transform:uppercase; margin-bottom:.7rem;}
.ash-title {font-size:clamp(3rem,7vw,6.3rem); line-height:.88; letter-spacing:-.06em; font-weight:900; margin:0 0 1.05rem;}
.ash-dek {font-size:1.05rem; line-height:1.6; max-width:880px; opacity:.78; margin-bottom:1.35rem;}
.loop {display:flex; gap:.48rem; flex-wrap:wrap; margin:.8rem 0 1.5rem;}
.loop span {border:1px solid rgba(130,130,160,.24); border-radius:999px; padding:.38rem .7rem; font-size:.78rem; font-weight:750; opacity:.84;}
.route {border:1px solid rgba(130,130,160,.20); border-radius:18px; padding:1rem 1.05rem; margin-bottom:.72rem; background:rgba(130,130,160,.045);}
.route h4 {font-size:1rem; margin:.1rem 0 .35rem;}
.route .meta {font-size:.76rem; opacity:.64; text-transform:uppercase; letter-spacing:.08em;}
.route .why {font-size:.86rem; opacity:.78; margin-top:.55rem; line-height:1.45;}
.route .ctx {font-size:.80rem; opacity:.66; margin-top:.5rem; line-height:1.42;}
.handle {box-shadow:inset 3px 0 0 #34d399}.draft {box-shadow:inset 3px 0 0 #60a5fa}.ask {box-shadow:inset 3px 0 0 #fb7185}.watch {box-shadow:inset 3px 0 0 #a78bfa}
.arch {display:grid;grid-template-columns:repeat(5,1fr);gap:.55rem;margin:1rem 0 1.4rem}.arch div{border:1px solid rgba(130,130,160,.22);border-radius:14px;padding:.8rem;text-align:center;font-size:.78rem;font-weight:800}.arch b{display:block;font-size:.68rem;opacity:.55;margin-bottom:.28rem;letter-spacing:.09em}
.note {font-size:.82rem; opacity:.72; line-height:1.5;}
@media(max-width:800px){.arch{grid-template-columns:1fr 1fr}.ash-title{font-size:3.4rem}}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="ash-kicker">Ash Intelligence · Forward-Deployed Product</div>', unsafe_allow_html=True)
st.markdown('<div class="ash-title">Ash OS<br>Personal Control Plane</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="ash-dek">A personal assistant should not just answer questions. It should notice what changed, understand what matters in context, handle safe work, stage the rest, and interrupt you only when your judgment is actually needed.</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="loop"><span>INBOX</span><span>CALENDAR</span><span>MONEY</span><span>CAREER</span><span>TRAVEL</span><span>PEOPLE</span><span>MEMORY</span><span>APPROVAL</span><span>AUDIT</span></div>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### Control policy")
    scenario_name = st.selectbox("Scenario", list(SCENARIOS), index=0)
    autonomy = st.slider(
        "Autonomy confidence threshold",
        min_value=.55,
        max_value=.95,
        value=.78,
        step=.01,
        help="Below this confidence, the system may prepare work but cannot treat it as ready for autonomous handling.",
    )
    money_gate = st.slider(
        "Money approval threshold",
        min_value=0,
        max_value=500,
        value=100,
        step=25,
        help="Actions at or above this amount always route to Ash for approval in the demo policy.",
    )
    st.caption("All examples are synthetic. No real inbox, account, calendar or credential data is used by this public demo.")

result = run_control_plane(
    SCENARIOS[scenario_name],
    autonomy_threshold=autonomy,
    money_approval_threshold=float(money_gate),
)
summary = result["summary"]

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Signals", summary["signals"])
m2.metric("Handled", summary["handled"])
m3.metric("Drafted", summary["drafted"])
m4.metric("Needs Ash", summary["needs_ash"])
m5.metric("Watching", summary["watching"])

st.markdown("### What changed → what happens next")
st.caption("The system ranks the queue, but policy—not model confidence alone—sets the action boundary.")

routes = {
    "HANDLE": ("Handled", "handle"),
    "DRAFT": ("Prepared for approval", "draft"),
    "ASK ASH": ("Needs Ash", "ask"),
    "WATCH": ("Watch quietly", "watch"),
}

cols = st.columns(4)
for col, (route, (heading, css_class)) in zip(cols, routes.items()):
    with col:
        st.markdown(f"#### {heading}")
        items = [d for d in result["decisions"] if d["route"] == route]
        if not items:
            st.caption("Nothing here in this scenario.")
        for item in items:
            title = html.escape(item["title"])
            detail = html.escape(item["detail"])
            action = html.escape(item["proposed_action"])
            reason = html.escape(item["reason"])
            context = html.escape(item["memory_context"] or "No extra memory context applied.")
            st.markdown(
                f"""
<div class="route {css_class}">
  <div class="meta">{html.escape(item['source'])} · {html.escape(item['domain'])} · priority {item['priority']:.0%}</div>
  <h4>{title}</h4>
  <div>{detail}</div>
  <div class="why"><b>Next:</b> {action}<br><b>Why:</b> {reason}</div>
  <div class="ctx"><b>Context used:</b> {context}</div>
</div>
""",
                unsafe_allow_html=True,
            )

st.markdown("### Decision trace")
for item in result["decisions"]:
    with st.expander(f"{item['route']} · {item['title']}"):
        c1, c2, c3 = st.columns(3)
        c1.metric("Confidence", f"{item['confidence']:.0%}")
        c2.metric("Urgency", f"{item['urgency']:.0%}")
        c3.metric("Due", f"{item['due_hours']:g}h")
        st.write("**Proposed action:**", item["proposed_action"])
        st.write("**Policy reason:**", item["reason"])
        st.write("**Memory/context:**", item["memory_context"] or "—")
        st.write("**Human approval:**", "Required" if item["approval_required"] else "Not required")

st.markdown("### System shape")
st.markdown(
    """
<div class="arch">
  <div><b>1 · SIGNALS</b>Email · calendar · money · travel · career</div>
  <div><b>2 · CONTEXT</b>Preferences · history · dependencies · current state</div>
  <div><b>3 · POLICY</b>Confidence · sensitivity · reversibility · spend</div>
  <div><b>4 · ACTION</b>Handle · draft · ask · watch</div>
  <div><b>5 · AUDIT</b>Reason · approval · result · follow-up</div>
</div>
""",
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="note"><b>Product principle:</b> the assistant should optimize for fewer things you have to remember—not for the highest possible number of autonomous actions. The useful boundary is contextual autonomy with visible approval and audit.</div>',
    unsafe_allow_html=True,
)

st.divider()
c1, c2 = st.columns([1, 1])
with c1:
    st.markdown("**What this demo proves**")
    st.write("Cross-domain prioritization, memory-aware routing, explicit autonomy policy, approval gates and traceable decisions.")
with c2:
    st.markdown("**What a production version adds**")
    st.write("Real connectors, event triggers, tool execution, durable state, user-specific policies, secure credential handling, notification controls and outcome learning.")
