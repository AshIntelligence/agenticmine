from __future__ import annotations

from dataclasses import asdict, is_dataclass
from functools import lru_cache
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def _f(name: str, label: str, kind: str, default: Any, **kwargs: Any) -> dict[str, Any]:
    return {"name": name, "label": label, "kind": kind, "default": default, **kwargs}


CATALOG: list[dict[str, Any]] = [
    {
        "slug": "agent-vs-workflow-router",
        "title": "Agent vs Workflow Router",
        "category": "Agents & Control",
        "summary": "Choose deterministic workflow, assisted agent, or autonomous agent from product risk and task variability.",
        "fields": [
            _f("variability", "Task variability", "slider", .75, min=0.0, max=1.0, step=.05),
            _f("consequence", "Consequence of a wrong action", "slider", .35, min=0.0, max=1.0, step=.05),
            _f("tool_count", "Tools available", "number", 4, min=0, max=12, step=1),
            _f("statefulness", "Statefulness", "slider", .55, min=0.0, max=1.0, step=.05),
            _f("ambiguity", "Ambiguity", "slider", .70, min=0.0, max=1.0, step=.05),
        ],
    },
    {
        "slug": "agentic-product-control-plane",
        "title": "Agent Control Plane",
        "category": "Agents & Control",
        "summary": "Register an agent, authorize a tool call, and decide whether rollout can advance.",
        "fields": [
            _f("agent_name", "Agent name", "text", "finance-agent"),
            _f("tools", "Registered tools", "multiselect", ["search", "draft", "refund"], options=["search", "draft", "refund", "delete-account", "publish"]),
            _f("approval_tools", "Approval-required tools", "multiselect", ["refund"], options=["refund", "delete-account", "publish"]),
            _f("tool_request", "Tool call to authorize", "select", "refund", options=["search", "draft", "refund", "delete-account", "publish"]),
            _f("approved", "Human approval already granted", "checkbox", False),
            _f("min_eval", "Minimum eval score", "slider", .82, min=0.0, max=1.0, step=.01),
            _f("eval_score", "Current eval score", "slider", .89, min=0.0, max=1.0, step=.01),
            _f("incident_rate", "Incident rate", "slider", .005, min=0.0, max=.08, step=.001),
            _f("max_cost", "Max cost budget", "number", .25, min=.01, max=5.0, step=.01),
            _f("cost_p95", "Current p95 cost", "number", .19, min=0.0, max=5.0, step=.01),
            _f("rollout", "Current rollout stage", "select", "canary", options=["shadow", "canary", "production"]),
        ],
    },
    {
        "slug": "billing-reconciliation-observatory",
        "title": "Billing Reconciliation Observatory",
        "category": "Fintech & Reliability",
        "summary": "Compare usage, rated price, and invoice amount and surface reconciliation failures.",
        "fields": [
            _f("record_id", "Record ID", "text", "meter-42"),
            _f("quantity", "Usage quantity", "number", 50.0, min=0.0, max=1000000.0, step=1.0),
            _f("unit_price", "Rated unit price", "number", 3.0, min=0.0, max=10000.0, step=.01),
            _f("invoice_amount", "Invoice amount", "number", 400.0, min=0.0, max=10000000.0, step=.01),
            _f("tolerance", "Tolerance", "number", .01, min=0.0, max=1000.0, step=.01),
        ],
    },
    {
        "slug": "experiment-analysis-copilot",
        "title": "Experiment Analysis Copilot",
        "category": "Product Intelligence",
        "summary": "Evaluate conversion uplift and statistical significance before recommending SHIP, HOLD, or STOP.",
        "fields": [
            _f("control_success", "Control conversions", "number", 1200, min=0, max=10000000, step=1),
            _f("control_n", "Control users", "number", 10000, min=1, max=10000000, step=1),
            _f("treatment_success", "Treatment conversions", "number", 1320, min=0, max=10000000, step=1),
            _f("treatment_n", "Treatment users", "number", 10000, min=1, max=10000000, step=1),
            _f("alpha", "Significance threshold", "select", .05, options=[.10, .05, .01]),
        ],
    },
    {
        "slug": "finance-close-orchestrator",
        "title": "Finance Close Orchestrator",
        "category": "Fintech & Reliability",
        "summary": "Explore dependency-aware finance-close states and human-controller checkpoints.",
        "fields": [
            _f("completed", "Completed tasks", "multiselect", ["ap-close", "ar-close", "cash-position"], options=["ap-close", "ar-close", "cash-position", "reconcile", "gl-close", "controller-approval"]),
            _f("reconcile_exception", "Reconciliation exception", "text", "cash mismatch > tolerance"),
        ],
    },
    {
        "slug": "fraud-signal-decision-engine",
        "title": "Risk Decision System",
        "category": "Fintech & Reliability",
        "summary": "Combine risk signals into explainable ALLOW, REVIEW, or BLOCK decisions.",
        "fields": [
            _f("velocity", "Velocity risk", "slider", .90, min=0.0, max=1.0, step=.05),
            _f("device_novelty", "Device novelty", "slider", .20, min=0.0, max=1.0, step=.05),
            _f("payment_mismatch", "Payment mismatch", "slider", .70, min=0.0, max=1.0, step=.05),
            _f("identity_risk", "Identity risk", "slider", .80, min=0.0, max=1.0, step=.05),
            _f("behavior_anomaly", "Behavior anomaly", "slider", .25, min=0.0, max=1.0, step=.05),
            _f("review_threshold", "Review threshold", "slider", .43, min=0.0, max=.95, step=.01),
            _f("block_threshold", "Block threshold", "slider", .72, min=.05, max=1.0, step=.01),
        ],
    },
    {
        "slug": "human-in-loop-risk-router",
        "title": "Human-in-the-Loop Risk Router",
        "category": "Agents & Control",
        "summary": "Route an AI action to ALLOW, REVIEW, or DENY using consequence, confidence, reversibility, and sensitivity.",
        "fields": [
            _f("consequence", "Consequence", "slider", .70, min=0.0, max=1.0, step=.05),
            _f("confidence", "Model confidence", "slider", .85, min=0.0, max=1.0, step=.05),
            _f("reversibility", "Reversibility", "slider", .40, min=0.0, max=1.0, step=.05),
            _f("sensitive", "Sensitive data/action", "checkbox", True),
        ],
    },
    {
        "slug": "incident-triage-agent",
        "title": "Incident Triage Agent",
        "category": "Fintech & Reliability",
        "summary": "Paste an incident and get severity, owner, matched signals, and the next operational action.",
        "fields": [
            _f("title", "Incident description", "textarea", "Checkout latency increased 9x and invoice callbacks are timing out."),
            _f("error_rate", "Error rate", "slider", .08, min=0.0, max=.20, step=.005),
            _f("affected_pct", "Affected traffic", "slider", .35, min=0.0, max=1.0, step=.05),
            _f("revenue_path", "Revenue-critical path", "checkbox", True),
        ],
    },
    {
        "slug": "instagram-intentional-discovery",
        "title": "Intentional Discovery Study",
        "category": "Discovery & Ranking",
        "summary": "Re-rank a synthetic discovery feed using relevance, novelty, diversity, ragebait, and time budget.",
        "fields": [
            _f("interests", "Interests", "multiselect", ["design", "travel"], options=["design", "travel", "ai", "food", "fitness"]),
            _f("seen_creators", "Already-seen creators (comma separated)", "text", "c2"),
            _f("minutes_left", "Minutes available", "number", 6, min=1, max=120, step=1),
            _f("items_json", "Feed items (JSON)", "textarea", '[{"id":"quiet-design","creator":"c1","tags":["design","travel"],"minutes":2},{"id":"rage","creator":"c2","tags":["design"],"ragebait":true,"minutes":1},{"id":"long","creator":"c3","tags":["travel"],"minutes":12}]'),
        ],
    },
    {
        "slug": "linkedin-career-discovery",
        "title": "Career Discovery Ranking Study",
        "category": "Discovery & Ranking",
        "summary": "Rank synthetic opportunities using skill fit, growth direction, freshness, and location preference.",
        "fields": [
            _f("skills", "Current skills (comma separated)", "text", "product, ai, platform, payments"),
            _f("learn_next", "Skills to grow (comma separated)", "text", "agents, evals"),
            _f("locations", "Preferred locations", "multiselect", ["Seattle", "Bay Area"], options=["Seattle", "Bay Area", "New York", "Remote"]),
            _f("jobs_json", "Candidate opportunities (JSON)", "textarea", '[{"title":"AI Platform PM","skills":["product","ai","platform","agents","evals"],"location":"Bay Area","days_old":3},{"title":"Growth PM","skills":["growth","ads"],"location":"Seattle","days_old":1},{"title":"Payments Platform PM","skills":["product","platform","payments"],"location":"Seattle","days_old":7}]'),
        ],
    },
    {
        "slug": "mautam-evaluation",
        "title": "MAUTAM AI Product Evaluation",
        "category": "Evaluation & RAG",
        "summary": "Evaluate AI product health across model quality, adoption, workflow success, trust, availability, and impact.",
        "fields": [
            _f("model_quality", "Model & response quality", "slider", .88, min=0.0, max=1.0, step=.01),
            _f("adoption", "Adoption", "slider", .74, min=0.0, max=1.0, step=.01),
            _f("workflow_success", "Workflow success", "slider", .82, min=0.0, max=1.0, step=.01),
            _f("trust_controls", "Trust & controls", "slider", .91, min=0.0, max=1.0, step=.01),
            _f("availability_health", "Availability & health", "slider", .79, min=0.0, max=1.0, step=.01),
            _f("business_impact", "Measurable business impact", "slider", .77, min=0.0, max=1.0, step=.01),
        ],
    },
    {
        "slug": "payment-provider-onboarding",
        "title": "Payment Provider Onboarding",
        "category": "Fintech & Reliability",
        "summary": "Test provider capabilities and regional readiness before launch.",
        "fields": [
            _f("capabilities", "Provider capabilities", "multiselect", ["tokenization", "webhooks", "idempotency", "refunds", "disputes"], options=["tokenization", "webhooks", "idempotency", "refunds", "disputes"]),
            _f("countries", "Supported countries (comma separated)", "text", "BR, MX, US"),
            _f("currencies", "Supported currencies (comma separated)", "text", "BRL, MXN, USD"),
            _f("chargeback_rate", "Provider chargeback rate", "number", .006, min=0.0, max=.20, step=.001),
            _f("uptime", "Provider uptime", "number", .9995, min=0.0, max=1.0, step=.0001),
            _f("country", "Launch country", "text", "BR"),
            _f("currency", "Launch currency", "text", "BRL"),
            _f("max_chargeback_rate", "Maximum chargeback rate", "number", .01, min=0.0, max=.20, step=.001),
            _f("min_uptime", "Minimum uptime", "number", .999, min=0.0, max=1.0, step=.0001),
        ],
    },
    {
        "slug": "prfaq-product-spec-agent",
        "title": "PRFAQ Product Spec Agent",
        "category": "Product Intelligence",
        "summary": "Turn a product idea into a structured customer promise, metrics, risks, and open questions.",
        "fields": [
            _f("name", "Product name", "text", "Close Copilot"),
            _f("customer", "Primary customer", "text", "finance analyst"),
            _f("problem", "Customer problem", "textarea", "Manual exception chasing slows the monthly close."),
            _f("outcome", "Product promise", "textarea", "Close exceptions resolved faster"),
            _f("constraints", "Constraints (one per line)", "textarea", "SOX controls\nPII privacy"),
        ],
    },
    {
        "slug": "product-prioritization-engine",
        "title": "Evidence-Weighted Prioritization",
        "category": "Product Intelligence",
        "summary": "Rank product bets using impact, evidence, leverage, effort, dependencies, control burden, and opportunity cost.",
        "fields": [
            _f("items_json", "Product bets (JSON)", "textarea", '[{"name":"agent-dashboard","impact":0.7,"evidence":0.95,"leverage":0.8,"effort":0.3,"dependencies":0.2,"control_burden":0.2,"opportunity_cost":0.2},{"name":"autonomous-agent","impact":0.85,"evidence":0.35,"leverage":0.9,"effort":0.8,"dependencies":0.8,"control_burden":0.9,"opportunity_cost":0.7}]'),
        ],
    },
    {
        "slug": "rag-quality-gate",
        "title": "Grounded RAG Quality Gate",
        "category": "Evaluation & RAG",
        "summary": "Check whether an answer is sufficiently grounded and correctly cited before it can ship.",
        "fields": [
            _f("question", "Question", "textarea", "What controls protect agent tool use?"),
            _f("answer", "Candidate answer", "textarea", "Tool calls use allowlists, human approval and audit traces."),
            _f("evidence", "Evidence (one passage per line)", "textarea", "Agent tool use is constrained by allowlists and approval gates.\nAudit traces record each tool call."),
            _f("citations", "Citation indexes (comma separated, zero-based)", "text", "0,1"),
            _f("contradictions", "Known contradictions", "number", 0, min=0, max=20, step=1),
        ],
    },
    {
        "slug": "retrieval-eval-benchmark",
        "title": "Retrieval Evaluation Benchmark",
        "category": "Evaluation & RAG",
        "summary": "Measure Precision@K, Recall@K, MRR, and nDCG for a retrieval result set.",
        "fields": [
            _f("ranked", "Ranked document IDs (comma separated)", "text", "d3,d1,d9,d2,d7"),
            _f("relevant", "Relevant document IDs (comma separated)", "text", "d1,d2,d5"),
            _f("k", "K", "number", 5, min=1, max=50, step=1),
        ],
    },
    {
        "slug": "support-knowledge-os",
        "title": "Customer Support Knowledge OS",
        "category": "Evaluation & RAG",
        "summary": "Ask a support question. The system answers from known evidence or escalates when confidence is too low.",
        "fields": [
            _f("query", "Ask the support agent", "textarea", "When will my approved refund arrive?"),
            _f("articles_json", "Knowledge base (JSON)", "textarea", '[{"id":"refunds","text":"Approved refund arrives in five to seven business days."},{"id":"password","text":"Use account recovery to reset a forgotten password."}]'),
            _f("threshold", "Answer confidence gate", "slider", .18, min=0.0, max=1.0, step=.01),
        ],
    },
    {
        "slug": "telemetry-anomaly-to-action",
        "title": "Telemetry Anomaly → Action",
        "category": "Product Intelligence",
        "summary": "Detect a metric anomaly and translate it into a product action instead of stopping at an alert.",
        "fields": [
            _f("values", "Metric series (comma separated)", "text", "100,102,98,101,99,100,52,101,150"),
            _f("window", "Rolling window", "number", 5, min=2, max=50, step=1),
            _f("threshold", "Z-score threshold", "number", 2.0, min=.5, max=10.0, step=.1),
        ],
    },
    {
        "slug": "tool-permission-policy-engine",
        "title": "Agent Tool Permission Policy",
        "category": "Agents & Control",
        "summary": "Evaluate a tool call against role, mutation risk, sensitivity, and approval state.",
        "fields": [
            _f("role", "Caller role", "select", "operator", options=["guest", "viewer", "analyst", "operator", "admin"]),
            _f("tool", "Tool", "text", "payments"),
            _f("action", "Action", "select", "refund", options=["search", "read", "list", "draft", "publish", "refund", "transfer", "delete"]),
            _f("sensitivity", "Data sensitivity", "select", "restricted", options=["internal", "confidential", "restricted"]),
            _f("approved", "Approval granted", "checkbox", False),
        ],
    },
    {
        "slug": "voc-synthesis-studio",
        "title": "Voice of Customer Synthesis",
        "category": "Product Intelligence",
        "summary": "Combine customer comments with usage evidence so loud anecdotes do not automatically become roadmap priority.",
        "fields": [
            _f("comments", "Customer comments (one per line)", "textarea", "Search is confusing and I cannot find the right report\nToo much manual workflow setup\nSearch is fast when it works"),
            _f("search", "Search usage signal", "slider", .80, min=0.0, max=1.0, step=.05),
            _f("onboarding", "Onboarding usage signal", "slider", .20, min=0.0, max=1.0, step=.05),
            _f("automation", "Automation usage signal", "slider", .60, min=0.0, max=1.0, step=.05),
            _f("trust", "Trust usage signal", "slider", .30, min=0.0, max=1.0, step=.05),
        ],
    },
]

