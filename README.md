# Ash Intelligence — AI Product Systems Lab

[![Portfolio tests](https://github.com/AshIntelligence/agenticmine/actions/workflows/tests.yml/badge.svg)](https://github.com/AshIntelligence/agenticmine/actions/workflows/tests.yml)

> **20 runnable product / AI systems** across agents, evaluation, fintech, risk, observability, product discovery and product design.

I’m **Ash Baskaran**, a Product & Technology Leader. I built this lab to make my product thinking inspectable in code: not just *what* I would build, but **where I draw system boundaries, when I use an agent, what I measure, what I keep deterministic, and where I require human control**.

**Portfolio:** https://ashbaskaran.netlify.app/ · **LinkedIn:** https://www.linkedin.com/in/ashb27 · **GitHub Pages:** https://ashintelligence.github.io/agenticmine/

## Start here

```bash
python tools/run_showcase.py
```

That runs a demo and self-test for all 20 projects. The showcase projects use only the Python standard library and synthetic data, so they are reproducible without API keys.

The repository’s original Streamlit / Anthropic agent demo remains available separately in the existing `app.py`, `agents/`, `core/`, and `evals/` structure.

## 20 projects

| # | Project | Product / architecture lens |
|---:|---|---|
| 01 | [MAUTAM AI Product Evaluation Lab](projects/01-mautam-eval-lab/) | AI evaluation → **SHIP / TUNE / SIMPLIFY / STOP** |
| 02 | [Agent vs Workflow Router](projects/02-agent-vs-workflow-router/) | Deterministic vs assisted vs autonomous agent |
| 03 | [Grounded RAG Quality Gate](projects/03-rag-quality-gate/) | Evidence coverage, citations, contradiction fallback |
| 04 | [Human-in-the-Loop Risk Router](projects/04-human-in-loop-risk-router/) | Consequence + confidence + reversibility → allow/review/deny |
| 05 | [Multi-Agent Finance Close Orchestrator](projects/05-finance-close-orchestrator/) | Specialist agents, dependencies, exceptions, human checkpoint |
| 06 | [Payment Provider Onboarding Simulator](projects/06-payment-provider-onboarding/) | Reusable provider contracts + regional launch gates |
| 07 | [Fraud Signal Decision Engine](projects/07-fraud-signal-decision-engine/) | Explainable risk decisioning and review boundaries |
| 08 | [Billing Reconciliation Observatory](projects/08-billing-reconciliation-observatory/) | Usage → rating → invoice end-to-end correctness |
| 09 | [Incident Triage Agent](projects/09-incident-triage-agent/) | Severity, ownership and next-action routing |
| 10 | [Voice of Customer Synthesis Studio](projects/10-voc-synthesis-studio/) | Qualitative sentiment + quantitative usage evidence |
| 11 | [PRFAQ Product Spec Agent](projects/11-prfaq-product-spec-agent/) | Product brief → users, promise, metrics, risks, questions |
| 12 | [Evidence-Weighted Prioritization Engine](projects/12-product-prioritization-engine/) | Impact + evidence − effort/dependencies/control burden |
| 13 | [Experiment Analysis Copilot](projects/13-experiment-analysis-copilot/) | Uplift, significance and product decision |
| 14 | [Telemetry Anomaly → Product Action](projects/14-telemetry-anomaly-to-action/) | Anomaly detection that ends in an action, not a red chart |
| 15 | [Retrieval Evaluation Benchmark](projects/15-retrieval-eval-benchmark/) | Precision@K, Recall@K, MRR, nDCG |
| 16 | [Agent Tool Permission Policy Engine](projects/16-tool-permission-policy-engine/) | Role, sensitivity, tool action, approval and audit |
| 17 | [LinkedIn Career Discovery Redesign](projects/17-linkedin-career-discovery-redesign/) | Career fit over raw engagement — independent product exercise |
| 18 | [Instagram Intentional Discovery](projects/18-instagram-intentional-discovery/) | Relevance + novelty + diversity + time budget — independent exercise |
| 19 | [Customer Support Knowledge OS](projects/19-support-knowledge-os/) | Answer with evidence or explicitly escalate |
| 20 | [Agentic Product Control Plane](projects/20-agentic-product-control-plane/) | Agent registry, eval gates, cost budgets and rollout control |

## Architecture principles across the lab

### 1. Agentic only when the problem earns it
Variability and ambiguity can justify agency. High consequence reduces autonomy. Some of the strongest AI product decisions are **not** to use an autonomous agent.

### 2. Deterministic shell, probabilistic center
Permissions, routing, state, budgets, audit and rollout gates should be inspectable even when a model sits in the middle.

### 3. Human review is a product state
`REVIEW` is designed into the state machine for consequential actions. It is not a vague safety disclaimer.

### 4. Ground before generation
A system should be able to say **I do not have enough evidence**. RAG quality is a release criterion, not decoration.

### 5. Evals should reach the user workflow
Model quality alone is incomplete. MAUTAM connects model / response quality to adoption, workflow success, trust, operational health and measurable impact.

### 6. Telemetry should change a decision
I care less about dashboards than about whether a signal changes rollout, prioritization, investigation, or the product mechanism itself.

## Reviewer shortcut — 5 projects to inspect first

If you only have a few minutes:

1. **01 MAUTAM** — my AI-product evaluation philosophy in executable form.
2. **02 Agent vs Workflow Router** — demonstrates mechanism judgment rather than agent hype.
3. **05 Finance Close Orchestrator** — multi-agent workflow + explicit human control.
4. **16 Tool Permission Policy Engine** — product architecture for safe tool use.
5. **20 Agentic Product Control Plane** — evals, tools, cost and rollout in one platform abstraction.

For product sense, inspect **17 LinkedIn Career Discovery** and **18 Instagram Intentional Discovery**.

## Run / verify

Run every demo and test:

```bash
python tools/run_showcase.py
```

Run a single project:

```bash
python projects/01-mautam-eval-lab/main.py
python projects/01-mautam-eval-lab/main.py --test
```

GitHub Actions also runs the original repository tests/evals plus all 20 showcase self-tests.

## Public-data boundary

All examples in `projects/` are **synthetic independent prototypes**. They do not contain confidential employer data. The LinkedIn and Instagram projects are independent product exercises and do not imply affiliation or endorsement.

---

**AI can mean a lot of things. Around here, it also means Ash Intelligence.**
