# Interview Proof Pack

## One-line positioning

> I wanted hands-on intuition for agent architecture rather than only managing AI programs, so I built three independent prototypes that make retrieval, tool boundaries, evaluation, observability, and human-control decisions inspectable.

## What you can prove live

| Signal | Proof in repo |
|---|---|
| RAG / grounding | Document agent retrieves evidence before synthesis and carries chunk IDs into answers. |
| Tool / workflow decomposition | Job agent separates discovery, evidence matching, gap analysis, and ranking. |
| Multi-agent decomposition | Product-design agent uses four specialized stages. |
| Evaluation | `run_evals.py`, `evals/golden_cases.json`, schema/citation/ranking checks. |
| Observability | JSONL traces record each step, tool boundary, output, and elapsed time. |
| Failure handling | Mock mode, insufficient-evidence behavior, explicit gaps, red-team stage. |
| Human-in-the-loop | Product design requires approval before consequential external actions. |
| Reliability thinking | Golden tests include deliberately conflicting source documents and a previous ranking failure. |

## Failure you can discuss #1 — retrieval vocabulary mismatch

The first document-eval pass asked for “postmortem timing.” One source used “post-incident review.” Retrieval found the source, but extractive sentence selection missed the timing sentence.

**Fix:** normalize domain synonyms and timing concepts before sentence selection.

**Lesson:** retrieval quality includes downstream evidence selection, not just search quality.

## Failure you can discuss #2 — fit score vs. search intent

The first job-ranking implementation ranked a generic cloud-platform TPM above the Anthropic example because generic resume-signal coverage was higher.

**Fix:** separate resume-fit coverage from current search-intent relevance and combine them explicitly.

**Lesson:** optimizing the wrong metric can produce the wrong product outcome even when the algorithm is internally consistent.

## Common interviewer questions

**Where is RAG?** `agents/document_intelligence.py` + `core/retrieval.py`.

**Why not a vector DB?** Small local corpus, deterministic/debuggable demo, replaceable retrieval interface.

**Where are the agents?** `agents/product_design.py`: discovery → architecture → evaluation → red team.

**How do you evaluate them?** `run_evals.py` + `evals/golden_cases.json`.

**How do you observe execution?** `core/tracing.py` writes JSONL with run ID, step, inputs/outputs, latency, and metadata.

**What stays deterministic?** Retrieval, search, scoring, evals, schema checks, mock mode.

**What would you build next?** Hybrid retrieval/reranking, real source adapters, durable state/checkpointing, OpenTelemetry/token-cost accounting, permission-scoped tools, calibrated judge evals.

## Do not overclaim

- These are not production enterprise deployments.
- This repo does not prove direct GPU/Kubernetes cluster ownership.
- It does not prove model training or fine-tuning.
- Lexical retrieval is not a vector database.
- Traces expose inspectable execution artifacts, not hidden chain-of-thought.
