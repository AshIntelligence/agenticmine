from __future__ import annotations

import json
from typing import Any


GUIDANCE: dict[str, dict[str, str]] = {
    "agent-vs-workflow-router": {
        "what": "Routes a task to a deterministic workflow, assisted agent or autonomous agent.",
        "inputs": "Set task variability, consequence, statefulness, ambiguity and the number of available tools.",
        "output": "A routing decision and the factors that drove it.",
    },
    "agentic-product-control-plane": {
        "what": "Applies tool-permission and rollout gates around an agent.",
        "inputs": "Choose registered tools, approval requirements, the requested tool call, and current quality, incident and cost signals.",
        "output": "ALLOW / REVIEW / DENY for the tool call and HOLD / CANARY / PRODUCTION for rollout, plus the audit trail.",
    },
    "billing-reconciliation-observatory": {
        "what": "Checks whether usage, rated price and invoice amount reconcile.",
        "inputs": "Enter usage quantity, unit price, invoice amount and tolerance. Expected amount = quantity × unit price.",
        "output": "Expected amount, invoiced amount, delta and reconciliation status.",
    },
    "experiment-analysis-copilot": {
        "what": "Analyzes a two-arm conversion experiment and returns SHIP, HOLD or STOP.",
        "inputs": "Enter conversions and users for control and treatment, plus the significance threshold.",
        "output": "Control and treatment rates, uplift, statistical evidence and recommendation.",
    },
    "finance-close-orchestrator": {
        "what": "Advances finance-close work through dependencies, exceptions and controller approval.",
        "inputs": "Mark completed tasks and add a reconciliation exception when you want to block the downstream flow.",
        "output": "The next executable or blocked steps, with the reason for each state.",
    },
    "fraud-signal-decision-engine": {
        "what": "Combines risk signals into an explainable ALLOW, REVIEW or BLOCK decision.",
        "inputs": "Set risk signals from 0 to 1. Keep the review threshold below the block threshold.",
        "output": "Risk score, action, top reason codes and weighted signal contributions.",
    },
    "human-in-loop-risk-router": {
        "what": "Routes an AI action to ALLOW, REVIEW or DENY.",
        "inputs": "Set consequence, model confidence, reversibility and whether the action is sensitive.",
        "output": "The routing decision and the factors behind the review boundary.",
    },
    "incident-triage-agent": {
        "what": "Maps incident symptoms and impact to severity, owner and next action.",
        "inputs": "Describe the incident, set error rate and affected traffic, and mark whether the path is revenue-critical.",
        "output": "Severity, likely owner, triage score, matched signals and next action.",
    },
    "instagram-intentional-discovery": {
        "what": "Re-ranks a synthetic feed using relevance, novelty, creator diversity, quality and available time.",
        "inputs": "Choose interests and time budget, then provide feed items as JSON.",
        "output": "A ranked feed constrained by the scoring rules and session budget.",
    },
    "linkedin-career-discovery": {
        "what": "Ranks synthetic opportunities using skill fit, growth direction, freshness and location.",
        "inputs": "Enter current skills, growth areas, preferred locations and a JSON list of opportunities.",
        "output": "A ranked opportunity list with component fit scores.",
    },
    "mautam-evaluation": {
        "what": "Measures AI product health across six lenses, not just model quality.",
        "inputs": "Score model quality, adoption, workflow success, trust, availability and business impact from 0 to 1.",
        "output": "MAUTAM score, SHIP / TUNE / SIMPLIFY / STOP, weakest lens, gate failures and contribution chart.",
    },
    "payment-provider-onboarding": {
        "what": "Checks payment-provider readiness for a market launch.",
        "inputs": "Set capabilities, supported markets and currencies, chargeback rate, uptime, launch market and policy gates.",
        "output": "Readiness status and any capability, market, risk or reliability blockers.",
    },
    "prfaq-product-spec-agent": {
        "what": "Structures an early product idea into a compact PRFAQ-style spec.",
        "inputs": "Enter the product, customer, problem, outcome and constraints.",
        "output": "Customer promise, metrics, risks, constraints and open questions.",
    },
    "product-prioritization-engine": {
        "what": "Ranks product bets using upside, evidence and delivery/control cost.",
        "inputs": "Provide product bets as JSON with impact, evidence, leverage, effort, dependencies, control burden and opportunity cost.",
        "output": "A ranked list with the score behind each bet.",
    },
    "rag-quality-gate": {
        "what": "Checks grounding, citations and contradictions before an answer is released.",
        "inputs": "Enter the question, candidate answer, evidence passages, citation indexes and known contradictions.",
        "output": "PASS or FAIL with grounding and citation checks.",
    },
    "retrieval-eval-benchmark": {
        "what": "Measures a ranked retrieval result against a known relevant set.",
        "inputs": "Enter ranked IDs, relevant IDs and the K cutoff.",
        "output": "Precision@K, Recall@K, MRR and nDCG.",
    },
    "support-knowledge-os": {
        "what": "Answers from the knowledge base when confidence clears the gate; otherwise escalates.",
        "inputs": "Enter a support question, knowledge-base articles and the confidence threshold.",
        "output": "ANSWER or ESCALATE, confidence, answer text when supported and source IDs.",
    },
    "telemetry-anomaly-to-action": {
        "what": "Detects metric anomalies and maps them to product or operational follow-up.",
        "inputs": "Enter a numeric time series, rolling window and anomaly threshold.",
        "output": "Anomalous points and the mapped follow-up action.",
    },
    "tool-permission-policy-engine": {
        "what": "Applies role, action, data-sensitivity and approval policy to a tool call.",
        "inputs": "Choose caller role, action, sensitivity and approval state; enter the tool name.",
        "output": "ALLOW / REVIEW / DENY with the policy reason.",
    },
    "voc-synthesis-studio": {
        "what": "Combines customer comments with usage signals before ranking product pain.",
        "inputs": "Paste one comment per line and set usage signals for search, onboarding, automation and trust.",
        "output": "Themes and priorities supported by both customer feedback and observed behavior.",
    },
}


