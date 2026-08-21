# Ash Baskaran — Agentic AI Builder Portfolio

Independent, runnable AI-system prototypes focused on **grounding, tool use, orchestration, evaluation, observability, reliability, and human-control boundaries**.

[Run locally](RUN_ME_FIRST.md) · [Architecture](docs/ARCHITECTURE.md)

> Public demo data in this repository is synthetic. The repo does not contain a resume, interview materials, or private career documents.

## Projects

### 1. Document Intelligence Agent

```text
Files → extraction → chunking → BM25 retrieval → evidence IDs
      → synthesis → citation evaluation → JSONL trace
```

Capabilities:
- ingest TXT / MD / JSON / CSV and optionally PDF / DOCX;
- retrieve evidence before synthesis;
- preserve source/chunk IDs;
- compare documents and surface conflicting evidence;
- evaluate citation coverage;
- trace retrieval, synthesis, output, and latency.

### 2. Research & Ranking Agent

```text
Search intent → candidate discovery → profile evidence
              → requirement matching → explicit gaps
              → relevance + fit score → ranking → trace
```

The included profile and opportunity data are **synthetic examples** used only to demonstrate ranking, evidence matching, gap preservation, and scoring behavior.

### 3. Product / Technical Design Agent

```text
Brief → Discovery Agent → Architecture Agent
      → Evaluation Agent → Red-Team Agent
      → structured design → rollout gates → trace
```

Capabilities:
- decompose an ambiguous brief into users, hypotheses, journeys, and requirements;
- propose retrieval, tool, state, and agent boundaries;
- create an evaluation plan;
- red-team permissions, grounding, prompt injection, tool failure, latency/cost, and over-agentization;
- preserve human-review gates for consequential actions.

## Shared principles

- **Ground before generation.**
- **Keep tool boundaries explicit.**
- **Use structured stage outputs.**
- **Evaluate behavior with golden cases.**
- **Trace meaningful execution steps.**
- **Use deterministic logic where it is safer.**
- **Keep public demos reproducible and synthetic.**

## Run locally

### Windows

Double-click:

```text
run_windows.bat
```

Or manually:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:AGENT_MODE="mock"
streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
AGENT_MODE=mock streamlit run app.py
```

## Tests and evals

```bash
python run_evals.py
pytest -q
```

Expected:

```text
Golden behavioral evals: 4/4 passing
Unit tests: 3/3 passing
```

## Optional live Claude mode

```bash
AGENT_MODE=live
ANTHROPIC_API_KEY=YOUR_KEY
ANTHROPIC_MODEL=claude-sonnet-5
streamlit run app.py
```

Never commit API keys or a real `.streamlit/secrets.toml`.

## Tech

Python · Streamlit · Anthropic SDK · retrieval · tool calling · evals · JSONL traces
