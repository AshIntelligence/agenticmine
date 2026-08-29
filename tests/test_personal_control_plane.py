from core.personal_control_plane import SCENARIOS, Signal, decide_signal, run_control_plane


def test_sensitive_action_requires_ash():
    signal = Signal(
        source="Identity",
        domain="Security",
        title="Reset password",
        detail="New device",
        proposed_action="Reset",
        confidence=.99,
        urgency=.9,
        reversibility=.2,
        sensitivity=.95,
        requires_external_commit=True,
    )
    assert decide_signal(signal).route == "ASK ASH"


def test_low_confidence_is_draft_not_autonomous():
    signal = Signal(
        source="Email",
        domain="Inbox",
        title="Ambiguous reply",
        detail="Context conflicts",
        proposed_action="Prepare reply",
        confidence=.62,
        urgency=.6,
        reversibility=.9,
        sensitivity=.2,
    )
    assert decide_signal(signal, autonomy_threshold=.78).route == "DRAFT"


def test_quiet_watch_path_exists():
    result = run_control_plane(SCENARIOS["Normal Tuesday"])
    assert any(decision["route"] == "WATCH" for decision in result["decisions"])


def test_money_above_gate_requires_ash():
    result = run_control_plane(SCENARIOS["Normal Tuesday"], money_approval_threshold=100)
    credit = next(decision for decision in result["decisions"] if "store credit" in decision["title"])
    assert credit["route"] == "ASK ASH"
