from __future__ import annotations

import html
from dataclasses import dataclass

import streamlit as st


@dataclass(frozen=True)
class Signal:
    source: str
    domain: str
    title: str
    detail: str
    action: str
    confidence: float
    urgency: float
    reversibility: float
    sensitivity: float
    due_hours: float
    external: bool = False
    amount: float = 0.0
    context: str = ""


def priority(s: Signal) -> float:
    due = 1.0 if s.due_hours <= 2 else .82 if s.due_hours <= 8 else .62 if s.due_hours <= 24 else .35
    return min(1.0, round(s.urgency * .52 + due * .28 + s.sensitivity * .10 + min(s.amount / 500, 1) * .10, 2))


def route(s: Signal, autonomy: float, money_gate: float) -> tuple[str, str, bool]:
    reasons = []
    if s.sensitivity >= .72:
        reasons.append("sensitive action")
    if s.amount >= money_gate and s.amount > 0:
        reasons.append(f"${s.amount:,.0f} financial impact")
    if s.reversibility < .45:
        reasons.append("hard to reverse")
    if s.external and (s.sensitivity >= .45 or s.reversibility < .45 or s.amount >= money_gate):
        reasons.append("external commitment")
    if reasons:
        return "ASK ASH", "Human approval required: " + ", ".join(dict.fromkeys(reasons)) + ".", True
    if s.confidence < autonomy:
        return "DRAFT", f"Confidence {s.confidence:.0%} is below the {autonomy:.0%} autonomy threshold. Prepare the work; do not commit it.", True
    if s.urgency < .28 and s.due_hours > 48:
        return "WATCH", "No action is needed yet. Keep state alive and re-check only when timing or context changes.", False
    if s.external:
        return "DRAFT", "The work is safe to prepare, but it changes an external system. Stage it for approval.", True
    return "HANDLE", "High confidence, reversible, low-sensitivity work inside the allowed autonomy boundary.", False


SCENARIOS = {
    "Normal Tuesday": [
        Signal("Gmail", "Inbox", "Recruiter asks for interview windows", "A recruiter needs three 45-minute windows next week.", "Cross-check the calendar and draft three open windows.", .97, .65, .95, .18, 10, context="Prefer Pacific-time-friendly windows and avoid back-to-back interviews."),
        Signal("Calendar", "Schedule", "Dinner overlaps a Seahawks home game", "Traffic makes the current reservation risky.", "Flag the conflict and suggest two nearby alternatives.", .93, .48, .95, .08, 36, context="Seattle event traffic matters more than the nominal calendar overlap."),
        Signal("Email", "Money", "$228 store credit found", "An old credit is still valid.", "Prepare redemption steps and stage the credit for approval.", .91, .35, .65, .55, 96, True, 228, "Do not spend or transfer money without approval."),
        Signal("Tasks", "Admin", "Parking packet is complete", "All required documents are present.", "Create a clean submission checklist.", .96, .62, .96, .22, 18, context="Keep source evidence attached to every administrative claim."),
        Signal("Travel", "Travel", "Hawaii fare is unchanged", "No meaningful price or schedule change.", "Keep watching; no notification needed.", .95, .15, 1.0, .05, 120, context="Interrupt only when fare, availability or itinerary quality changes materially."),
    ],
    "Interview Day": [
        Signal("Gmail", "Career", "Panel details arrived", "New interviewers and focus areas landed three hours before the call.", "Update the brief and map one story to each focus area.", .98, .96, .98, .15, 2, context="Use concise executive-principal answers with technical depth."),
        Signal("Calendar", "Schedule", "Prep block is squeezed", "Only 20 minutes remain between commitments.", "Draft a reschedule note for the lower-priority meeting.", .86, .88, .80, .25, 1.5, True, context="Protect interview preparation time when there is a real conflict."),
        Signal("Notes", "Career", "Compensation notes conflict", "Two recruiter notes use different equity assumptions.", "Surface the discrepancy and ask which number is canonical.", .69, .72, .95, .35, 3, context="Never invent compensation details when notes disagree."),
        Signal("Tasks", "Career", "Thank-you is due", "The interview ended 40 minutes ago.", "Draft a short thank-you referencing the actual discussion.", .94, .58, .90, .12, 8, True, context="Keep follow-ups specific, warm and brief."),
    ],
    "Travel Disruption": [
        Signal("Airline", "Travel", "Flight moved by 2h 15m", "Arrival now conflicts with the rental-car pickup.", "Rebuild the arrival plan and draft the rental-car change.", .96, .92, .82, .18, 3, True, context="Prefer lower walking burden and simple hotel check-in."),
        Signal("Calendar", "Schedule", "Airport departure overlaps a work call", "The call falls inside the new boarding window.", "Draft a reschedule request with two alternatives.", .94, .90, .90, .18, 2, True, context="Do not create a new meeting until the other party confirms."),
        Signal("Hotel", "Travel", "Upgrade offer expires tonight", "The upgrade is $180 and non-refundable.", "Show the tradeoff and ask before purchasing.", .99, .68, .15, .50, 6, True, 180, "Paid, non-refundable travel changes require approval."),
        Signal("Weather", "Travel", "Rain probability rose to 35%", "No material itinerary impact yet.", "Watch for a stronger change before interrupting.", .92, .18, 1.0, .02, 72, context="Avoid low-value travel alerts."),
    ],
    "High-Stakes Money": [
        Signal("Bank Alert", "Money", "Large unfamiliar charge posted", "$1,840 charge does not match recent purchase context.", "Gather evidence and ask Ash to review before any dispute or account action.", .87, .98, .35, .92, 1, False, 1840, "Financial disputes and account restrictions require approval."),
        Signal("Email", "Money", "Subscription renewal notice", "A $29 monthly tool renews in five days.", "Compare recent usage and prepare a keep/cancel recommendation.", .94, .45, .85, .26, 60, False, 29, "Small recurring charges can be analyzed automatically; cancellation is staged."),
        Signal("Finance", "Money", "Card payment is scheduled", "The existing payment matches the statement plan.", "Watch for posting; do not create a duplicate payment.", .97, .24, .75, .68, 72, context="Never duplicate an already-scheduled payment."),
        Signal("Identity", "Security", "Password-reset request detected", "A reset was initiated from a new device.", "Do not act autonomously; surface the security context.", .99, .95, .25, .98, .5, True, context="Identity, login and credential changes always require direct user control."),
    ],
}