CATALOG_BY_SLUG = {item["slug"]: item for item in CATALOG}


def default_payload(slug: str) -> dict[str, Any]:
    return {field["name"]: field["default"] for field in CATALOG_BY_SLUG[slug]["fields"]}


def _csv(value: str) -> list[str]:
    return [x.strip() for x in str(value).split(",") if x.strip()]


def _lines(value: str) -> list[str]:
    return [x.strip() for x in str(value).splitlines() if x.strip()]


def _json(value: str) -> Any:
    return json.loads(value)


def _normalize(value: Any) -> Any:
    if is_dataclass(value):
        return _normalize(asdict(value))
    if isinstance(value, dict):
        return {str(k): _normalize(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_normalize(v) for v in value]
    return value


@lru_cache(maxsize=None)
def load_engine(slug: str):
    path = ROOT / "projects" / slug / "main.py"
    if not path.exists():
        raise FileNotFoundError(path)
    module_name = "ash_demo_" + slug.replace("-", "_")
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {slug}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def run_product(slug: str, p: dict[str, Any]) -> Any:
    m = load_engine(slug)

    if slug == "agent-vs-workflow-router":
        return _normalize(m.route(float(p["variability"]), float(p["consequence"]), int(p["tool_count"]), float(p["statefulness"]), float(p["ambiguity"])))

    if slug == "agentic-product-control-plane":
        spec = m.AgentSpec(str(p["agent_name"]), list(p["tools"]), float(p["max_cost"]), min_eval=float(p["min_eval"]), requires_approval=list(p["approval_tools"]), rollout=str(p["rollout"]))
        plane = m.ControlPlane()
        plane.register(spec)
        tool_decision = plane.authorize(spec.name, str(p["tool_request"]), bool(p["approved"]))
        rollout = plane.assess(spec.name, m.RuntimeSignals(float(p["eval_score"]), float(p["incident_rate"]), float(p["cost_p95"])))
        return {"tool_authorization": tool_decision, "rollout": rollout, "audit": plane.audit}

    if slug == "billing-reconciliation-observatory":
        rid = str(p["record_id"])
        return m.reconcile([{"id": rid, "qty": float(p["quantity"])}], [{"id": rid, "unit_price": float(p["unit_price"])}], [{"id": rid, "amount": float(p["invoice_amount"])}], tolerance=float(p["tolerance"]))

    if slug == "experiment-analysis-copilot":
        return m.analyze(int(p["control_success"]), int(p["control_n"]), int(p["treatment_success"]), int(p["treatment_n"]), alpha=float(p["alpha"]))

    if slug == "finance-close-orchestrator":
        exception = str(p["reconcile_exception"]).strip()
        exceptions = {"reconcile": exception} if exception else {}
        return m.plan(set(p["completed"]), exceptions)

    if slug == "fraud-signal-decision-engine":
        policy = m.DecisionPolicy(float(p["review_threshold"]), float(p["block_threshold"]))
        signals = {k: float(p[k]) for k in m.WEIGHTS}
        return m.decide(signals, policy)

    if slug == "human-in-loop-risk-router":
        return _normalize(m.decide(float(p["consequence"]), float(p["confidence"]), float(p["reversibility"]), bool(p["sensitive"])))

    if slug == "incident-triage-agent":
        return m.triage(str(p["title"]), float(p["error_rate"]), float(p["affected_pct"]), bool(p["revenue_path"]))

    if slug == "instagram-intentional-discovery":
        return m.rank(_json(str(p["items_json"])), set(p["interests"]), set(_csv(str(p["seen_creators"]))), int(p["minutes_left"]))

    if slug == "linkedin-career-discovery":
        profile = {"skills": _csv(str(p["skills"])), "learn_next": _csv(str(p["learn_next"])), "locations": list(p["locations"])}
        return m.rank(profile, _json(str(p["jobs_json"])))

    if slug == "mautam-evaluation":
        lenses = {k: float(p[k]) for k in m.WEIGHTS}
        return _normalize(m.evaluate(lenses))

    if slug == "payment-provider-onboarding":
        provider = {"capabilities": list(p["capabilities"]), "countries": _csv(str(p["countries"])), "currencies": _csv(str(p["currencies"])), "chargeback_rate": float(p["chargeback_rate"]), "uptime": float(p["uptime"])}
        market = {"country": str(p["country"]).strip(), "currency": str(p["currency"]).strip(), "max_chargeback_rate": float(p["max_chargeback_rate"]), "min_uptime": float(p["min_uptime"])}
        return m.assess(provider, market)

    if slug == "prfaq-product-spec-agent":
        return _normalize(m.generate(str(p["name"]), str(p["customer"]), str(p["problem"]), str(p["outcome"]), _lines(str(p["constraints"]))))

    if slug == "product-prioritization-engine":
        return m.rank(_json(str(p["items_json"])))

    if slug == "rag-quality-gate":
        evidence = _lines(str(p["evidence"]))
        citations = [int(x) for x in _csv(str(p["citations"]))]
        return _normalize(m.evaluate(str(p["question"]), str(p["answer"]), evidence, citations, int(p["contradictions"])))

    if slug == "retrieval-eval-benchmark":
        return m.metrics(_csv(str(p["ranked"])), set(_csv(str(p["relevant"]))), int(p["k"]))

    if slug == "support-knowledge-os":
        return m.answer(str(p["query"]), _json(str(p["articles_json"])), threshold=float(p["threshold"]))

    if slug == "telemetry-anomaly-to-action":
        values = [float(x) for x in _csv(str(p["values"]))]
        return m.detect(values, int(p["window"]), float(p["threshold"]))

    if slug == "tool-permission-policy-engine":
        return m.authorize(str(p["role"]), str(p["tool"]), str(p["action"]), str(p["sensitivity"]), bool(p["approved"]))

    if slug == "voc-synthesis-studio":
        telemetry = {k: float(p[k]) for k in ("search", "onboarding", "automation", "trust")}
        return m.synthesize(_lines(str(p["comments"])), telemetry)

    raise KeyError(slug)


def verify_catalog() -> dict[str, Any]:
    slugs = [item["slug"] for item in CATALOG]
    missing = [slug for slug in slugs if not (ROOT / "projects" / slug / "main.py").exists()]
    return {"count": len(slugs), "unique": len(set(slugs)) == len(slugs), "missing": missing}
