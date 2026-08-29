from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable


@dataclass(frozen=True)
class Signal:
    source: str
    domain: str
    title: str
    detail: str
    proposed_action: str
    confidence: float = 0.9
    urgency: float = 0.5
    reversibility: float = 0.8
    sensitivity: float = 0.2
    due_hours: float = 24.0
    requires_external_commit: bool = False
    amount_usd: float = 0.0
    memory_context: str = ""


@dataclass(frozen=True)
class Decision:
    source: str
    domain: str
    title: str
    detail: str
    proposed_action: str
    route: str
    priority: float
    reason: str
    approval_required: bool
    confidence: float
    urgency: float
    due_hours: float
    memory_context: str


ROUTE_ORDER = {"ASK ASH": 0, "DRAFT": 1, "HANDLE": 2, "WATCH": 3}


def _priority(signal: Signal) -> float:
    due_pressure = 1.0 if signal.due_hours <= 2 else 0.82 if signal.due_hours <= 8 else 0.62 if signal.due_hours <= 24 else 0.35
    financial_weight = min(signal.amount_usd / 500.0, 1.0) * 0.10
    score = (signal.urgency * 0.52) + (due_pressure * 0.28) + (signal.sensitivity * 0.10) + financial_weight
    return round(min(score, 1.0), 2)


def decide_signal(signal: Signal, *, autonomy_threshold: float = 0.78, money_approval_threshold: float = 100.0) -> Decision:
    """Route one signal without equating model confidence with execution authority."""
    high_money = signal.amount_usd >= money_approval_threshold and signal.amount_usd > 0
    low_reversibility = signal.reversibility < 0.45
    high_sensitivity = signal.sensitivity >= 0.72
    low_confidence = signal.confidence < autonomy_threshold
    high_consequence_commit = signal.requires_external_commit and (
        signal.sensitivity >= 0.45 or low_reversibility or high_money
    )

    if high_sensitivity or high_money or low_reversibility or high_consequence_commit:
        reasons = []
        if high_sensitivity:
            reasons.append("sensitive action")
        if high_money:
            reasons.append(f"${signal.amount_usd:,.0f} financial impact")
        if low_reversibility:
            reasons.append("hard to reverse")
        if high_consequence_commit:
            reasons.append("external commitment")
        route = "ASK ASH"
        reason = "Human approval required: " + ", ".join(dict.fromkeys(reasons)) + "."
        approval_required = True
    elif low_confidence:
        route = "DRAFT"
        reason = f"Confidence {signal.confidence:.0%} is below the {autonomy_threshold:.0%} autonomy threshold. Prepare the work; do not commit it."
        approval_required = True
    elif signal.urgency < 0.28 and signal.due_hours > 48:
        route = "WATCH"
        reason = "No action is needed yet. Keep state alive and re-check only when timing or context changes."
        approval_required = False
    elif signal.requires_external_commit:
        route = "DRAFT"
        reason = "The work is safe to prepare, but it changes an external system. Stage it for approval."
        approval_required = True
    else:
        route = "HANDLE"
        reason = "High confidence, reversible, low-sensitivity work inside the allowed autonomy boundary."
        approval_required = False

    return Decision(
        source=signal.source,
        domain=signal.domain,
        title=signal.title,
        detail=signal.detail,
        proposed_action=signal.proposed_action,
        route=route,
        priority=_priority(signal),
        reason=reason,
        approval_required=approval_required,
        confidence=signal.confidence,
        urgency=signal.urgency,
        due_hours=signal.due_hours,
        memory_context=signal.memory_context,
    )


def run_control_plane(signals: Iterable[Signal], *, autonomy_threshold: float = 0.78, money_approval_threshold: float = 100.0) -> dict[str, Any]:
    decisions = [
        decide_signal(signal, autonomy_threshold=autonomy_threshold, money_approval_threshold=money_approval_threshold)
        for signal in signals
    ]
    decisions.sort(key=lambda d: (ROUTE_ORDER[d.route], -d.priority, d.due_hours))
    counts = {route: sum(1 for decision in decisions if decision.route == route) for route in ROUTE_ORDER}
    return {
        "summary": {
            "signals": len(decisions),
            "handled": counts["HANDLE"],
            "drafted": counts["DRAFT"],
            "needs_ash": counts["ASK ASH"],
            "watching": counts["WATCH"],
        },
        "decisions": [asdict(decision) for decision in decisions],
        "policy": {
            "autonomy_threshold": autonomy_threshold,
            "money_approval_threshold": money_approval_threshold,
            "principle": "Confidence can recommend an action; policy decides whether the system may execute it.",
        },
    }


