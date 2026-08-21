# Ash Baskaran — Agentic AI Builder Portfolio

**Independent, runnable agent prototypes demonstrating hands-on depth in RAG/grounding, native tool use, multi-agent orchestration, evaluation, observability, reliability, and human-control boundaries.**

[Public portfolio site](https://ashintelligence.github.io/agenticmine/) · [Run locally](RUN_ME_FIRST.md) · [Architecture](docs/ARCHITECTURE.md) · [Interview proof pack](docs/INTERVIEW_PROOF_PACK.md)

> These are independent prototypes/product experiments, not claims of enterprise production deployment. The proof is in runnable code, visible system boundaries, traces, tests, and evals.

## Proof at a glance

| Signal | Proof |
|---|---|
| Runnable systems | **3** agent prototypes |
| Behavioral evaluation | **4/4** golden cases passing |
| Unit tests | **3/3** passing |
| Grounding | Retrieval before synthesis + explicit evidence IDs |
| Tool use | Native Claude client-tool loop in live mode |
| Multi-agent orchestration | Discovery → Architecture → Evaluation → Red Team |
| Observability | JSONL traces for meaningful agent steps |
| Reliability | Deterministic mock mode for interview-safe demos |
| Live model path | Anthropic Python SDK + `claude-sonnet-5` |

## The three prototypes

### 1. Document Intelligence Agent
Files → extraction → chunking → BM25 retrieval → evidence IDs → Claude synthesis → citation evaluation → JSONL trace.

It can ingest TXT/MD/JSON/CSV and optionally PDF/DOCX, retrieve evidence before generation, preserve source IDs, compare documents, surface conflicting evidence, and evaluate citation coverage.

### 2. Research / Job Discovery Agent
Search intent → candidate discovery → resume evidence → requirement matching → explicit gaps → query relevance + fit score → ranking → trace/eval.

The design intentionally separates *fit* from *current search intent* so a generic role with broad overlap does not automatically outrank the user's actual target.

### 3. Product / Technical Design Agent
Brief → Discovery Agent → Architecture Agent → Evaluation Agent → Red-Team Agent → structured design → rollout gates → trace.

The stages have different objectives and explicit boundaries. Consequential actions stay behind human approval points.

## Run locally

### Windows — easiest

Double-click:

```text
run_windows.bat
```

It creates a virtual environment, installs dependencies, sets deterministic mock mode, and launches Streamlit at:

```text
http://localhost:8501
```

### Manual

```bash
python -m venv .venv
pip install -r requirements.txt
streamlit run app.py
```

Set `AGENT_MODE=mock` for the interview-safe deterministic path.

## Proof checks

```bash
python run_evals.py
pytest -q
```

Expected:

```text
Golden behavioral evals: 4/4 passing
Unit tests: 3/3 passing
```

## Live Claude mode

```bash
AGENT_MODE=live
ANTHROPIC_API_KEY=YOUR_KEY
ANTHROPIC_MODEL=claude-sonnet-5
streamlit run app.py
```

Never commit an API key or a real `.streamlit/secrets.toml`.

## Public surfaces

- GitHub: `AshIntelligence/agenticmine`
- GitHub Pages: `https://ashintelligence.github.io/agenticmine/`
- Streamlit Community Cloud entrypoint: `streamlit_app.py`
- Interview fallback: local Streamlit via `run_windows.bat`

## Defensible interview framing

> I wanted hands-on intuition rather than being a TPM who only talks around AI systems, so I built inspectable prototypes myself. I can walk through the architecture, show where deterministic logic ends and model judgment begins, demonstrate native tool use, show failed eval cases and fixes, and explain reliability and human-control tradeoffs. These are independent prototypes—not enterprise production deployments.
