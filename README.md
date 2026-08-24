# Ash Intelligence — Product & AI Systems

[![System checks](https://github.com/AshIntelligence/agenticmine/actions/workflows/tests.yml/badge.svg)](https://github.com/AshIntelligence/agenticmine/actions/workflows/tests.yml)

I use this repo to build through questions I keep running into in AI product work: when an agent should act, when it should stop, how to ground an answer, how to review a risky action, how to measure whether something is actually useful, and how to keep cost and reliability visible.

I keep most projects compact enough that I can follow the whole path from input to decision to output. Some are architecture experiments, some are product tools, and some are small implementations of ideas I wanted to test in code.

**[Active roadmap](https://github.com/AshIntelligence/agenticmine/issues)** · **[Portfolio](https://ashbaskaran.netlify.app/)** · **[LinkedIn](https://www.linkedin.com/in/ashb27)**

## Current focus

### MAUTAM — AI product evaluation

[![MAUTAM evaluation system](docs/assets/mautam-system.svg)](https://github.com/AshIntelligence/AI-Observability)

MAUTAM combines model and response quality with adoption, workflow success, trust, availability and measurable impact. The current implementation maps those signals to **SHIP / TUNE / SIMPLIFY / STOP**.

**[Standalone repo →](https://github.com/AshIntelligence/AI-Observability)** · **[Lab source →](projects/mautam-evaluation/)**

### Agentic Product Control Plane

[![Agentic Product Control Plane](docs/assets/control-plane.svg)](https://github.com/AshIntelligence/agent-control-plane)

This brings agent registration, eval gates, tool permissions, cost budgets, incident thresholds and rollout state into one control surface. The browser version lets me change the inputs and see why an agent is held, moved to canary, or promoted.

**[Standalone repo →](https://github.com/AshIntelligence/agent-control-plane)** · **[Lab source →](projects/agentic-product-control-plane/)** · **[Interactive UI source →](docs/control-plane-demo.html)**

### Risk Decision System

[![Risk decision system](docs/assets/risk-decision-system.svg)](https://github.com/AshIntelligence/risk-decision-system)

A small risk-decision engine that keeps signals, policy, human review and action separate. I use it to explore the balance between earlier containment and unnecessary customer friction.

**[Standalone repo →](https://github.com/AshIntelligence/risk-decision-system)** · **[Lab source →](projects/fraud-signal-decision-engine/)** · **[Human-review router →](projects/human-in-loop-risk-router/)**

## Agent architecture & control

- [Agent vs Workflow Router](projects/agent-vs-workflow-router/) — chooses deterministic, assisted or autonomous behavior from variability, consequence and state.
- [Human-in-the-Loop Risk Router](projects/human-in-loop-risk-router/) — maps consequence, confidence, reversibility and sensitivity to `ALLOW / REVIEW / DENY`.
- [Agent Tool Permission Policy](projects/tool-permission-policy-engine/) — role-aware tool policy with approval and audit boundaries.
- [Finance Close Orchestrator](projects/finance-close-orchestrator/) — dependency-bound specialist stages, exceptions and controller approval.

## Evaluation, retrieval & evidence

- [Grounded RAG Quality Gate](projects/rag-quality-gate/) — evidence coverage and citation checks before answer release.
- [Retrieval Evaluation Benchmark](projects/retrieval-eval-benchmark/) — Precision@K, Recall@K, MRR and nDCG.
- [Customer Support Knowledge OS](projects/support-knowledge-os/) — answer with evidence or escalate.
- Document intelligence and source-grounded comparison also live under [`agents/`](agents/).

## Fintech, risk & reliability

- [Payment Provider Onboarding](projects/payment-provider-onboarding/)
- [Billing Reconciliation Observatory](projects/billing-reconciliation-observatory/)
- [Incident Triage Agent](projects/incident-triage-agent/)
- [Telemetry Anomaly → Product Action](projects/telemetry-anomaly-to-action/)

## Product discovery & decision systems

- [Voice of Customer Synthesis](projects/voc-synthesis-studio/)
- [PRFAQ Product Spec Agent](projects/prfaq-product-spec-agent/)
- [Evidence-Weighted Product Prioritization](projects/product-prioritization-engine/)
- [Experiment Analysis Copilot](projects/experiment-analysis-copilot/)

## Product studies

- [Career Discovery Ranking Study](projects/linkedin-career-discovery/) — an independent product study using LinkedIn career discovery as the surface; unaffiliated with LinkedIn.
- [Intentional Discovery Study](projects/instagram-intentional-discovery/) — an independent recommender study using Instagram as the surface; unaffiliated with Instagram.

## A few choices I use across the projects

- If a normal workflow is clearer and safer, I use the workflow.
- Permissions, state, budgets and rollout rules stay explicit instead of disappearing inside model behavior.
- High-consequence actions have a real review path, not just a warning in the UI.
- Retrieval, evals and telemetry are part of the product loop because they change what I ship next.

## Run locally

```bash
python tools/run_systems.py
```

Each project has a local demo and a self-check. The Streamlit app remains in `app.py`, `agents/`, `core/` and `evals/`.

Run one system directly, for example:

```bash
python projects/mautam-evaluation/main.py
python projects/mautam-evaluation/main.py --test
```

The product roadmap lives in [`docs/PRODUCT_ROADMAP.md`](docs/PRODUCT_ROADMAP.md), and current work is tracked in GitHub Issues.

## Data boundary

Everything under `projects/` uses synthetic inputs. I do not publish employer or customer confidential data here.

The LinkedIn and Instagram studies are independent explorations and do not imply affiliation or endorsement.