SCENARIOS: dict[str, list[dict[str, Any]]] = {
    "agent-vs-workflow-router": [
        {"label": "Stable, high-consequence workflow", "why": "Repeatable work with high downside favors a deterministic path.", "payload": {"variability": 0.10, "consequence": 0.90, "tool_count": 2, "statefulness": 0.20, "ambiguity": 0.10}},
        {"label": "Exploratory, low-risk task", "why": "High variability with low consequence allows more autonomy.", "payload": {"variability": 0.95, "consequence": 0.15, "tool_count": 7, "statefulness": 0.75, "ambiguity": 0.95}},
    ],
    "agentic-product-control-plane": [
        {"label": "Healthy search rollout", "why": "Registered search access and healthy runtime signals clear the gates.", "payload": {"agent_name": "research-agent", "tools": ["search", "draft"], "approval_tools": [], "tool_request": "search", "approved": False, "min_eval": 0.80, "eval_score": 0.94, "incident_rate": 0.002, "max_cost": 0.30, "cost_p95": 0.12, "rollout": "shadow"}},
        {"label": "Refund + cost breach", "why": "The refund needs approval and current cost exceeds budget.", "payload": {"agent_name": "finance-agent", "tools": ["search", "refund"], "approval_tools": ["refund"], "tool_request": "refund", "approved": False, "min_eval": 0.85, "eval_score": 0.88, "incident_rate": 0.004, "max_cost": 0.20, "cost_p95": 0.48, "rollout": "canary"}},
    ],
    "billing-reconciliation-observatory": [
        {"label": "Exact invoice match", "why": "Usage × rate equals the invoice.", "payload": {"record_id": "meter-ok", "quantity": 80.0, "unit_price": 2.5, "invoice_amount": 200.0, "tolerance": 0.01}},
        {"label": "Large invoice mismatch", "why": "The invoice is materially above rated usage.", "payload": {"record_id": "meter-bad", "quantity": 80.0, "unit_price": 2.5, "invoice_amount": 255.0, "tolerance": 0.50}},
    ],
    "experiment-analysis-copilot": [
        {"label": "Clear conversion uplift", "why": "Treatment shows a meaningful lift at scale.", "payload": {"control_success": 1000, "control_n": 10000, "treatment_success": 1250, "treatment_n": 10000, "alpha": 0.05}},
        {"label": "Flat experiment", "why": "Treatment is effectively flat versus control.", "payload": {"control_success": 1000, "control_n": 10000, "treatment_success": 1005, "treatment_n": 10000, "alpha": 0.05}},
    ],
    "finance-close-orchestrator": [
        {"label": "Clean close progression", "why": "Upstream tasks are complete and reconciliation is clear.", "payload": {"completed": ["ap-close", "ar-close", "cash-position"], "reconcile_exception": ""}},
        {"label": "Reconciliation blocked", "why": "A material mismatch blocks downstream close steps.", "payload": {"completed": ["ap-close", "ar-close", "cash-position"], "reconcile_exception": "bank cash differs from ledger by $250K"}},
    ],
    "fraud-signal-decision-engine": [
        {"label": "Low-risk purchase", "why": "All risk signals are low.", "payload": {"velocity": 0.10, "device_novelty": 0.10, "payment_mismatch": 0.05, "identity_risk": 0.10, "behavior_anomaly": 0.05, "review_threshold": 0.43, "block_threshold": 0.72}},
        {"label": "Mixed-risk review", "why": "Several elevated signals push the case into review.", "payload": {"velocity": 0.65, "device_novelty": 0.55, "payment_mismatch": 0.50, "identity_risk": 0.45, "behavior_anomaly": 0.55, "review_threshold": 0.40, "block_threshold": 0.75}},
    ],
    "human-in-loop-risk-router": [
        {"label": "Safe reversible action", "why": "Low consequence and high reversibility allow the action.", "payload": {"consequence": 0.15, "confidence": 0.95, "reversibility": 0.95, "sensitive": False}},
        {"label": "Sensitive irreversible action", "why": "High consequence and low reversibility require stronger control.", "payload": {"consequence": 0.95, "confidence": 0.60, "reversibility": 0.10, "sensitive": True}},
    ],
    "incident-triage-agent": [
        {"label": "Minor non-revenue degradation", "why": "Low error rate and small blast radius keep severity down.", "payload": {"title": "Admin report export is slower than normal.", "error_rate": 0.005, "affected_pct": 0.03, "revenue_path": False}},
        {"label": "Checkout outage", "why": "High errors on a revenue path drive a severe escalation.", "payload": {"title": "Checkout requests are failing and payments time out across regions.", "error_rate": 0.15, "affected_pct": 0.80, "revenue_path": True}},
    ],
    "instagram-intentional-discovery": [
        {"label": "Short design session", "why": "A tight time budget favors short, relevant items.", "payload": {"interests": ["design"], "seen_creators": "c2", "minutes_left": 4, "items_json": "[{\"id\":\"design-tip\",\"creator\":\"c1\",\"tags\":[\"design\"],\"minutes\":2},{\"id\":\"repeat-design\",\"creator\":\"c2\",\"tags\":[\"design\"],\"minutes\":2},{\"id\":\"travel-long\",\"creator\":\"c3\",\"tags\":[\"travel\"],\"minutes\":8}]"}},
        {"label": "AI + travel discovery", "why": "More time gives novelty and diversity room to influence the rank.", "payload": {"interests": ["ai", "travel"], "seen_creators": "", "minutes_left": 10, "items_json": "[{\"id\":\"ai-agent\",\"creator\":\"a1\",\"tags\":[\"ai\"],\"minutes\":3},{\"id\":\"tokyo\",\"creator\":\"t1\",\"tags\":[\"travel\"],\"minutes\":4},{\"id\":\"rage-ai\",\"creator\":\"a2\",\"tags\":[\"ai\"],\"ragebait\":true,\"minutes\":2},{\"id\":\"food\",\"creator\":\"f1\",\"tags\":[\"food\"],\"minutes\":2}]"}},
    ],
    "linkedin-career-discovery": [
        {"label": "AI platform direction", "why": "Platform experience plus agent/eval growth favors AI-platform roles.", "payload": {"skills": "product, platform, ai, payments", "learn_next": "agents, evals", "locations": ["Seattle", "Bay Area"], "jobs_json": "[{\"title\":\"AI Agent Platform PM\",\"skills\":[\"product\",\"platform\",\"ai\",\"agents\",\"evals\"],\"location\":\"Bay Area\",\"days_old\":2},{\"title\":\"Payments PM\",\"skills\":[\"product\",\"payments\"],\"location\":\"Seattle\",\"days_old\":4},{\"title\":\"Ads Growth PM\",\"skills\":[\"growth\",\"ads\"],\"location\":\"Seattle\",\"days_old\":1}]"}},
        {"label": "Remote payments direction", "why": "Payments skills and a remote preference change the ranking.", "payload": {"skills": "product, payments, risk", "learn_next": "fintech, platform", "locations": ["Remote"], "jobs_json": "[{\"title\":\"Remote Payments Platform PM\",\"skills\":[\"product\",\"payments\",\"platform\"],\"location\":\"Remote\",\"days_old\":5},{\"title\":\"AI PM\",\"skills\":[\"product\",\"ai\"],\"location\":\"Bay Area\",\"days_old\":1},{\"title\":\"Risk PM\",\"skills\":[\"product\",\"risk\",\"fintech\"],\"location\":\"Remote\",\"days_old\":12}]"}},
    ],
    "mautam-evaluation": [
        {"label": "Healthy AI capability", "why": "All six lenses are strong.", "payload": {"model_quality": 0.93, "adoption": 0.90, "workflow_success": 0.91, "trust_controls": 0.94, "availability_health": 0.96, "business_impact": 0.89}},
        {"label": "Trust gate failure", "why": "Strong model quality does not clear a weak trust gate.", "payload": {"model_quality": 0.94, "adoption": 0.82, "workflow_success": 0.86, "trust_controls": 0.40, "availability_health": 0.90, "business_impact": 0.84}},
    ],
    "payment-provider-onboarding": [
        {"label": "Ready for Brazil", "why": "Market, currency, capability, risk and uptime requirements are met.", "payload": {"capabilities": ["tokenization", "webhooks", "idempotency", "refunds", "disputes"], "countries": "BR, MX, US", "currencies": "BRL, MXN, USD", "chargeback_rate": 0.006, "uptime": 0.9997, "country": "BR", "currency": "BRL", "max_chargeback_rate": 0.01, "min_uptime": 0.999}},
        {"label": "Market + risk blockers", "why": "Currency support, chargebacks and uptime all block launch readiness.", "payload": {"capabilities": ["tokenization", "webhooks", "refunds"], "countries": "US, CA", "currencies": "USD, CAD", "chargeback_rate": 0.025, "uptime": 0.997, "country": "BR", "currency": "BRL", "max_chargeback_rate": 0.01, "min_uptime": 0.999}},
    ],
    "prfaq-product-spec-agent": [
        {"label": "Support knowledge copilot", "why": "A support problem produces a customer promise, metrics and open questions.", "payload": {"name": "Support Knowledge Copilot", "customer": "customer support specialist", "problem": "Agents lose time searching across inconsistent policy documents before answering customers.", "outcome": "Grounded policy answers in seconds with citations and escalation when evidence is weak.", "constraints": "PII privacy\nHuman review for consequential actions\nSource citations"}},
        {"label": "Developer incident assistant", "why": "A developer-platform problem exercises the same spec structure in another domain.", "payload": {"name": "Incident Context Assistant", "customer": "on-call engineer", "problem": "Responders spend the first 20 minutes reconstructing changes, owners, and telemetry during incidents.", "outcome": "Assemble a trusted incident brief before responders start mitigation.", "constraints": "Read-only production access\nAuditability\nNo automatic remediation"}},
    ],
    "product-prioritization-engine": [
        {"label": "Evidence beats excitement", "why": "Strong evidence offsets lower headline impact against a speculative bet.", "payload": {"items_json": "[{\"name\":\"grounded-search\",\"impact\":0.72,\"evidence\":0.95,\"leverage\":0.78,\"effort\":0.30,\"dependencies\":0.20,\"control_burden\":0.15,\"opportunity_cost\":0.20},{\"name\":\"autonomous-actions\",\"impact\":0.95,\"evidence\":0.25,\"leverage\":0.90,\"effort\":0.85,\"dependencies\":0.80,\"control_burden\":0.90,\"opportunity_cost\":0.75},{\"name\":\"eval-dashboard\",\"impact\":0.65,\"evidence\":0.85,\"leverage\":0.75,\"effort\":0.25,\"dependencies\":0.15,\"control_burden\":0.10,\"opportunity_cost\":0.15}]"}},
        {"label": "Two close roadmap bets", "why": "Similar upside makes evidence and effort more decisive.", "payload": {"items_json": "[{\"name\":\"workflow-builder\",\"impact\":0.80,\"evidence\":0.75,\"leverage\":0.70,\"effort\":0.45,\"dependencies\":0.30,\"control_burden\":0.25,\"opportunity_cost\":0.25},{\"name\":\"analytics-copilot\",\"impact\":0.82,\"evidence\":0.60,\"leverage\":0.80,\"effort\":0.55,\"dependencies\":0.35,\"control_burden\":0.20,\"opportunity_cost\":0.30}]"}},
    ],
    "rag-quality-gate": [
        {"label": "Grounded cited answer", "why": "The supplied passages support the answer and both are cited.", "payload": {"question": "How are risky tool calls controlled?", "answer": "Risky tool calls are constrained by allowlists and may require human approval; audit traces record calls.", "evidence": "Tool access is constrained by explicit allowlists and approval gates.\nEvery tool call is written to an audit trace.", "citations": "0,1", "contradictions": 0}},
        {"label": "Unsupported answer", "why": "The answer conflicts with the supplied evidence.", "payload": {"question": "Can the agent delete customer accounts automatically?", "answer": "Yes. The agent can always delete customer accounts without approval.", "evidence": "Account deletion requires explicit human approval.\nTool access is limited by role and policy.", "citations": "0", "contradictions": 1}},
    ],
    "retrieval-eval-benchmark": [
        {"label": "Strong retrieval", "why": "Relevant documents dominate the top ranks.", "payload": {"ranked": "d1,d2,d5,d8,d9", "relevant": "d1,d2,d5", "k": 5}},
        {"label": "Weak retrieval", "why": "Only one relevant document appears, and it is late in the ranking.", "payload": {"ranked": "d8,d9,d7,d1,d6", "relevant": "d1,d2,d5", "k": 5}},
    ],
    "support-knowledge-os": [
        {"label": "Answerable refund question", "why": "The knowledge base contains the refund timing policy.", "payload": {"query": "How long does an approved refund take?", "articles_json": "[{\"id\":\"refunds\",\"text\":\"Approved refunds arrive in five to seven business days.\"},{\"id\":\"password\",\"text\":\"Use account recovery to reset a forgotten password.\"}]", "threshold": 0.18}},
        {"label": "Unknown warranty question", "why": "The knowledge base has no warranty evidence, so the result escalates.", "payload": {"query": "Does the product include a lifetime hardware warranty?", "articles_json": "[{\"id\":\"refunds\",\"text\":\"Approved refunds arrive in five to seven business days.\"},{\"id\":\"shipping\",\"text\":\"Standard shipping takes three to five business days.\"}]", "threshold": 0.30}},
    ],
    "telemetry-anomaly-to-action": [
        {"label": "Stable metric", "why": "The series stays within the normal range.", "payload": {"values": "100,101,99,100,102,101,100,99,101,100", "window": 5, "threshold": 2.5}},
        {"label": "Sudden production drop", "why": "A sharp change follows a stable baseline.", "payload": {"values": "100,101,99,100,102,100,98,52,50,49", "window": 5, "threshold": 2.0}},
    ],
    "tool-permission-policy-engine": [
        {"label": "Viewer reads internal data", "why": "A read-only internal action stays within the viewer boundary.", "payload": {"role": "viewer", "tool": "analytics", "action": "read", "sensitivity": "internal", "approved": False}},
        {"label": "Operator refund without approval", "why": "A financial mutation triggers the approval boundary.", "payload": {"role": "operator", "tool": "payments", "action": "refund", "sensitivity": "restricted", "approved": False}},
    ],
    "voc-synthesis-studio": [
        {"label": "Search pain dominates", "why": "Repeated search complaints align with heavy search usage.", "payload": {"comments": "Search results are hard to trust\nI cannot find the right report\nSearch makes me try three different queries\nAutomation is fine", "search": 0.90, "onboarding": 0.30, "automation": 0.55, "trust": 0.45}},
        {"label": "Onboarding + trust friction", "why": "A different feedback and usage pattern moves the priority to onboarding and trust.", "payload": {"comments": "Setup takes too many steps\nI do not understand why the agent needs this permission\nOnboarding documentation is confusing\nSearch works well", "search": 0.45, "onboarding": 0.90, "automation": 0.40, "trust": 0.85}},
    ],
}


