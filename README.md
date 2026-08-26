# Ash Intelligence Lab

**20 runnable product prototypes across AI control, evaluation, risk, fintech, reliability and product discovery.**

I built the lab to make product mechanics testable. Each system exposes the inputs, rules, state and output behind a decision instead of stopping at a PRD or architecture diagram.

**[▶ Open the live lab](https://ash-intelligence-lab.streamlit.app/)** · **[GitHub profile](https://github.com/AshIntelligence)** · **[Roadmap](docs/PRODUCT_ROADMAP.md)** · **[LinkedIn](https://www.linkedin.com/in/ashb27)**

The collection is organized around three recurring areas:

| Area | Focus |
|---|---|
| **CONTROL** | Autonomy, permissions, approvals, orchestration and rollout |
| **EVALUATE** | Quality, grounding, adoption, reliability, experiments and product health |
| **DECIDE** | Risk, fintech, ranking, incidents and policy tradeoffs |

Every project is small enough to trace **input → decision → output** without hiding the product logic behind a large framework.

---

## Start with the three flagships

### CONTROL · Agent Control Plane

[![Agent Control Plane](docs/assets/control-plane.svg)](https://github.com/AshIntelligence/agent-control-plane)

Agent registration, tool authorization, approval gates, eval thresholds, cost and incident limits, rollout state and audit events in one control surface.

**[▶ Try live](https://ash-intelligence-lab.streamlit.app/?product=agentic-product-control-plane)** · **[Standalone repo](https://github.com/AshIntelligence/agent-control-plane)** · **[Lab source](projects/agentic-product-control-plane/)**

### EVALUATE · MAUTAM — AI Product Evaluation

[![MAUTAM evaluation system](docs/assets/mautam-system.svg)](https://github.com/AshIntelligence/AI-Observability)

Evaluates an AI capability across model quality, adoption, workflow success, trust, availability and measurable impact, then returns **SHIP / TUNE / SIMPLIFY / STOP**.

**[▶ Try live](https://ash-intelligence-lab.streamlit.app/?product=mautam-evaluation)** · **[Standalone repo](https://github.com/AshIntelligence/AI-Observability)** · **[Lab source](projects/mautam-evaluation/)**

### DECIDE · Risk Decision System

[![Risk Decision System](docs/assets/risk-decision-system.svg)](https://github.com/AshIntelligence/risk-decision-system)

Turns behavioral, payment and identity signals into explainable **ALLOW / REVIEW / BLOCK** decisions while keeping review load and good-user harm visible.

**[▶ Try live](https://ash-intelligence-lab.streamlit.app/?product=fraud-signal-decision-engine)** · **[Standalone repo](https://github.com/AshIntelligence/risk-decision-system)** · **[Lab source](projects/fraud-signal-decision-engine/)**

---

## CONTROL

| System | What it does |
|---|---|
| **[Agent Control Plane](projects/agentic-product-control-plane/)** | Authorizes tools and decides whether rollout should HOLD, CANARY or advance to PRODUCTION. |
| **[Agent vs Workflow Router](projects/agent-vs-workflow-router/)** | Chooses deterministic workflow, assisted agent or autonomous agent from variability, consequence and state. |
| **[Human-in-the-Loop Risk Router](projects/human-in-loop-risk-router/)** | Routes AI actions to ALLOW, REVIEW or DENY using confidence, consequence, reversibility and sensitivity. |
| **[Agent Tool Permission Policy](projects/tool-permission-policy-engine/)** | Applies role, mutation risk, data sensitivity and approval policy before a tool can execute. |
| **[Finance Close Orchestrator](projects/finance-close-orchestrator/)** | Sequences dependency-bound finance work and keeps exceptions and controller approval in the workflow state. |

## EVALUATE

| System | What it does |
|---|---|
| **[MAUTAM](projects/mautam-evaluation/)** | Measures AI product health across quality, adoption, workflow, trust, availability and impact. |
| **[Grounded RAG Quality Gate](projects/rag-quality-gate/)** | Checks grounding and citations before an answer is released. |
| **[Retrieval Evaluation Benchmark](projects/retrieval-eval-benchmark/)** | Measures Precision@K, Recall@K, MRR and nDCG for retrieval results. |
| **[Customer Support Knowledge OS](projects/support-knowledge-os/)** | Answers when evidence clears the confidence gate; otherwise escalates. |
| **[Telemetry Anomaly → Product Action](projects/telemetry-anomaly-to-action/)** | Detects anomalies and maps them to rollout, diagnosis or follow-up action. |
| **[Experiment Analysis Copilot](projects/experiment-analysis-copilot/)** | Calculates conversion evidence and returns SHIP, HOLD or STOP. |
| **[Voice of Customer Synthesis](projects/voc-synthesis-studio/)** | Combines customer comments with usage evidence before ranking product pain. |
| **[Evidence-Weighted Prioritization](projects/product-prioritization-engine/)** | Ranks product bets using impact, evidence, leverage, effort and control cost. |
| **[PRFAQ Product Spec Agent](projects/prfaq-product-spec-agent/)** | Converts an early product idea into a customer promise, metrics, constraints, risks and open questions. |

## DECIDE

| System | What it does |
|---|---|
| **[Risk Decision System](projects/fraud-signal-decision-engine/)** | Converts synthetic risk signals into explainable ALLOW / REVIEW / BLOCK states. |
| **[Payment Provider Onboarding](projects/payment-provider-onboarding/)** | Checks provider capability, market support, risk and reliability before launch. |
| **[Billing Reconciliation Observatory](projects/billing-reconciliation-observatory/)** | Finds mismatches across usage → rating → invoice. |
| **[Incident Triage Agent](projects/incident-triage-agent/)** | Turns incident symptoms into severity, owner and next action. |
| **[Career Discovery Ranking Study](projects/linkedin-career-discovery/)** | Ranks synthetic opportunities using fit, growth direction, freshness and location. |
| **[Intentional Discovery Study](projects/instagram-intentional-discovery/)** | Re-ranks a synthetic feed around relevance, novelty, diversity and a finite attention budget. |

### Grounded document Q&A

The live lab also includes a document agent that retrieves evidence first, answers from the retrieved text, cites the chunks and shows its evaluation trace.

**[▶ Open the live lab](https://ash-intelligence-lab.streamlit.app/)**

---

## How I use the lab

The code is there to pressure-test the parts of a product decision that are easy to gloss over in prose:

- whether the work needs an agent at all
- which state stays authoritative outside the model
- where approval, audit or rollback is required
- which metric should change the roadmap
- what happens when confidence is low or a dependency fails
- whether another person can trace why the system produced the result

The aim is simple: build enough of the mechanism to challenge the assumption.

## Run locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Run the underlying systems without the UI:

```bash
python tools/run_systems.py
```

Or run one directly:

```bash
python projects/mautam-evaluation/main.py
python projects/mautam-evaluation/main.py --test
```

The Streamlit layer calls the original engines under `projects/`; it does not duplicate their decision logic.

## Repository map

- `projects/` — 20 compact decision systems
- `streamlit_app.py` — interactive demo hub
- `ui/` — adapters, scenarios and input guidance
- `agents/` — grounded document, job-research and product-design agents
- `core/` — retrieval, tool runtime, evaluation, tracing and LLM abstractions
- `evals/` — behavioral evaluation cases and results
- `tests/` — system, scenario, link and Streamlit coverage
- `docs/` — architecture, deployment and roadmap notes

All demos use synthetic or public-safe inputs.
