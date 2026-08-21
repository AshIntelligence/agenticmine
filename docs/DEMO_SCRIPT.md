# 6-minute interview demo script

## 0:00–0:30 — Frame the portfolio

> These are independent prototypes, not production systems. I built them because I wanted to test agent architecture decisions firsthand — grounding, orchestration, tool boundaries, state, evaluation, observability, failure modes, latency/cost, and human approval.

Open `README.md` or the Streamlit app.

## 0:30–2:15 — Document Intelligence

Run:

```bash
AGENT_MODE=mock python demo.py docs
```

Ask:

> Compare the availability targets and postmortem timing. Where do the policies conflict?

Show:
1. retrieved chunks;
2. citations in the output;
3. trace JSONL;
4. golden test with two intentionally conflicting source files.

Say:

> My design choice was retrieve first, synthesize second. The model never gets permission to manufacture evidence. The eval also checks the citations instead of treating a fluent answer as success.

## 2:15–3:30 — Job Research

Run:

```bash
AGENT_MODE=mock python demo.py jobs
```

Show the Anthropic role ranking.

Say:

> I split discovery from fit analysis because they're different objectives. My first implementation actually failed this test: a generic cloud role had perfect resume coverage and outranked Anthropic. I fixed it by separating candidate-fit coverage from current search-intent relevance.

## 3:30–5:00 — Product / Technical Design

Run:

```bash
AGENT_MODE=mock python demo.py product
```

Show the four stages:

`discovery -> architecture -> evaluation -> red team`

Say:

> I use multiple agents only where the objectives are meaningfully different. The red-team stage exists to challenge over-agentization, permissions, grounding, tool failure, and latency/cost. Consequential actions stay behind an approval boundary.

## 5:00–5:40 — Evals

Run:

```bash
AGENT_MODE=mock python run_evals.py
```

Show `4/4`.

## 5:40–6:00 — Close

> The point of the repo isn't that three prototypes are frontier infrastructure. It's that I can reason about agent systems from both sides: I have operated hyperscale platform/reliability programs professionally, and I build agent architectures hands-on enough to understand where grounding, orchestration, evaluation, permissions, and reliability break.