_JSON_LIST_FIELDS: dict[str, dict[str, tuple[str, ...]]] = {
    "instagram-intentional-discovery": {"items_json": ("id", "creator", "tags", "minutes")},
    "linkedin-career-discovery": {"jobs_json": ("title", "skills", "location", "days_old")},
    "product-prioritization-engine": {"items_json": ("name", "impact", "evidence", "leverage", "effort", "dependencies", "control_burden", "opportunity_cost")},
    "support-knowledge-os": {"articles_json": ("id", "text")},
}


def _parse_json_list(value: Any, label: str, required_keys: tuple[str, ...], errors: list[str]) -> list[Any] | None:
    try:
        parsed = json.loads(str(value))
    except json.JSONDecodeError:
        errors.append(f"{label} must be valid JSON. Load a sample scenario if you prefer not to edit JSON manually.")
        return None
    if not isinstance(parsed, list) or not parsed:
        errors.append(f"{label} must be a non-empty JSON list.")
        return None
    for index, item in enumerate(parsed):
        if not isinstance(item, dict):
            errors.append(f"{label} item {index + 1} must be a JSON object.")
            continue
        missing = [key for key in required_keys if key not in item]
        if missing:
            errors.append(f"{label} item {index + 1} is missing: {', '.join(missing)}.")
    return parsed