st.set_page_config(page_title="Ash OS · Personal Control Plane", page_icon="✦", layout="wide")
st.markdown("""
<style>
.block-container{max-width:1250px;padding-top:3rem;padding-bottom:4rem}.k{font-size:.78rem;letter-spacing:.16em;font-weight:850;opacity:.68;text-transform:uppercase}.t{font-size:clamp(3rem,7vw,6.3rem);line-height:.88;letter-spacing:-.06em;font-weight:900;margin:.7rem 0 1rem}.d{font-size:1.05rem;line-height:1.6;max-width:900px;opacity:.78}.loop{display:flex;gap:.45rem;flex-wrap:wrap;margin:1rem 0 1.6rem}.loop span{border:1px solid rgba(130,130,160,.24);border-radius:999px;padding:.38rem .7rem;font-size:.77rem;font-weight:750}.r{border:1px solid rgba(130,130,160,.2);border-radius:18px;padding:1rem;margin-bottom:.72rem;background:rgba(130,130,160,.045)}.r h4{font-size:1rem;margin:.15rem 0 .35rem}.m{font-size:.72rem;opacity:.62;text-transform:uppercase;letter-spacing:.07em}.w{font-size:.84rem;opacity:.78;margin-top:.55rem;line-height:1.45}.c{font-size:.79rem;opacity:.64;margin-top:.48rem;line-height:1.4}.handle{box-shadow:inset 3px 0 0 #34d399}.draft{box-shadow:inset 3px 0 0 #60a5fa}.ask{box-shadow:inset 3px 0 0 #fb7185}.watch{box-shadow:inset 3px 0 0 #a78bfa}.arch{display:grid;grid-template-columns:repeat(5,1fr);gap:.55rem;margin:1rem 0}.arch div{border:1px solid rgba(130,130,160,.22);border-radius:14px;padding:.8rem;text-align:center;font-size:.78rem;font-weight:800}.arch b{display:block;font-size:.67rem;opacity:.55;margin-bottom:.28rem;letter-spacing:.08em}@media(max-width:800px){.arch{grid-template-columns:1fr 1fr}.t{font-size:3.35rem}}
</style>""", unsafe_allow_html=True)

