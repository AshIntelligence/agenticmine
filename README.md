# Ash Intelligence — Product & AI Systems

[![Lab checks](https://github.com/AshIntelligence/agenticmine/actions/workflows/tests.yml/badge.svg)](https://github.com/AshIntelligence/agenticmine/actions/workflows/tests.yml)

Ash Intelligence is where I work through product and architecture questions in code — agent boundaries, retrieval quality, evaluation, permissions, workflow state, fintech decisioning, observability and product discovery.

Most of the systems are intentionally small enough to inspect end to end. I care about the mechanics around the model as much as the model itself: what stays deterministic, where evidence is required, when a human enters the loop, how the system fails, and what I would measure before expanding autonomy.

**Portfolio:** https://ashbaskaran.netlify.app/ · **LinkedIn:** https://www.linkedin.com/in/ashb27 · **Lab site:** https://ashintelligence.github.io/agenticmine/

## Agent architecture & control

- [Agent vs Workflow Router](projects/agent-vs-workflow-router/) — chooses deterministic, assisted or autonomous behavior from variability, consequence and state.
- [Human-in-the-Loop Risk Router](projects/human-in-loop-risk-router/) — maps consequence, confidence, reversibility and sensitivity to `ALLOW / REVIEW / DENY`.
- [Agent Tool Permission Policy](projects/tool-permission-policy-engine/) — role-aware tool policy with approval and audit boundaries.
- [Agentic Product Control Plane](projects/agentic-product-control-plane/) — eval gates, tool policy, cost budgets and rollout state in one control surface.
- [Finance Close Orchestrator](projects/finance-close-orchestrator/) — dependency-bound specialist stages, exceptions and controller approval.

## Evaluation, retrieval & evidence

- [MAUTAM AI Product Evaluation](projects/mautam-eval-lab/) — model quality, adoption, workflow success, trust, health and measurable impact.
- [Grounded RAG Quality Gate](projects/rag-quality-gate/) — evidence coverage and citation checks before answer release.
- [Retrieval Evaluation Benchmark](projects/retrieval-eval-benchmark/) — Precision@K, Recall@K, MRR and nDCG.
- [Customer Support Knowledge OS](projects/support-knowledge-os/) — answer with evidence or escalate.
- Document intelligence and source-grounded comparison also live under [`agents/`](agents/).

## Fintech, risk & reliability

- [Payment Provider Onboarding](projects/payment-provider-onboarding/)
- [Fraud Signal Decision Engine](projects/fraud-signal-decision-engine/)
- [Billing Reconciliation Observatory](projects/billing-reconciliation-observatory/)
- [Incident Triage Agent](projects/incident-triage-agent/)
- [Telemetry Anomaly → Product Action](projects/telemetry-anomaly-to-action/)

## Product discovery & decision systems

- [Voice of Customer Synthesis](projects/voc-synthesis-studio/)
- [PRFAQ Product Spec Agent](projects/prfaq-product-spec-agent/)
- [Evidence-Weighted Product Prioritization](projects/product-prioritization-engine/)
- [Experiment Analysis Copilot](projects/experiment-analysis-copilot/)

## Product studies

- [Career Discovery Ranking Study](projects/linkedin-career-discovery/) — a personal product study using LinkedIn career discovery as the surface; unaffiliated with LinkedIn.
- [Intentional Discovery Study](projects/instagram-intentional-discovery/) — a personal recommender study using Instagram as the surface; unaffiliated with Instagram.

## How I build here

**Agentic only when the problem earns it.** Variability and ambiguity can justify agency; consequence reduces autonomy.

**Deterministic shell, probabilistic center.** Permissions, routing, state, budgets, audit and rollout gates stay inspectable even when a model sits in the middle.

**Human review is a state, not a disclaimer.** Consequential actions have explicit review and approval paths.

**Ground before generation.** If evidence is weak, the system should be able to stop or escalate.

**Evals reach the workflow.** Model quality matters, but so do completion, adoption, trust, operational health and impact.

**Telemetry should change a decision.** Signals are useful when they alter rollout, prioritization, investigation or the product mechanism.

## Run the lab

```bash
python tools/run_lab.py
```

Each project has a local demo and a self-check. The Streamlit / Anthropic app remains in `app.py`, `agents/`, `core/` and `evals/`.

Run one system directly, for example:

```bash
python projects/mautam-eval-lab/main.py
python projects/mautam-eval-lab/main.py --test
```

## Data

Everything under `projects/` uses synthetic inputs. I do not publish employer or customer confidential data here.

The LinkedIn and Instagram studies are independent explorations and do not imply affiliation or endorsement.