SCENARIOS: dict[str, list[Signal]] = {
    "Normal Tuesday": [
        Signal("Gmail", "Inbox", "Recruiter asks for interview windows", "A recruiter needs three 45-minute windows next week.", "Cross-check the calendar and draft three open windows.", .97, .65, .95, .18, 10, memory_context="Prefer Pacific-time-friendly windows and avoid back-to-back interviews."),
        Signal("Calendar", "Schedule", "Dinner overlaps a Seahawks home game", "Traffic makes the current reservation risky.", "Flag the conflict and suggest two nearby alternatives.", .93, .48, .95, .08, 36, memory_context="Seattle event traffic matters more than the nominal calendar overlap."),
        Signal("Email", "Money", "$228 store credit found", "An old credit is still valid.", "Prepare redemption steps and stage the credit for approval.", .91, .35, .65, .55, 96, True, 228, "Do not spend or transfer money without approval."),
        Signal("Tasks", "Admin", "Parking packet is complete", "All required documents are present.", "Create a clean submission checklist.", .96, .62, .96, .22, 18, memory_context="Keep source evidence attached to every administrative claim."),
        Signal("Travel", "Travel", "Hawaii fare is unchanged", "No meaningful price or schedule change.", "Keep watching; no notification needed.", .95, .15, 1.0, .05, 120, memory_context="Interrupt only when fare, availability or itinerary quality changes materially."),
    ],
    "Interview Day": [
        Signal("Gmail", "Career", "Panel details arrived", "New interviewers and focus areas landed three hours before the call.", "Update the brief and map one story to each focus area.", .98, .96, .98, .15, 2, memory_context="Use concise executive-principal answers with technical depth."),
        Signal("Calendar", "Schedule", "Prep block is squeezed", "Only 20 minutes remain between commitments.", "Draft a reschedule note for the lower-priority meeting.", .86, .88, .80, .25, 1.5, True, memory_context="Protect interview preparation time when there is a real conflict."),
        Signal("Notes", "Career", "Compensation notes conflict", "Two recruiter notes use different equity assumptions.", "Surface the discrepancy and ask which number is canonical.", .69, .72, .95, .35, 3, memory_context="Never invent compensation details when notes disagree."),
        Signal("Tasks", "Career", "Thank-you is due", "The interview ended 40 minutes ago.", "Draft a short thank-you referencing the actual discussion.", .94, .58, .90, .12, 8, True, memory_context="Keep follow-ups specific, warm and brief."),
    ],
    "Travel Disruption": [
        Signal("Airline", "Travel", "Flight moved by 2h 15m", "Arrival now conflicts with the rental-car pickup.", "Rebuild the arrival plan and draft the rental-car change.", .96, .92, .82, .18, 3, True, memory_context="Prefer lower walking burden and simple hotel check-in."),
        Signal("Calendar", "Schedule", "Airport departure overlaps a work call", "The call falls inside the new boarding window.", "Draft a reschedule request with two alternatives.", .94, .90, .90, .18, 2, True, memory_context="Do not create a new meeting until the other party confirms."),
        Signal("Hotel", "Travel", "Upgrade offer expires tonight", "The upgrade is $180 and non-refundable.", "Show the tradeoff and ask before purchasing.", .99, .68, .15, .50, 6, True, 180, "Paid, non-refundable travel changes require approval."),
        Signal("Weather", "Travel", "Rain probability rose to 35%", "No material itinerary impact yet.", "Watch for a stronger change before interrupting.", .92, .18, 1.0, .02, 72, memory_context="Avoid low-value travel alerts."),
    ],
    "High-Stakes Money": [
        Signal("Bank Alert", "Money", "Large unfamiliar charge posted", "$1,840 charge does not match recent purchase context.", "Gather evidence and ask Ash to review before any dispute or account action.", .87, .98, .35, .92, 1, False, 1840, "Financial disputes and account restrictions require approval."),
        Signal("Email", "Money", "Subscription renewal notice", "A $29 monthly tool renews in five days.", "Compare recent usage and prepare a keep/cancel recommendation.", .94, .45, .85, .26, 60, False, 29, "Small recurring charges can be analyzed automatically; cancellation is staged."),
        Signal("Finance", "Money", "Card payment is scheduled", "The existing payment matches the statement plan.", "Watch for posting; do not create a duplicate payment.", .97, .24, .75, .68, 72, memory_context="Never duplicate an already-scheduled payment."),
        Signal("Identity", "Security", "Password-reset request detected", "A reset was initiated from a new device.", "Do not act autonomously; surface the security context.", .99, .95, .25, .98, .5, True, memory_context="Identity, login and credential changes always require direct user control."),
    ],
}