def validate_payload(slug: str, payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    for field_name, required_keys in _JSON_LIST_FIELDS.get(slug, {}).items():
        _parse_json_list(payload.get(field_name, ""), field_name.replace("_", " ").title(), required_keys, errors)

    if slug == "agentic-product-control-plane" and not str(payload.get("agent_name", "")).strip():
        errors.append("Agent name cannot be empty.")
    if slug == "billing-reconciliation-observatory" and not str(payload.get("record_id", "")).strip():
        errors.append("Record ID cannot be empty.")
    if slug == "experiment-analysis-copilot":
        if int(payload["control_success"]) > int(payload["control_n"]):
            errors.append("Control conversions cannot exceed control users.")
        if int(payload["treatment_success"]) > int(payload["treatment_n"]):
            errors.append("Treatment conversions cannot exceed treatment users.")
    if slug == "fraud-signal-decision-engine" and float(payload["review_threshold"]) >= float(payload["block_threshold"]):
        errors.append("Review threshold must be lower than block threshold.")
    if slug == "incident-triage-agent" and not str(payload.get("title", "")).strip():
        errors.append("Incident description cannot be empty.")
    if slug == "prfaq-product-spec-agent":
        for key, label in {"name": "Product name", "customer": "Primary customer", "problem": "Customer problem", "outcome": "Product promise"}.items():
            if not str(payload.get(key, "")).strip():
                errors.append(f"{label} cannot be empty.")
    if slug == "rag-quality-gate":
        evidence = [line.strip() for line in str(payload.get("evidence", "")).splitlines() if line.strip()]
        if not evidence:
            errors.append("Add at least one evidence passage.")
        raw_citations = [x.strip() for x in str(payload.get("citations", "")).split(",") if x.strip()]
        try:
            citations = [int(x) for x in raw_citations]
        except ValueError:
            citations = []
            errors.append("Citation indexes must be comma-separated integers such as 0,1.")
        if any(index < 0 or index >= len(evidence) for index in citations):
            errors.append("Each citation index must point to an evidence passage. Indexes are zero-based.")
    if slug == "retrieval-eval-benchmark":
        ranked = [x.strip() for x in str(payload.get("ranked", "")).split(",") if x.strip()]
        relevant = [x.strip() for x in str(payload.get("relevant", "")).split(",") if x.strip()]
        if not ranked:
            errors.append("Add at least one ranked document ID.")
        if not relevant:
            errors.append("Add at least one relevant document ID.")
    if slug == "support-knowledge-os" and not str(payload.get("query", "")).strip():
        errors.append("Support question cannot be empty.")
    if slug == "telemetry-anomaly-to-action":
        raw = [x.strip() for x in str(payload.get("values", "")).split(",") if x.strip()]
        try:
            values = [float(x) for x in raw]
        except ValueError:
            values = []
            errors.append("Metric series must contain only comma-separated numbers.")
        window = int(payload["window"])
        if values and len(values) < window:
            errors.append(f"Rolling window ({window}) cannot exceed the number of metric points ({len(values)}).")
    if slug == "tool-permission-policy-engine" and not str(payload.get("tool", "")).strip():
        errors.append("Tool name cannot be empty.")
    if slug == "voc-synthesis-studio":
        comments = [line.strip() for line in str(payload.get("comments", "")).splitlines() if line.strip()]
        if not comments:
            errors.append("Add at least one customer comment.")
    return errors