st.markdown('<div class="k">Ash Intelligence · Forward-Deployed Product</div>', unsafe_allow_html=True)
st.markdown('<div class="t">Ash OS<br>Personal Control Plane</div>', unsafe_allow_html=True)
st.markdown('<div class="d">A personal assistant should not just answer questions. It should notice what changed, understand what matters in context, handle safe work, stage the rest, and interrupt you only when your judgment is actually needed.</div>', unsafe_allow_html=True)
st.markdown('<div class="loop"><span>INBOX</span><span>CALENDAR</span><span>MONEY</span><span>CAREER</span><span>TRAVEL</span><span>PEOPLE</span><span>MEMORY</span><span>APPROVAL</span><span>AUDIT</span></div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Control policy")
    scenario = st.selectbox("Scenario", list(SCENARIOS))
    autonomy = st.slider("Autonomy confidence threshold", .55, .95, .78, .01)
    money_gate = st.slider("Money approval threshold", 0, 500, 100, 25)
    st.caption("Synthetic demo only. No real inbox, account, calendar or credential data is used.")

rows = []
for s in SCENARIOS[scenario]:
    status, why, approval = route(s, autonomy, float(money_gate))
    rows.append((status, priority(s), s, why, approval))
order = {"ASK ASH":0,"DRAFT":1,"HANDLE":2,"WATCH":3}
rows.sort(key=lambda x:(order[x[0]],-x[1],x[2].due_hours))
counts = {k:sum(1 for r in rows if r[0]==k) for k in order}

metrics = st.columns(5)
for c, label, value in zip(metrics,["Signals","Handled","Drafted","Needs Ash","Watching"],[len(rows),counts["HANDLE"],counts["DRAFT"],counts["ASK ASH"],counts["WATCH"]]):
    c.metric(label,value)

st.markdown("### What changed → what happens next")
st.caption("The model can recommend. Policy decides whether the system is allowed to act.")
columns = st.columns(4)
for col, status, heading, css in zip(columns,["HANDLE","DRAFT","ASK ASH","WATCH"],["Handled","Prepared","Needs Ash","Watch quietly"],["handle","draft","ask","watch"]):
    with col:
        st.markdown(f"#### {heading}")
        selected = [r for r in rows if r[0]==status]
        if not selected:
            st.caption("Nothing here in this scenario.")
        for _, p, s, why, approval in selected:
            st.markdown(f'''<div class="r {css}"><div class="m">{html.escape(s.source)} · {html.escape(s.domain)} · priority {p:.0%}</div><h4>{html.escape(s.title)}</h4><div>{html.escape(s.detail)}</div><div class="w"><b>Next:</b> {html.escape(s.action)}<br><b>Why:</b> {html.escape(why)}</div><div class="c"><b>Context used:</b> {html.escape(s.context or "No extra context")}</div></div>''', unsafe_allow_html=True)

st.markdown("### Decision trace")
for status,p,s,why,approval in rows:
    with st.expander(f"{status} · {s.title}"):
        a,b,c = st.columns(3)
        a.metric("Confidence",f"{s.confidence:.0%}")
        b.metric("Urgency",f"{s.urgency:.0%}")
        c.metric("Due",f"{s.due_hours:g}h")
        st.write("**Proposed action:**",s.action)
        st.write("**Policy reason:**",why)
        st.write("**Memory/context:**",s.context or "—")
        st.write("**Human approval:**","Required" if approval else "Not required")

st.markdown("### System shape")
st.markdown('''<div class="arch"><div><b>1 · SIGNALS</b>Email · calendar · money · travel · career</div><div><b>2 · CONTEXT</b>Preferences · history · dependencies · state</div><div><b>3 · POLICY</b>Confidence · sensitivity · reversibility · spend</div><div><b>4 · ACTION</b>Handle · draft · ask · watch</div><div><b>5 · AUDIT</b>Reason · approval · result · follow-up</div></div>''', unsafe_allow_html=True)
st.write("**Product principle:** optimize for fewer things the user has to remember—not for the maximum number of autonomous actions. The useful boundary is contextual autonomy with visible approval and audit.")
st.divider()
a,b = st.columns(2)
a.markdown("**What this demo proves**")
a.write("Cross-domain prioritization, memory-aware routing, explicit autonomy policy, approval gates and traceable decisions.")
b.markdown("**What production adds**")
b.write("Real connectors, event triggers, tool execution, durable state, secure credential handling, notification controls and outcome learning.")
